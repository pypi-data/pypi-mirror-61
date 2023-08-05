# -*- coding: utf-8 -*-

import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="frozenleaves",
    version="0.0.2",
    py_modules=['demo', 'hello'],
    author="frozenleaves",
    author_email="914814442@qq.com",
    description="A test package",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="http://frozenleaves.cn",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)