# PyTorch Source Mapping

This file records the provenance classification of PyTorch-derived and generated files bundled in `torch-mocker`.

- Upstream repository: <https://github.com/pytorch/pytorch>
- Upstream version: `v2.12.0`
- Upstream commit: `0d62256a2b23365f8e1604297eb23a6545102aa8`
- License: BSD-3-Clause
- Local license copy: `LICENSE.pytorch.txt`

Classification is based on byte comparison, syntax/token comparison, and inspection of FastPT, torch-mocker, DTK, HCU, HIP, and ROCm adaptation evidence. Internal torch-mocker/FastPT history was also used to confirm modification ownership for semantically different files. A content difference alone is not treated as proof of HYGON authorship.

Of the 88 H2 files, 49 contain direct FastPT, HCU, DTK, or mocker markers. The remaining 39 have substantive differences whose HYGON modification ownership is confirmed by internal torch-mocker/FastPT introduction and adaptation history.

## H5: Upstream-identical PyTorch files (17)

Action: Retain PyTorch attribution; no HYGON header.

| Local path | Upstream path |
| --- | --- |
| `torch-mocker/aten/src/ATen/cuda/CuSparseHandlePool.cpp` | `aten/src/ATen/cuda/CuSparseHandlePool.cpp` |
| `torch-mocker/aten/src/ATen/cuda/MemPool.cpp` | `aten/src/ATen/cuda/MemPool.cpp` |
| `torch-mocker/aten/src/ATen/native/cudnn/BatchNorm.h` | `aten/src/ATen/native/cudnn/BatchNorm.h` |
| `torch-mocker/aten/src/ATen/native/cudnn/ConvShared.h` | `aten/src/ATen/native/cudnn/ConvShared.h` |
| `torch-mocker/aten/src/ATen/native/cudnn/MHA.h` | `aten/src/ATen/native/cudnn/MHA.h` |
| `torch-mocker/aten/src/ATen/native/cudnn/RNNUtils.h` | `aten/src/ATen/native/cudnn/RNNUtils.h` |
| `torch-mocker/include/ATen/cuda/MemPool.h` | `aten/src/ATen/cuda/MemPool.h` |
| `torch-mocker/include/c10/cuda/CUDAAllocatorConfig.h` | `c10/cuda/CUDAAllocatorConfig.h` |
| `torch-mocker/include/c10/util/Half-inl.h` | `c10/util/Half-inl.h` |
| `torch-mocker/include/THC/THCAtomics.cuh` | `aten/src/THC/THCAtomics.cuh` |
| `torch-mocker/include/THC/THCDeviceUtils.cuh` | `aten/src/THC/THCDeviceUtils.cuh` |
| `torch-mocker/include/torch/csrc/jit/codegen/fuser/cuda/resource_strings.h` | `torch/csrc/jit/codegen/fuser/cuda/resource_strings.h` |
| `torch-mocker/include/torch/headeronly/core/TensorAccessor.h` | `torch/headeronly/core/TensorAccessor.h` |
| `torch-mocker/include/torch/headeronly/macros/Export.h` | `torch/headeronly/macros/Export.h` |
| `torch-mocker/include/torch/headeronly/macros/Macros.h` | `torch/headeronly/macros/Macros.h` |
| `torch-mocker/include/torch/headeronly/util/complex.h` | `torch/headeronly/util/complex.h` |
| `torch-mocker/include/torch/headeronly/util/Half.h` | `torch/headeronly/util/Half.h` |

## H2: PyTorch-derived files with confirmed HYGON/FastPT substantive modifications (88)

Action: Retain PyTorch attribution and apply the H2 modification notice.

The `torch-mocker/include/ATen/cudnn/Descriptors.h` overlay uses FastPT-specific
tensor and filter descriptor implementation types to isolate cuDNN/MIOpen
symbols while retaining the original type names as aliases.

