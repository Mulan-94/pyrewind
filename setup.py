import os
from setuptools import setup, find_packages


build_root = os.path.dirname(__file__)

with open(os.path.join(build_root, 'README.rst')) as fh:
    long_description = fh.read()

setup(
    name="pyrewind",
    version="0.0.1",
    author="L. A. L. Andati",
    author_email="andatilexy@gmail.com",
    description="Rewind python packages to versions before a certain date",
    license="MIT",
    long_description=long_description,
    url="",
    packages=['pyrewind'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires=">=3.6",

    # package requirements
    install_requires=[],
    project_urls={
        "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code": "https://code.example.com/HelloWorld/",
    },
    scripts=[os.path.join("pyrewind", "bin", i)
             for i in os.listdir("pyrewind/bin/")]
)
