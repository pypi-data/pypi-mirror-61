import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="x-deep",
  version="0.0.9",
  author="DATA LAB at Texas A&M University",
  author_email="hu@cse.tamu.edu",
  description="XDeep is an open-source package for Interpretable Machine Learning.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/datamllab/xdeep",
  packages=setuptools.find_packages(),
  install_requires=[
   'anchor-exp',
   'shap',
   'torch',
   'torchvision'
  ],
  classifiers=[
  "Programming Language :: Python :: 3.6",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)