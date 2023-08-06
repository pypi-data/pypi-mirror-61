import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="atalaya",
    version="0.1.5.4",
    python_requires=">=3.6",
    description="Atalaya is a logger for pytorch.",
    url="https://github.com/jacr13/Atalaya",
    author="Joao Ramos",
    author_email="joao.candido@etu.unige.ch",
    license="MIT",
    packages=find_packages(),
    install_requires=["numpy", "torch", "visdom>=0.1.8.8", "tensorboardX==1.4"],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    zip_safe=False,
)
