#!/usr/bin/env bash
set -euo pipefail

export ROCM_PATH=/opt/dtk
set +u
# shellcheck disable=SC1091
source /opt/dtk/env.sh
# shellcheck disable=SC1091
source /opt/dtk/cuda/env.sh
set -u
shopt -s nullglob
wheels=(dist/manylinux/fastpt-*.whl)
(( ${#wheels[@]} == 1 )) || { echo 'Expected one shared FastPT wheel' >&2; exit 1; }
python3 -m pip install --no-deps --force-reinstall "${wheels[0]}"
python3 -c 'import fastpt; print(fastpt.__version__)'
fastpt.hipify.file --help
torch_path="$(python3 -c 'import os, torch; print(os.path.dirname(torch.__file__))')"
export LD_LIBRARY_PATH="${PWD}/torch-mocker/build:${torch_path}/lib:${LD_LIBRARY_PATH:-}"
ctest --test-dir torch-mocker/build --output-on-failure -j1
