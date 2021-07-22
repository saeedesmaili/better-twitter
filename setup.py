from setuptools import setup, find_packages
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="better-twitter",
    version="0.0.20",
    description="A python package to block and mute fake and toxic twitter accounts in an automated and easy way.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saeedesmaili/better-twitter",
    author="Saeed Esmaili",
    author_email="me@saeedesmaili.com",
    license="MIT license",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    entry_points='''
        [console_scripts]
        better-twitter=better_twitter.main:cursive_command
    ''',
    keywords="twitter",
    packages=["better_twitter"],
    include_package_data=True,
    install_requires=["pandas", "python-twitter", "pendulum"]
)
