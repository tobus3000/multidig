"""setup.py for pip"""
# coding: utf-8
from os import path, system
import sys
import re
import unittest
from setuptools import setup, find_packages

PACKAGE = "multidig"

def multidig_test_suite():
    """Load and return the unit tests as a test suite."""
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(
        "tests",
        pattern="test_*.py"
    )
    return test_suite

def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    
    :param PACKAGE: The python package name.
    :type PACKAGE: str
    :return: Version as stored in `__version__` of `__init__.py`.
    :rtype: str
    """
    init_py = open(
        path.join(package, "__init__.py"),
        encoding = "utf-8"
    ).read()
    v = re.search(
        "^__version__ = ['\"]([^'\"]+)['\"]",
        init_py,
        re.MULTILINE
    )
    if v:
        return v.group(1)
    return "n/a"

def get_author(package):
    """
    Return package author as listed in `__author__` inside `__init__.py`.

    :param PACKAGE: The python package name.
    :type PACKAGE: str
    :return: Author as stored in `__author__` of `__init__.py`.
    :rtype: str
    """
    init_py = open(
        path.join(package, "__init__.py"),
        encoding = "utf-8"
    ).read()
    author = re.search(
        "^__author__ = ['\"]([^'\"]+)['\"]",
        init_py,
        re.MULTILINE
    )
    if author:
        return author.group(1)
    return "n/a"

def get_email(package):
    """
    Return package email as listed in `__email__` inside `__init__.py`.

    :param PACKAGE: The python package name.
    :type PACKAGE: str
    :return: Email address as stored in `__author__` of `__init__.py`.
    :rtype: str
    """
    init_py = open(
        path.join(package, "__init__.py"),
        encoding = "utf-8"
    ).read()
    email = re.search(
        "^__email__ = ['\"]([^'\"]+)['\"]",
        init_py,
        re.MULTILINE
    )
    if email:
        return email.group(1)
    return "n/a"

if sys.argv[-1] == "publish":
    system("python setup.py sdist")
    version = get_version(PACKAGE)
    print("You probably want to also tag the version now:")
    print(f"  git tag -a {version} -m 'version {version}'")
    print("  git push --tags")
    sys.exit()

here = path.abspath(path.dirname(__file__))

# Get long description from README.md.
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name = PACKAGE,
    version = get_version(PACKAGE),
    author = get_author(PACKAGE),
    author_email = get_email(PACKAGE),
    description = "Universal DNS lookup client.",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="tbd.git", #TODO: Path to GitHub repo
    packages=find_packages(
        exclude=[
            "ez_setup",
            "examples",
            "tests"
        ]
    ),
    keywords = "DNS Dig DoH DoT Query name resolution",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: GUI",
        "Intented Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    entry_points = {
        "console_scripts": [
            "multidig = multidig.app:main"
        ]
    },
    install_requires=[],
    include_package_data = True,
    zip_safe = False,
    test_suite = "setup.multidig_test_suite"
)
