# -*- coding:utf-8 -*-

from pathlib import Path

from setuptools import find_packages, setup

from emgen import __version__

setup(
    name="emgen",
    version=__version__,
    description="Generate random email addresses",
    long_description=Path("./README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Eric Tedor",
    author_email="eric@tedor.org",
    url="https://github.com/etedor/emgen",
    download_url="https://github.com/etedor/emgen",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: Email",
        "Topic :: Utilities",
    ],
    license="MIT",
    keywords="email",
    platforms=["any"],
    include_package_data=True,
    entry_points={"console_scripts": ["emgen=emgen.cli:main"]},
    install_requires=["email_validator", "pyperclip"],
)
