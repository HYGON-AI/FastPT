#!/usr/bin/env bash
set -euo pipefail

shared_dir="$1"
mode="${2:-select}"
: "${DTK_CHANNEL:?}"
: "${DTK_PKG_URL:?}"
: "${AICC_INSTALLER_URL:?}"
: "${AICC_MAJOR:?}"
: "${PYPI_URL:?}"

python_minor=3.10
index_path=nightly/dtk2604
if [[ "${DTK_CHANNEL}" == 2610 ]]; then
    python_minor=3.12
    index_path=das_nightly/dtk2610
elif [[ "${DTK_CHANNEL}" != 2604 ]]; then
    echo "Unsupported DTK channel: ${DTK_CHANNEL}" >&2
    exit 1
fi
python3 -c 'import sys; assert f"{sys.version_info.major}.{sys.version_info.minor}" == sys.argv[1]' "${python_minor}"
mkdir -p "${shared_dir}"

curl -fsSLo /tmp/fastpt-dtk.tar.gz "${DTK_PKG_URL}"
rm -rf /opt/dtk
tar -xzf /tmp/fastpt-dtk.tar.gz -C /opt
dtk_dirs=(/opt/dtk-*)
[[ ${#dtk_dirs[@]} -eq 1 && -d "${dtk_dirs[0]}" ]] || { echo 'Expected one extracted DTK directory' >&2; exit 1; }
mv "${dtk_dirs[0]}" /opt/dtk
export ROCM_PATH=/opt/dtk

curl -fsSLo /tmp/hcu_llvm_installer.sh "${AICC_INSTALLER_URL}"
if [[ "${mode}" == restore ]]; then
    [[ -s "${shared_dir}/aicc-version.txt" && -s "${shared_dir}/wheel-requirements.txt" ]] || exit 1
    printf 'y\n' | bash /tmp/hcu_llvm_installer.sh --version "$(cat "${shared_dir}/aicc-version.txt")"
else
    printf 'y\n' | bash /tmp/hcu_llvm_installer.sh --major "${AICC_MAJOR}" 2>&1 | tee /tmp/fastpt-aicc-install.log
    python3 - /tmp/fastpt-aicc-install.log "${shared_dir}/aicc-version.txt" <<'PY'
import re
import sys
from pathlib import Path

log = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
match = re.search(r"完整版本:\s*(\S+)", log)
if not match:
    raise SystemExit("Cannot determine installed AICC version")
Path(sys.argv[2]).write_text(match.group(1) + "\n", encoding="utf-8")
PY
fi

index="${PYPI_URL%/}/${index_path}/+simple/"
host="${PYPI_URL#*://}"
host="${host%%/*}"
mkdir -p ~/.pip
printf '[global]\nindex-url = %s\nextra-index-url = https://mirrors.huaweicloud.com/artifactory/pypi-public/simple\ntrusted-host = %s\n' \
    "${index}" "${host}" > ~/.pip/pip.conf
if [[ "${mode}" != restore ]]; then
    python3 .github/scripts/select-nightly-wheels.py "${index}" "${shared_dir}/wheel-requirements.txt"
fi
python3 -m pip install --no-cache-dir --pre --upgrade --force-reinstall -r "${shared_dir}/wheel-requirements.txt"
numpy_version=1.24.3
[[ "${DTK_CHANNEL}" == 2610 ]] && numpy_version=1.26.4
python3 -m pip install --no-cache-dir "numpy==${numpy_version}"

set +u
# shellcheck disable=SC1091
source /opt/dtk/env.sh
# shellcheck disable=SC1091
source /opt/dtk/cuda/env.sh
set -u
if [[ "${DTK_CHANNEL}" == 2610 ]]; then
    dnf install -y libevent
    mapfile -t mpi_libraries < <(find /usr /opt -name libmpi.so.40 -print 2>/dev/null)
    mpi_library=
    for candidate in "${mpi_libraries[@]}"; do
        if nm -D "${candidate}" 2>/dev/null | awk '$NF ~ /^MPIX_Query_rocm_support(@|$)/ {found=1} END {exit !found}'; then
            mpi_library="${candidate}"
            break
        fi
    done
    [[ -n "${mpi_library}" ]] || { printf 'No HCU-compatible libmpi.so.40 found; candidates: %s\n' "${mpi_libraries[*]}" >&2; exit 1; }
    echo "Using MPI library: ${mpi_library}"
    export LD_LIBRARY_PATH="$(dirname "${mpi_library}"):${LD_LIBRARY_PATH:-}"
    for ((attempt=0; attempt<10; attempt++)); do
        missing="$(ldd "${mpi_library}" | awk '$2 == "=>" && $3 == "not" {print $1}')"
        [[ -n "${missing}" ]] || break
        while IFS= read -r library; do
            path="$(find /usr /opt -name "${library}" -print -quit 2>/dev/null || true)"
            [[ -n "${path}" ]] || { echo "${library} is missing from the DTK 26.10 image" >&2; exit 1; }
            directory="$(dirname "${path}")"
            case ":${LD_LIBRARY_PATH}:" in
                *":${directory}:"*) ;;
                *) export LD_LIBRARY_PATH="${directory}:${LD_LIBRARY_PATH}" ;;
            esac
        done <<< "${missing}"
    done
    if [[ -n "${GITHUB_ENV:-}" ]]; then
        printf 'LD_LIBRARY_PATH=%s\n' "${LD_LIBRARY_PATH}" >> "${GITHUB_ENV}"
    fi
fi
command -v aicc >/dev/null || { echo 'AICC is missing after installation' >&2; exit 1; }
python3 - "${DTK_CHANNEL}" <<'PY'
import sys
from importlib.metadata import version

import torch

dtk = sys.argv[1]
assert torch.version.hip, "HCU/HIP torch is required"
assert f"dtk{dtk}" in version("torch"), version("torch")
if dtk == "2610":
    for package in ("torchvision", "triton", "flash-attn"):
        assert f"dtk2610.torch2120" in version(package), (package, version(package))
print(f"torch={torch.__version__}, torch.hip={torch.version.hip}")
PY
