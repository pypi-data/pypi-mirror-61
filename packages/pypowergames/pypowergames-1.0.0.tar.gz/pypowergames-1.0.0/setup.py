from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="pypowergames",
    version="1.0.0",
    description="A Python package to play tic tac toe",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/tirth-2001/ttt.git",
    author="PyPower Projects",
    author_email="projectspypower@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pypowergames"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pypowergames=lkj.call:tictactoe",
        ]
   
    },
)