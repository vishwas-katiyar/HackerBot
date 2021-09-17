import setuptools
with open("README.md", "r") as fh:
    long_description = fh. read()
setuptools.setup(
name="HackerBot",
version="0.0.1",
author="HackerBot",
author_email="honeykatiyar1436@gmail.com",
description="A small chatbot library",
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/vishwas-katiyar/HackerBot",
packages=setuptools.find_packages(),
classifiers=[
"Programming Language :: Python : : 3",
"License :: OSI Approved : : MIT License",
"Operating System : : OS Independent",
],
python_requires='>=3.6',
)
