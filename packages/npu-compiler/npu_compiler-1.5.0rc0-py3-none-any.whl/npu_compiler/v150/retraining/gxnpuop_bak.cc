#include "tensorflow/core/framework/common_shape_fns.h"
#include "tensorflow/core/framework/op.h"
#include "tensorflow/core/framework/shape_inference.h"
#include "tensorflow/core/util/padding.h"
#include "tensorflow/core/framework/numeric_op.h"
#include "tensorflow/core/framework/tensor.h"
#include "tensorflow/core/lib/core/errors.h"
#include "tensorflow/core/platform/protobuf.h"

using namespace tensorflow;
using shape_inference::InferenceContext;

REGISTER_OP("NPUInference")
	.Input("inputs: inputs_num * float")
	.Input("tf_outputs: outputs_num * float")
	.Attr("inputs_num: int >= 1")
	.Attr("outputs_num: int >= 1")
	.Attr("infer_batch: bool = false")
	.Output("outputs: outputs_num * float")
	.SetShapeFn([](InferenceContext* c) {
		int inputs_num, outputs_num;
		c->GetAttr("inputs_num", &inputs_num);
		c->GetAttr("outputs_num", &outputs_num);
		for (int i=0; i<outputs_num; i++) {
			c->set_output(i, c->input(inputs_num+i));
		}
		return Status::OK();
	})
	.Doc(R"doc(
)doc");

// -----------------------------------------------------------------------------

#include "snpu.h"
#include "parse.h"

using tensorflow::DEVICE_CPU;
using tensorflow::OpKernel;
using tensorflow::OpKernelConstruction;
using tensorflow::OpKernelContext;
using tensorflow::Tensor;
using tensorflow::TensorShape;
using tensorflow::TTypes;  // NOLINT This is needed in CUDA mode, do not remove.
using tensorflow::errors::InvalidArgument;

typedef Eigen::ThreadPoolDevice CPUDevice;

#define MCU_TO_DEV(x) x

/*
 * float32: 1 8 23
 * float16: 1 (1-8) (14-7)
 */
static unsigned short float_32_to_16(float in_data, int exponent_width)
{
	int e_bit_width = exponent_width; // 16bits中有e_bit_width指数位
	int d_bit_width = 15 - e_bit_width; // 16bits中有d_bit_width小数位
	unsigned int s, e, d; // 符号位， 指数位， 小数位
	int e_out, d_out;
	unsigned short out_data;
	unsigned char round_bit;
	unsigned int u32_in_data = *(unsigned int *)&in_data;

	s = (u32_in_data & 0x80000000) >> 31;
	e = (u32_in_data & 0x7f800000) >> 23;
	d = (u32_in_data & 0x007fffff);
	e_out = e - (1 << 7) + (1 << (e_bit_width - 1));
	d_out = (d >> (23 - d_bit_width));
	round_bit = ((d >> (23 - d_bit_width - 1)) & 1);
	if (e_out < 0) // overflow
		out_data = (s << 15) | 0;
	else if (e_out >= (1 << e_bit_width) - 1) // overflow
		out_data = (s << 15) | 0x7fff;
	else
		out_data = (s << 15) | (((e_out << d_bit_width) | d_out) + round_bit);

	return out_data;
}

static int snpu_float_32_to_16(const float *in_data, SNPU_FLOAT *out_data, int num)
{
	for (int i=0; i<num; i++) {
		out_data[i] = float_32_to_16(in_data[i], 5);
	}

	return 0;
}

static volatile int is_finished = 0;
static int callback(int module_id, SNPU_STATE state, void *private_data)
{
#if 0
	int i;
	float **out_data = (float**)private_data;
	// print result
	printf("out\n");
	for (i = 0; i < 1000; i++) {
		printf("%f, ", out_data[0][i]);
		if ((i + 1) % 10 == 0)
			printf("\n");
	}
	printf("\n");
#endif
	is_finished = 1;
	return 0;
}

