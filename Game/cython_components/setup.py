from setuptools import setup
from Cython.Build import cythonize
from distutils.sysconfig import get_python_inc
import os

output_dir = os.path.join(os.getcwd(), 'Game/cython_components')  # Change this path as needed

setup(
    ext_modules=cythonize("Game/cython_components/quick_eval.pyx"),
    include_dirs=[get_python_inc()],
    script_args=["build_ext", "--inplace"],
)

# compile with "python Game/cython_components/setup.py build_ext --inplace"