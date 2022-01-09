from setuptools import setup
from glob import glob
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        '_vmath',
        [
            'src/main.cpp', 'src/glm_util.cpp', 'src/wrap_vmath.cpp'
        ],
    ),
]

setup(
    name='vmath',
    version='0.0.2',
    py_modules=['vmath'],
    ext_modules=ext_modules,
    packages=['vmathlib'],
    scripts=[],
)
