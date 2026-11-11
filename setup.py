# Copyright (c) 2026 Hygon Information Technology Co., Ltd.
# SPDX-License-Identifier: BSD-3-Clause

from setuptools import setup, Extension, find_packages
from setuptools.dist import Distribution
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py
from setuptools.command.build import build
from setuptools.command.install import install
from wheel.bdist_wheel import bdist_wheel
import os
import sys
import shutil
import re

__version__ = '2.12.0'
das_version = 'das'

try:
    import torch
    torch_install_path = os.path.dirname(torch.__file__)
    # CMake consumes TORCH_PATH from its environment. Derive it from the
    # imported torch package so callers do not need to export it manually.
    os.environ["TORCH_PATH"] = torch_install_path
except ImportError as e:
    raise RuntimeError("Torch is required") from e

torch_version = torch.__version__

__version__ = torch.__version__

FASTPT_CTEST = os.getenv("FASTPT_CTEST", "1") == "1"
FASTPT_HIPIFY_ONLY = os.getenv("FASTPT_HIPIFY_ONLY", "0") == "1"


include_ends = ['.h', '.cuh', '.hpp', '.cmake']

cwd = os.path.dirname(os.path.abspath(__file__))
torch_mocker_path = os.path.join(cwd, 'torch-mocker')
torch_obj_build_path = "build/lib/fastpt/torch"  # 存放torch相关文件的路径

class CMakeBuild(build_ext):
    def run(self):
        # 创建构建目录
        tm_build_path = os.path.join(torch_mocker_path, 'build')
        if not os.path.exists(tm_build_path):
            os.makedirs(tm_build_path)

        fmt_cmake_path = os.path.join(torch_mocker_path, 'third_party', 'fmt', 'CMakeLists.txt')
        if not os.path.exists(fmt_cmake_path):
            raise FileNotFoundError(
                "fmt submodule is missing. Run 'git submodule update --init --recursive' "
                "from the fastpt repository root before building."
            )

        torch_lib_path = torch_install_path
        if not os.path.isdir(torch_lib_path):
            raise RuntimeError(f"Torch installation directory does not exist: {torch_lib_path}")
        cmake_args = os.environ.get("TORCH_MOCKER_CMAKE_ARGS", "")
        make_args = "-j8 VERBOSE=1"
        make_args_env = os.environ.get("TORCH_MOCKER_MAKE_ARGS", "")
        make_args += make_args_env
        extra_cmake_args = ""
        cmake_args += extra_cmake_args
        extra_cmake_options = [
            "USE_GLOG=1",
            # "OTHER_OPTION=ON",  # 其他需要添加的参数
        ]
        if FASTPT_CTEST:
            extra_cmake_options.append("USE_TEST=ON")

        extra_cmake_args = " ".join([f"-D{opt}" for opt in extra_cmake_options])

        cmake_args = f"{cmake_args} {extra_cmake_args}".strip()

        build_cmd = f"""
            cd {tm_build_path}
            cmake {cmake_args} ..
            make {make_args}
        """
        ret = os.system(build_cmd)
        if ret != 0:
            raise Exception("Failed to build torch-mocker")

        torch_lib_dir = os.path.join(torch_obj_build_path, 'lib')
        torch_include_dir = os.path.join(torch_obj_build_path, 'include')
        os.makedirs(torch_lib_dir, exist_ok=True)
        os.makedirs(torch_include_dir, exist_ok=True)
        print("-- Copying files")
        so_files = ["libc10_cuda.so", "libtorch_cuda.so", "libtorch_mocker.so"]
        for so_file_name in so_files:
            so_file = os.path.join(tm_build_path, so_file_name)  # 确保路径正确
            shutil.copy(so_file, torch_lib_dir)

        # 复制 include 文件到 torch/include
        file_paths = []
        if os.path.exists(torch_include_dir):
            shutil.rmtree(torch_include_dir)
        include_dir = os.path.join(torch_mocker_path, 'include')
        shutil.copytree(include_dir, torch_include_dir)
        
        _tmp_cuda_dir = os.path.join(torch_obj_build_path, 'cuda')
        _tmp_utils_dir = os.path.join(torch_obj_build_path, 'utils')
        _tmp_share_dir = os.path.join(torch_obj_build_path, 'share/cmake/Caffe2')
        os.makedirs(_tmp_cuda_dir, exist_ok=True)
        os.makedirs(_tmp_utils_dir, exist_ok=True)
        os.makedirs(_tmp_share_dir, exist_ok=True)
        py_files = [
            ('torch/version.py', torch_obj_build_path),
            ('torch/cuda/__init__.py', _tmp_cuda_dir),
            ('torch/utils/cpp_extension.py', _tmp_utils_dir),
            ('torch/share/cmake/Caffe2/Caffe2Targets.cmake', _tmp_share_dir),
            ('torch/share/cmake/Caffe2/Caffe2Targets-release.cmake', _tmp_share_dir),
        ]

        for src_name, tar_version_path in py_files:
            src_path = os.path.join(torch_mocker_path, src_name)
            shutil.copy(src_path, tar_version_path)
            print(f"Copying {src_path} to build directory: {tar_version_path}")

        print("\n torch mocker build succeeded\n")


