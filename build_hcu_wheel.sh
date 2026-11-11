#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${repo_root}"
command -v python3 >/dev/null || { echo 'Python 3 is required' >&2; exit 1; }
[[ -f /opt/dtk/env.sh && -f /opt/dtk/cuda/env.sh ]] || { echo 'DTK is required at /opt/dtk' >&2; exit 1; }
export ROCM_PATH=/opt/dtk
set +u
# shellcheck disable=SC1091
source /opt/dtk/env.sh
# shellcheck disable=SC1091
source /opt/dtk/cuda/env.sh
set -u
command -v aicc >/dev/null || { echo 'AICC is required' >&2; exit 1; }
python3 -c 'import torch; assert torch.version.hip, "HCU/HIP torch is required"; print(f"torch={torch.__version__}")'
: "${HIP_TORCH_PATH:?Set HIP_TORCH_PATH to the matching pytorch-das source tree}"
[[ -d "${HIP_TORCH_PATH}/torch" ]] || { echo 'Matching pytorch-das source tree is missing' >&2; exit 1; }

export TORCH_PATH="$(python3 -c 'import os, torch; print(os.path.dirname(torch.__file__))')"
export TORCH_MOCKER_CMAKE_ARGS="${TORCH_MOCKER_CMAKE_ARGS:-} -DPython3_EXECUTABLE=$(command -v python3)"
python3 -m pip install --no-cache-dir wheel setuptools auditwheel patchelf 'cmake>=3.29,<3.30'
export PATH="$(python3 -c 'import sysconfig; print(sysconfig.get_path("scripts"))'):${PATH}"
cmake --version
git config --global --add safe.directory "${repo_root}"
git config --global --add safe.directory "${HIP_TORCH_PATH}"
git submodule update --init --recursive
rm -rf build dist fastpt.egg-info torch-mocker/build
FASTPT_CTEST=1 python3 setup.py bdist_wheel

platform="$(ldd --version | awk 'NR == 1 {split($NF, v, "."); print "manylinux_" v[1] "_" v[2] "_x86_64"}')"
mkdir -p dist/manylinux
auditwheel repair --plat "${platform}" \
    --exclude libc10.so --exclude libc10_hip.so \
    --exclude libtorch.so --exclude libtorch_cpu.so --exclude libtorch_hip.so --exclude libtorch_python.so \
    --exclude libgalaxyhip.so.5 --exclude libMIOpen.so.1 --exclude librccl.so.1 \
    --exclude libhipblas.so.0 --exclude libhipblas.so.2 --exclude libhipblaslt.so.0 \
    --exclude libhipfft.so --exclude libhipfft.so.0 --exclude libhiprand.so.1 \
    --exclude libhipsolver.so.0 --exclude libhipsparse.so.0 --exclude libhipsparse.so.1 \
    --exclude libhipnn.so --exclude librocblas.so.0 --exclude librocblas.so.4 \
    --exclude librocsolver.so.0 --exclude librocfft.so.0 --exclude librocrand.so.1 \
    --exclude librocsparse.so.0 --exclude librocsparse.so.1 \
    --wheel-dir dist/manylinux dist/fastpt-*.whl
shopt -s nullglob
wheels=(dist/manylinux/fastpt-*.whl)
(( ${#wheels[@]} == 1 )) || { echo 'Expected one repaired FastPT wheel' >&2; exit 1; }
[[ "${wheels[0]}" == *manylinux*.whl ]] || { echo 'Wheel is not tagged manylinux' >&2; exit 1; }
ls -lh "${wheels[0]}"
