from setuptools import setup, find_packages
from JBTools import __version__
import io 

with io.open("README.md", mode='r', encoding="utf-8") as f:
    readme = f.read()

setup(
    name="JBTools",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    description="My personal packages",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=[
        "pickleshare==0.7.5",
        "numpy==1.17.2",
        "Keras==2.3.1",
        "Keras-Applications==1.0.8",
        "Keras-Preprocessing==1.1.0",
        "tensorboard==2.0.0",
        "tensorflow==2.1.0",
        "tensorflow-estimator==2.0.0"
    ],
    url="https://github.com/jbtanguy/JBTools.git",
    author='Jean-Baptiste Tanguy',
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    license="MIT",
)