class CustomBuild(build):
    def run(self):
        self.run_command('build_ext')
        build.run(self)

class CustomDistWheel(bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False

    def run(self):
        self.skip_install = True
        self.run_command('build')
        bdist_wheel.run(self)

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

class NoDistInfoBuild(build_py):
    def run(self):
        super().run()  
        build_dir = self.build_lib
        dist_info_dirs = [d for d in os.listdir(build_dir) if d.endswith('.dist-info')]
        for dist_info_dir in dist_info_dirs:
            shutil.rmtree(os.path.join(build_dir, dist_info_dir))

package_data = {}
package_data["fastpt.torch"] = [
    "include/**/*",
    "lib/*",
    "share/cmake/Caffe2/*.cmake",
    "version.py",          
    "cuda/__init__.py",    
    "utils/cpp_extension.py"  
]
package_data["fastpt"] = [
    "fastpt"
]

ROCM_PATH = os.getenv('ROCM_PATH', "/opt/dtk/")
dtk_path = ROCM_PATH + '/.info/rocm_version'
with open(dtk_path, 'r') as file:
    content = file.read().strip()
dtk_version = content.replace('.', '')
torch_hcu_version = torch.__hcu_version__
hcu_version = __version__.split('+', 1)[0] + f'+das.dtk' + dtk_version
required_version = ".".join(torch_version.split(".")[:2])
print('hcu_version:', hcu_version)
def write_fastpt_shell():
    fastpt_path = os.path.join(cwd, "fastpt", "fastpt")
    with open(fastpt_path, "r+") as f:
        content = f.read()
        lines = content.splitlines(keepends=True)

        version_pattern = re.compile(
            r"^\s*(?:torch_version|require_dtk_version)\s*=\s*['\"].*?['\"]"
        )
        new_lines = [line for line in lines if not version_pattern.match(line)]

        # Keep generated version settings below the shell and license header.
        new_lines[4:4] = [
            f"torch_version='{required_version}'\n",
            f"require_dtk_version='{dtk_version}'\n",
        ]

        new_content = "".join(new_lines)
        f.seek(0)
        f.write(new_content)
        f.truncate()

def write_init_fastpt_file():
    required_version = ".".join(torch_version.split(".")[:2])
    init_path = os.path.join(cwd, "fastpt", "init_process.py")

    with open(init_path, "r+") as f:
        content = f.read()
        lines = content.splitlines(keepends=True)

        new_lines = []
        version_found = False

        for i, line in enumerate(lines):
            match = re.match(r"^\s*required_version\s*=\s*['\"](.*?)['\"]", line)
            if match:
                version_found = True
                new_lines.append(f"required_version='{required_version}'\n")
            else:
                new_lines.append(line)

        if not version_found:
            while len(new_lines) < 15:
                new_lines.append("\n")
            new_lines.insert(14, f"required_version='{required_version}'\n")

        new_content = "".join(new_lines)
        f.seek(0)
        f.write(new_content)
        f.truncate()

def write_version_file():
    version_path = os.path.join(cwd, "fastpt", "__init__.py")
    with open(version_path, "r+") as f:
        content = f.read()
        if re.search(r"^__version__\s*=\s*'.*?'", content, flags=re.MULTILINE):
            content = re.sub(r"^__version__\s*=\s*'.*?'", f"__version__ = '{__version__}'", content, flags=re.MULTILINE)
        else:
            content += f"\n__version__ = '{__version__}'\n"
    
        if re.search(r"^__hcu_version__\s*=\s*'.*?'", content, flags=re.MULTILINE):
            content = re.sub(r"^__hcu_version__\s*=\s*'.*?'", f"__hcu_version__ = '{hcu_version}'", content, flags=re.MULTILINE)
        else:
            content += f"\n__hcu_version__ = '{hcu_version}'\n"
        if re.search(r"^required_version\s*=.*$", content, flags=re.MULTILINE):
            content = re.sub(r"^required_version\s*=.*$", f"required_version = '{required_version}'", content, flags=re.MULTILINE)
        else:
            lines = content.splitlines(keepends=True)
            new_lines = []
            for i, line in enumerate(lines):
                if re.match(r"^\s*try\s*:", line):
                    new_lines.append(f"required_version = '{required_version}'\n")
                new_lines.append(line)
            content = "".join(new_lines)
        f.seek(0)
        f.write(content)
        f.truncate()

python_min_version = (3, 8, 0)
python_min_version_str = ".".join(map(str, python_min_version))


def get_setup_kwargs():
    setup_kwargs = {
        'packages': ["fastpt", "fastpt.torch"],
        'package_dir': {'fastpt.torch': torch_obj_build_path},
        'package_data': package_data,
        'cmdclass': {
            'build': CustomBuild,
            'bdist_wheel': CustomDistWheel,
            'build_ext': CMakeBuild,
        },
        'entry_points': {
            'console_scripts': [
                'fastpt.cuda.init = fastpt.init_process:cuda_init',
                'fastpt.cuda.exe = fastpt.init_process:cuda_exe',
                "fastpt.hipify=fastpt.cli:hipify",
                "fastpt.hipify.file=fastpt.cli:hipify_file",
                "fastpt.hipify.folder=fastpt.cli:hipify_folder",
                "fastpt.hipify.cmake=fastpt.cli:hipify_cmake",
            ]
        },
        'data_files': [
            ('lib', [os.path.join(torch_obj_build_path, "lib", "libtorch_cuda.so"),
                  os.path.join(torch_obj_build_path, "lib", "libtorch_mocker.so"),
                  os.path.join(torch_obj_build_path, "lib", "libc10_cuda.so")]),
        ],
        'scripts': ['fastpt/fastpt'],
    }

    if FASTPT_HIPIFY_ONLY:
        setup_kwargs.update({
            'packages': ["fastpt"],
            'package_dir': {},
            'cmdclass': {},
            'entry_points': {
                'console_scripts': [
                    "fastpt.hipify=fastpt.cli:hipify",
                    "fastpt.hipify.file=fastpt.cli:hipify_file",
                    "fastpt.hipify.folder=fastpt.cli:hipify_folder",
                    "fastpt.hipify.cmake=fastpt.cli:hipify_cmake",
                ]
            },
            'data_files': [],
            'scripts': [],
        })

    return setup_kwargs

if __name__ == "__main__":
    if not FASTPT_HIPIFY_ONLY:
        write_fastpt_shell()
        write_init_fastpt_file()
        write_version_file()
    setup_kwargs = get_setup_kwargs()
    setup(
        name='fastpt',
        version=hcu_version,
        packages=setup_kwargs['packages'],
        package_dir=setup_kwargs['package_dir'],
        package_data=setup_kwargs['package_data'],

        license='BSD-3-Clause',
        license_files=['LICENSE.txt', 'THIRD_PARTY_NOTICES'],
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'License :: OSI Approved :: BSD License (BSD-3-Clause)',
        ],

        ext_modules=[],
        include_package_data=True,
        cmdclass=setup_kwargs['cmdclass'],
        distclass=BinaryDistribution if not FASTPT_HIPIFY_ONLY else Distribution,
        zip_safe=False,
        python_requires=f">={python_min_version_str}",
        entry_points=setup_kwargs['entry_points'],
        data_files=setup_kwargs['data_files'],
        scripts=setup_kwargs['scripts']
    )
