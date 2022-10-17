

from setuptools import setup, find_packages, Extension

NAME = "approxer"
AUTHOR = "Anton Normelius"
EMAIL = "a.normelius@gmail.com"
URL = "https://github.com/normelius/approxer"

PACKAGES = ['approxer']

# Read readme.
with open("README.md", "r") as fh:
    long_description = fh.read()

# Read requirements.
with open('requirements.txt') as f:
    required = f.read().splitlines()

module1 = Extension("approxer.odes.ode_solvers",
    sources = ["approxer/odes/euler_lib.cc"],
    extra_compile_args=['-std=c++17'],
)

setup(
    name=NAME,
    py_modules=["approxer"],
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    version="0.1",
    packages=find_packages(),
    install_requires=required,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    ext_modules=[module1]
)
