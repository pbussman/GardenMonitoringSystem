from setuptools import setup, find_packages

setup(
    name="garden_zero",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "RPi.GPIO",
        "paho-mqtt",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "garden-source=Zero.main:main",
        ],
    },
)
