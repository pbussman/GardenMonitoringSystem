# setup.py

from setuptools import setup, find_packages

setup(
    name="garden_zero",
    version="0.1.0",
    description="Raspberry Pi Zero 2 W source/pump controller for GardenMonitoringSystem",
    author="Paul Bussman",
    license="MIT",
    packages=find_packages(include=["Zero", "Zero.*"]),
    install_requires=[
        "RPi.GPIO>=0.7.0",
        "paho-mqtt>=1.6.1",
        "PyYAML>=6.0"
    ],
    entry_points={
        "console_scripts": [
            "garden-zero-source=Zero.main:main"
        ]
    },
    package_data={
        "Zero": ["config.yaml.example"]
    },
    include_package_data=True,
    python_requires=">=3.7"
)
