---
name: fastpt-hcu-wheel
description: Build and test FastPT HCU manylinux wheels with a matching DTK, Torch and AICC environment.
---

# FastPT HCU wheel

Run from the repository root in a Linux environment with Python, DTK at `/opt/dtk`, matching HCU Torch, AICC, and the `HYGON-AI/pytorch-das` 2.12 source tree installed. The build script checks these prerequisites and installs the remaining build dependencies.

```bash
export HIP_TORCH_PATH=/path/to/pytorch-das
bash build_hcu_wheel.sh
```

The script builds the full FastPT package with `FASTPT_CTEST=1`, repairs the wheel with auditwheel, and requires exactly one `dist/manylinux/fastpt-*.whl`. It fails if the environment or repair is incomplete. Use the same script in PR and release CI; do not substitute `python -m build` because FastPT's `setup.py` needs Torch and compiles torch-mocker.

To verify the result in the matching HCU environment, install the repaired wheel and run the CTest binaries built by the script:

```bash
python3 -m pip install --no-deps --force-reinstall dist/manylinux/fastpt-*.whl
python3 -c 'import fastpt; print(fastpt.__version__)'
fastpt.hipify.file --help
TORCH_PATH="$(python3 -c 'import os, torch; print(os.path.dirname(torch.__file__))')"
export LD_LIBRARY_PATH="$PWD/torch-mocker/build:$TORCH_PATH/lib:${LD_LIBRARY_PATH:-}"
ctest --test-dir torch-mocker/build --output-on-failure -j1
```

CI selects one newest compatible Torch wheel for each DTK channel from its configured simple index. DTK 26.10 also selects matching torchvision, triton, and flash-attn wheels. The selected wheel URLs and exact AICC version are reused by the GPU test job through the run-scoped `/ci_public` directory. CTest failures fail the workflow. PR jobs use read-only GitHub permissions; only the push-triggered publish job receives `PYPI_PASSWORD`.

The target repository must configure Actions variables `PYPI_URL`, `RESOURCE_SERVER_URL`, `DTK2604_IMAGE_UBUNTU_PY310`, `DTK2610_IMAGE_ROCKY_PY312`, `DTK2610_PKG_URL`, and `AICC2610_INSTALLER_URL`. Set `PYPI_URL` to the intended package and NIGHTLY server before enabling the new workflow. The build and GPU runner pools must both mount `/ci_public` at the same path and use the same `GITHUB_WORKSPACE` path so the compiled CTest tree remains valid.

PR Test uses the `v2.12` branch's trusted `pull_request_target` workflow. Changes to that workflow in a PR cannot exercise themselves until they are merged into `v2.12`; validate fork execution with a new fork PR after the merge. GitHub's repository or organization policy may still require a one-time workflow approval for some external contributors.