static void run_npu(const char *model, const float **pp_input_data, int input_num, float **pp_output_data, int output_num)
{
	SNPU_TASK kws_task;
	int ret;

	void *handle;
	struct NpuInfo npu_info;

	load_model(&handle, &npu_info, model);

	kws_task.module_id = 3;
	kws_task.ops = (void*)MCU_TO_DEV(npu_info.mcu_content);
	kws_task.data = (void*)MCU_TO_DEV(npu_info.data_content);
	kws_task.cmd = (void*)MCU_TO_DEV(npu_info.cmd_content);
	kws_task.tmp_mem = (void*)MCU_TO_DEV(npu_info.tmp_content);
	kws_task.weight = (void*)MCU_TO_DEV(npu_info.weight_content);
	kws_task.input = (void*)MCU_TO_DEV(npu_info.data_in_content);
	kws_task.output = (void*)MCU_TO_DEV(npu_info.data_out_content);

	SnpuInit();

	is_finished = 0;

	for (int i=0; i<input_num; i++) {
		snpu_float_32_to_16(pp_input_data[i],
				(SNPU_FLOAT*)(npu_info.data_in_content+npu_info.input_offset[i]),
				npu_info.input_size[i]/sizeof(SNPU_FLOAT));
	}
	ret = SnpuRunTask(&kws_task, callback, pp_output_data);
	if (ret) {
		printf("SnpuRunTask error %d\n", ret);
		return;
	}

	while (!is_finished);

	for (int i=0; i<output_num; i++) {
		memcpy(pp_output_data[i], (float*)(npu_info.data_out_content+npu_info.output_offset[i]),
				npu_info.output_size[i]);
	}

	SnpuDone();

	release_model(handle, &npu_info);
}


// -----------------------------------------------------------------------------
template <typename Device>
class GxNPUOp : public OpKernel {
public:
	explicit GxNPUOp(OpKernelConstruction* c)
		: OpKernel::OpKernel(c) {
			OP_REQUIRES_OK(c, c->GetAttr("inputs_num", &inputs_num_));
			OP_REQUIRES_OK(c, c->GetAttr("outputs_num", &outputs_num_));
			OP_REQUIRES_OK(c, c->GetAttr("infer_batch", &infer_batch_));
		}

	void Compute(OpKernelContext* c) override {
		if (infer_batch_)
			_ComputeInferBatch(c);
		else
			_ComputeNormal(c);
	}

	void _ComputeNormal(OpKernelContext* c) {
		const float *p_input_data[MAX_IO_NUM];
		float *p_output_data[MAX_IO_NUM];
		for (int i=0; i<inputs_num_; i++) {
			const Tensor &input_tensor = c->input(i);
			const float *input_data = input_tensor.flat<float>().data();
			p_input_data[i] = input_data;
		}

		for (int i=0; i<outputs_num_; i++) {
			Tensor *output_tensor = nullptr;
			const Tensor &tf_result = c->input(inputs_num_ + i);
			TensorShape output_shape(tf_result.shape());
			OP_REQUIRES_OK(c, c->allocate_output(i, output_shape, &output_tensor));
			float *output_data = output_tensor->flat<float>().data();
			p_output_data[i] = output_data;
		}

		run_npu("model.npu", p_input_data, inputs_num_, p_output_data, outputs_num_);
	}