| Local path | Upstream path |
| --- | --- |
| `torch-mocker/aten/src/ATen/cuda/CublasHandlePool.cpp` | `aten/src/ATen/cuda/CublasHandlePool.cpp` |
| `torch-mocker/aten/src/ATen/cuda/CUDABlas.cpp` | `aten/src/ATen/cuda/CUDABlas.cpp` |
| `torch-mocker/aten/src/ATen/cuda/CUDAContext.cpp` | `aten/src/ATen/cuda/CUDAContext.cpp` |
| `torch-mocker/aten/src/ATen/cuda/CUDAGeneratorImpl.cpp` | `aten/src/ATen/cuda/CUDAGeneratorImpl.cpp` |
| `torch-mocker/aten/src/ATen/cuda/CUDAGraph.cpp` | `aten/src/ATen/cuda/CUDAGraph.cpp` |
| `torch-mocker/aten/src/ATen/cuda/CUDASparseBlas.cpp` | `aten/src/ATen/cuda/CUDASparseBlas.cpp` |
| `torch-mocker/aten/src/ATen/cuda/detail/CUDAHooks.cpp` | `aten/src/ATen/cuda/detail/CUDAHooks.cpp` |
| `torch-mocker/aten/src/ATen/cuda/detail/LazyNVRTC.cpp` | `aten/src/ATen/cuda/detail/LazyNVRTC.cpp` |
| `torch-mocker/aten/src/ATen/cuda/Exceptions.cpp` | `aten/src/ATen/cuda/Exceptions.cpp` |
| `torch-mocker/aten/src/ATen/cuda/nvrtc_stub/ATenNVRTC.cpp` | `aten/src/ATen/cuda/nvrtc_stub/ATenNVRTC.cpp` |
| `torch-mocker/aten/src/ATen/cuda/nvrtc_stub/ATenNVRTC.h` | `aten/src/ATen/cuda/nvrtc_stub/ATenNVRTC.h` |
| `torch-mocker/aten/src/ATen/cuda/PeerToPeerAccess.cpp` | `aten/src/ATen/cuda/PeerToPeerAccess.cpp` |
| `torch-mocker/aten/src/ATen/cudnn/AutocastRNN.cpp` | `aten/src/ATen/cudnn/AutocastRNN.cpp` |
| `torch-mocker/aten/src/ATen/cudnn/Handle.cpp` | `aten/src/ATen/cudnn/Handle.cpp` |
| `torch-mocker/aten/src/ATen/cudnn/Types.cpp` | `aten/src/ATen/cudnn/Types.cpp` |
| `torch-mocker/aten/src/ATen/detail/CUDAHooksInterface.cpp` | `aten/src/ATen/detail/CUDAHooksInterface.cpp` |
| `torch-mocker/aten/src/ATen/native/cuda/jit_utils.cpp` | `aten/src/ATen/native/cuda/jit_utils.cpp` |
| `torch-mocker/aten/src/ATen/native/cuda/SpectralOps.cpp` | `aten/src/ATen/native/cuda/SpectralOps.cpp` |
| `torch-mocker/aten/src/ATen/native/cudnn/AffineGridGenerator.cpp` | `aten/src/ATen/native/cudnn/AffineGridGenerator.cpp` |
| `torch-mocker/aten/src/ATen/native/cudnn/BatchNorm.cpp` | `aten/src/ATen/native/cudnn/BatchNorm.cpp` |
| `torch-mocker/aten/src/ATen/native/cudnn/Conv_v7.cpp` | `aten/src/ATen/native/cudnn/Conv_v7.cpp` |
| `torch-mocker/aten/src/ATen/native/cudnn/Conv_v8.cpp` | `aten/src/ATen/native/cudnn/Conv_v8.cpp` |
| `torch-mocker/aten/src/ATen/native/cudnn/ConvPlaceholders.cpp` | `aten/src/ATen/native/cudnn/ConvPlaceholders.cpp` |
| `torch-mocker/aten/src/ATen/native/cudnn/ConvShared.cpp` | `aten/src/ATen/native/cudnn/ConvShared.cpp` |
| `torch-mocker/aten/src/ATen/native/cudnn/GridSampler.cpp` | `aten/src/ATen/native/cudnn/GridSampler.cpp` |
| `torch-mocker/aten/src/ATen/native/cudnn/LossCTC.cpp` | `aten/src/ATen/native/cudnn/LossCTC.cpp` |
| `torch-mocker/aten/src/ATen/native/cudnn/MHA.cpp` | `aten/src/ATen/native/cudnn/MHA.cpp` |
| `torch-mocker/aten/src/ATen/native/cudnn/RNN.cpp` | `aten/src/ATen/native/cudnn/RNN.cpp` |
| `torch-mocker/c10/cuda/CUDAAllocatorConfig.cpp` | `c10/cuda/CUDAAllocatorConfig.cpp` |
| `torch-mocker/c10/cuda/CUDACachingAllocator.cpp` | `c10/cuda/CUDACachingAllocator.cpp` |
| `torch-mocker/c10/cuda/CUDADeviceAssertionHost.cpp` | `c10/cuda/CUDADeviceAssertionHost.cpp` |
| `torch-mocker/c10/cuda/CUDAException.cpp` | `c10/cuda/CUDAException.cpp` |
| `torch-mocker/c10/cuda/CUDAFunctions.cpp` | `c10/cuda/CUDAFunctions.cpp` |
| `torch-mocker/c10/cuda/CUDAMallocAsyncAllocator.cpp` | `c10/cuda/CUDAMallocAsyncAllocator.cpp` |
| `torch-mocker/c10/cuda/CUDAMiscFunctions.cpp` | `c10/cuda/CUDAMiscFunctions.cpp` |
| `torch-mocker/c10/cuda/CUDAStream.cpp` | `c10/cuda/CUDAStream.cpp` |
| `torch-mocker/c10/cuda/driver_api.cpp` | `c10/cuda/driver_api.cpp` |
| `torch-mocker/c10/cuda/impl/CUDATest.cpp` | `c10/cuda/impl/CUDATest.cpp` |
| `torch-mocker/c10/util/flags_use_no_gflags.cpp` | `c10/util/flags_use_no_gflags.cpp` |
| `torch-mocker/c10/util/Logging.cpp` | `c10/util/Logging.cpp` |
| `torch-mocker/c10/util/StringUtil.cpp` | `c10/util/StringUtil.cpp` |
| `torch-mocker/include/ATen/cuda/CUDAContextLight.h` | `aten/src/ATen/cuda/CUDAContextLight.h` |
| `torch-mocker/include/ATen/cuda/detail/CUDAHooks.h` | `aten/src/ATen/cuda/detail/CUDAHooks.h` |
| `torch-mocker/include/ATen/cudnn/Descriptors.h` | `aten/src/ATen/cudnn/Descriptors.h` |
| `torch-mocker/include/ATen/detail/CUDAHooksInterface.h` | `aten/src/ATen/detail/CUDAHooksInterface.h` |
| `torch-mocker/include/ATen/native/cuda/jit_utils.h` | `aten/src/ATen/native/cuda/jit_utils.h` |
| `torch-mocker/include/ATen/native/cuda/Loops.cuh` | `aten/src/ATen/native/cuda/Loops.cuh` |
| `torch-mocker/include/ATen/native/cuda/Randperm.cuh` | `aten/src/ATen/native/cuda/Randperm.cuh` |
| `torch-mocker/include/c10/cuda/CUDAGuard.h` | `c10/cuda/CUDAGuard.h` |
| `torch-mocker/include/c10/cuda/CUDAStream.h` | `c10/cuda/CUDAStream.h` |
| `torch-mocker/include/c10/cuda/impl/CUDAGuardImpl.h` | `c10/cuda/impl/CUDAGuardImpl.h` |
| `torch-mocker/include/torch/csrc/autograd/functions/comm.h` | `torch/csrc/autograd/functions/comm.h` |
| `torch-mocker/include/torch/csrc/cuda/comm.h` | `torch/csrc/cuda/comm.h` |
| `torch-mocker/include/torch/csrc/cuda/CUDAPluggableAllocator.h` | `torch/csrc/cuda/CUDAPluggableAllocator.h` |
| `torch-mocker/include/torch/csrc/cuda/Event.h` | `torch/csrc/cuda/Event.h` |
| `torch-mocker/include/torch/csrc/cuda/nccl.h` | `torch/csrc/cuda/nccl.h` |
| `torch-mocker/include/torch/csrc/cuda/Stream.h` | `torch/csrc/cuda/Stream.h` |
| `torch-mocker/include/torch/csrc/cuda/utils.h` | `torch/csrc/cuda/utils.h` |
| `torch-mocker/include/torch/csrc/CudaIPCTypes.h` | `torch/csrc/CudaIPCTypes.h` |
| `torch-mocker/include/torch/csrc/distributed/c10d/cuda/CUDAEventCache.hpp` | `torch/csrc/distributed/c10d/cuda/CUDAEventCache.hpp` |
| `torch-mocker/include/torch/csrc/distributed/c10d/NCCLUtils.hpp` | `torch/csrc/distributed/c10d/NCCLUtils.hpp` |
| `torch-mocker/include/torch/csrc/distributed/c10d/ProcessGroupNCCL.hpp` | `torch/csrc/distributed/c10d/ProcessGroupNCCL.hpp` |
| `torch-mocker/include/torch/csrc/distributed/c10d/ProcessGroupUCC.hpp` | `torch/csrc/distributed/c10d/ProcessGroupUCC.hpp` |
| `torch-mocker/include/torch/csrc/distributed/c10d/symm_mem/CUDASymmetricMemory.hpp` | `torch/csrc/distributed/c10d/symm_mem/CUDASymmetricMemory.hpp` |
| `torch-mocker/include/torch/csrc/distributed/c10d/symm_mem/CUDASymmetricMemoryTypes.hpp` | `torch/csrc/distributed/c10d/symm_mem/CUDASymmetricMemoryTypes.hpp` |
| `torch-mocker/include/torch/csrc/distributed/c10d/symm_mem/intra_node_comm.hpp` | `torch/csrc/distributed/c10d/symm_mem/intra_node_comm.hpp` |
| `torch-mocker/include/torch/csrc/distributed/c10d/symm_mem/nvshmem_team_manager.hpp` | `torch/csrc/distributed/c10d/symm_mem/nvshmem_team_manager.hpp` |
| `torch-mocker/include/torch/csrc/jit/codegen/fuser/cuda/fused_kernel.h` | `torch/csrc/jit/codegen/fuser/cuda/fused_kernel.h` |
| `torch-mocker/include/torch/csrc/jit/cuda/cuda.h` | `torch/csrc/jit/cuda/cuda.h` |
| `torch-mocker/include/torch/csrc/jit/tensorexpr/cuda_codegen.h` | `torch/csrc/jit/tensorexpr/cuda_codegen.h` |
| `torch-mocker/include/torch/csrc/profiler/stubs/base.h` | `torch/csrc/profiler/stubs/base.h` |
| `torch-mocker/include/torch/headeronly/util/BFloat16.h` | `torch/headeronly/util/BFloat16.h` |
| `torch-mocker/include/torch/headeronly/util/Deprecated.h` | `torch/headeronly/util/Deprecated.h` |
| `torch-mocker/include/torch/headeronly/util/Exception.h` | `torch/headeronly/util/Exception.h` |
| `torch-mocker/torch/csrc/autograd/functions/comm.cpp` | `torch/csrc/autograd/functions/comm.cpp` |
| `torch-mocker/torch/csrc/cuda/comm.cpp` | `torch/csrc/cuda/comm.cpp` |
| `torch-mocker/torch/csrc/cuda/CUDAPluggableAllocator.cpp` | `torch/csrc/cuda/CUDAPluggableAllocator.cpp` |
| `torch-mocker/torch/csrc/cuda/nccl.cpp` | `torch/csrc/cuda/nccl.cpp` |
| `torch-mocker/torch/csrc/CudaIPCTypes.cpp` | `torch/csrc/CudaIPCTypes.cpp` |
| `torch-mocker/torch/csrc/distributed/c10d/cuda/utils.cpp` | `torch/csrc/distributed/c10d/cuda/utils.cpp` |
| `torch-mocker/torch/csrc/distributed/c10d/FlightRecorderCuda.cpp` | `torch/csrc/distributed/c10d/FlightRecorderCuda.cpp` |
| `torch-mocker/torch/csrc/distributed/c10d/NanCheck.cu` | `torch/csrc/distributed/c10d/NanCheck.cu` |
| `torch-mocker/torch/csrc/distributed/c10d/NCCLUtils.cpp` | `torch/csrc/distributed/c10d/NCCLUtils.cpp` |
| `torch-mocker/torch/csrc/distributed/c10d/ProcessGroupNCCL.cpp` | `torch/csrc/distributed/c10d/ProcessGroupNCCL.cpp` |
| `torch-mocker/torch/csrc/jit/codegen/fuser/cuda/fused_kernel.cpp` | `torch/csrc/jit/codegen/fuser/cuda/fused_kernel.cpp` |
| `torch-mocker/torch/csrc/jit/tensorexpr/cuda_codegen.cpp` | `torch/csrc/jit/tensorexpr/cuda_codegen.cpp` |
| `torch-mocker/torch/cuda/__init__.py` | `torch/cuda/__init__.py` |
| `torch-mocker/torch/utils/cpp_extension.py` | `torch/utils/cpp_extension.py` |

## H6: Generated files (3)

Action: Treat as generated artifacts; do not edit generated headers directly.

| Local path | Upstream path |
| --- | --- |
| `torch-mocker/include/ATen/cuda/CUDAConfig.h` | Generated artifact |
| `torch-mocker/torch/share/cmake/Caffe2/Caffe2Targets-release.cmake` | Generated artifact |
| `torch-mocker/torch/version.py` | Generated artifact |

