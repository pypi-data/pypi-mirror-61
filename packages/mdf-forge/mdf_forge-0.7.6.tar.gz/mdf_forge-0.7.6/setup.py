import os
from setuptools import setup

# Single source of truth for version
version_ns = {}
with open(os.path.join("mdf_forge", "version.py")) as f:
    exec(f.read(), version_ns)
version = version_ns['__version__']

setup(
    name='mdf_forge',
    version=version,
    packages=['mdf_forge'],
    description='Materials Data Facility python package',
    long_description=("Forge is the Materials Data Facility Python package"
                      " to interface and leverage the MDF Data Discovery service. "
                      "Forge allows users to perform simple queries and "
                      "facilitiates moving and synthesizing results."),
    install_requires=[
        "mdf-toolbox>=0.5.0",
        "globus-sdk>=1.7.0",
        "requests>=2.18.4",
        "tqdm>=4.19.4"
    ],
    python_requires=">=3.4",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering"
    ],
    keywords=[
        "MDF",
        "Materials Data Facility",
        "materials science",
        "dft",
        "data discovery",
        "supercomputing",
        "light sources"
    ],
    license="Apache License, Version 2.0",
    url="https://github.com/materials-data-facility/forge"
)