	void _ComputeInferBatch(OpKernelContext* c) {
		const float *p_input_data[MAX_IO_NUM];
		float *p_output_data[MAX_IO_NUM];
		Tensor *output_tensors[MAX_IO_NUM] = {nullptr};
		const Tensor &input_tensor = c->input(0);
		int batch = input_tensor.shape().dim_size(0);

		// 只支持一个inputs
		if (inputs_num_ != 1) {
			printf("[NPU OP] InferBatch only supports one input num");
			return;
		}

		for (int i=0; i<outputs_num_; i++) {
			const Tensor &tf_result = c->input(inputs_num_ + i);
			TensorShape output_shape(tf_result.shape());
			OP_REQUIRES_OK(c, c->allocate_output(i, output_shape, &output_tensors[i]));
		}

#if 0
		for (int i=0; i<batch; i++) {
			const float *input_data = input_tensor.flat<float>().data();
			int one_batch_input_data_num = input_tensor.shape().num_elements() / batch;
			p_input_data[0] = input_data + one_batch_input_data_num * i;
			for (int j=0; j<outputs_num_; j++) {
				Tensor *output_tensor = output_tensors[j];
				float *output_data = output_tensor->flat<float>().data();
				int one_batch_output_data_num = output_tensors[j]->shape().num_elements() / batch;
				p_output_data[j] = output_data + one_batch_output_data_num * i;
			}
			run_npu("model.npu", p_input_data, inputs_num_, p_output_data, outputs_num_);
		}
#else
		if (thread_num == 0) {
			for (int i=0; i<batch; i++) {
				const float *input_data = input_tensor.flat<float>().data();
				int one_batch_input_data_num = input_tensor.shape().num_elements() / batch;
				p_input_data[0] = input_data + one_batch_input_data_num * i;
				for (int j=0; j<outputs_num_; j++) {
					Tensor *output_tensor = output_tensors[j];
					float *output_data = output_tensor->flat<float>().data();
					int one_batch_output_data_num = output_tensors[j]->shape().num_elements() / batch;
					p_output_data[j] = output_data + one_batch_output_data_num * i;
				}
				run_npu("model.npu", p_input_data, inputs_num_, p_output_data, outputs_num_);
			}
		} else {
			int loop_num = (batch - thread_num + 1) / thread_num;
			int last_loop_batch_index = (loop_num - 1) * thread_num;
			int last_loop_batch_num = batch - last_loop_batch_index;
			//for (int i=0; i<loop_num-1; i++) {
			//	const float *input_data = input_tensor.flat<float>().data();
			//	int one_batch_input_data_num = input_tensor.shape().num_elements() / batch;
			//	p_input_data[0] = input_data + one_batch_input_data_num * i;
			//	for (int j=0; j<outputs_num_; j++) {
			//		Tensor *output_tensor = output_tensors[j];
			//		float *output_data = output_tensor->flat<float>().data();
			//		int one_batch_output_data_num = output_tensors[j]->shape().num_elements() / batch;
			//		p_output_data[j] = output_data + one_batch_output_data_num * i;
			//	}
			//	for (int j=0; j<batch; j++) {
			//		run_npu("model.npu", p_input_data, inputs_num_, p_output_data, outputs_num_);
			//	}
			//}

			load_npu_model();

			const float *input_data = input_tensor.flat<float>().data();
			int one_batch_input_data_num = input_tensor.shape().num_elements() / batch;
			float *output_data_array[MAX_IO_NUM];
			int one_batch_output_data_num_array[MAX_IO_NUM];
			for (int i=0; i<outputs_num_; i++) {
				Tensor *output_tensor = output_tensors[i];
				output_data_array[i] = output_tensor->flat<float>().data();
				one_batch_output_data_num_array[i] = output_tensors[i]->shape().num_elements() / batch;
			}

			for (int k=0; k<last_loop_batch_num; k++) {
				int batch_index = last_loop_batch_index + k;
				p_input_data[0] = input_data + one_batch_input_data_num * batch_index;
				for (int j=0; j<outputs_num_; j++) {
					p_output_data[j] = output_data_array[j] + one_batch_output_data_num_array[j] * batch_index;
				}
				run_npu("model.npu", p_input_data, inputs_num_, p_output_data, outputs_num_);
			}
		}
#endif
	}


private:
	const int MAX_IO_NUM = 10;
	int inputs_num_;
	int outputs_num_;
	bool infer_batch_;
};


REGISTER_KERNEL_BUILDER(Name("NPUInference").Device(DEVICE_CPU), GxNPUOp<CPUDevice>);
