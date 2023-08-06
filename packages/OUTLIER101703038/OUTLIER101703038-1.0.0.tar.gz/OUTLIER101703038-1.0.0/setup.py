from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="OUTLIER101703038",
    version="1.0.0",
    description="A Python package for outlier detection and removal.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/kiliumnatta/Outlier",
    author="Aditya Tomar",
    author_email="aditya65921@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["OUTLIER101703038"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "OUTLIER101703038=OUTLIER101703038.Outlier:main",
        ]
    },
)