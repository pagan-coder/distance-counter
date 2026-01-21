from setuptools import setup, Extension
from Cython.Build import cythonize


extensions = [
    Extension(
        "distance_wrapper",
        ["distance_wrapper.pyx", "c_lib/distance.c"],
        include_dirs=["c_lib"],
        extra_compile_args=["-O3"],
        language="c"
    )
]

setup(
    name="distance-counter",
    version="1.0.0",
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    zip_safe=False,
    install_requires=[
        "aiohttp>=3.8.0",
        "cython>=0.29.0"
    ]
)
