import os
import re
import typing

from setuptools import setup


def get_version(package) -> str:
    """Return package version as listed in `__version__` in `init.py`."""

    path = os.path.join(package, "__init__.py")
    version = ""
    with open(path, "r", encoding="utf8") as init_py:
        version = re.search(
            r"^__version__\s*=\s*['\"]([^'\"]*)['\"]",
            init_py.read(),
            re.MULTILINE,
        ).group(1)

    if not version:
        raise RuntimeError(f"__version__ is not set in {path}")

    return version


def get_packages(package) -> typing.List[str]:
    """Return root package and all sub-packages."""

    return [
        dirpath
        for dirpath, *_ in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


def get_long_description(filename: str = "README.rst") -> str:
    """Return the README."""

    with open(filename, "r", encoding="utf8") as readme:
        long_description = readme.read()
    return long_description


def get_requirements(filename: str = "requirements.txt") -> typing.List[str]:
    """Return the requirements."""

    requirements = []
    with open(filename, "r", encoding="utf8") as requirements_txt:
        requirements = requirements_txt.read().splitlines()
    return requirements


extra_requires = {
    "async": get_requirements("async-requirements.txt"),
}

setup(
    name="codingame",
    version=get_version("codingame"),
    url="https://github.com/takos22/codingame",
    license="MIT",
    description="Pythonic wrapper for the undocumented CodinGame API.",
    long_description=get_long_description(),
    long_description_content_type="text/x-rst",
    author="takos22",
    author_email="takos2210@gmail.com",
    packages=[
        "codingame",
        "codingame.client",
        "codingame.http",
    ],
    python_requires=">=3.6",
    install_requires=get_requirements(),
    extras_require=extra_requires,
    project_urls={
        "Documentation": "https://codingame.readthedocs.io/",
        "Issue tracker": "https://github.com/takos22/codingame/issues",
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
