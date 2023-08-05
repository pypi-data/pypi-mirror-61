#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import warnings
from setuptools import setup, find_packages, Command
from setuptools.command.install import install as _install

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'requests',
    'Click'
]

setup_requirements = [
    'pytest-runner'
]

test_requirements = [
    'pytest'
]

class install(_install):
    def run(self):
        _install.do_egg_install(self)

class FakeBdist(Command):
    """Fake bdist wheel class for ignoring bdist_wheel build
    """

    user_options = [(
        "dist-dir=",
        "d",
        "directory to put final built distributions in [default: dist]"
    ), (
        "python-tag=",
        None,
        "Python tag (cp32|cp33|cpNN) for abi3 wheel tag (default:false)"
    )]

    def initialize_options(self):
        self.dist_dir = None
        self.python_tag = None

    def finalize_options(self):
        pass

    def run(self):
        warnings.warn(
            "{name}{version} does not support building wheels".format(
                name=about["__title__"],
                version=about["__version__"]
            )
        )

setup(
    name='split-downloader',
    version='0.2.6',
    description="Parallel downloader",
    long_description=readme,
    author="Joe Paul",
    author_email='joeirimpan@gmail.com',
    url='https://github.com/joeirimpan/pyparallel',
    packages=find_packages(include=['pyparallel']),
    include_package_data=True,
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        download=pyparallel:cli
    ''',
    license="MIT license",
    zip_safe=False,
    keywords='pyparallel',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    long_description_content_type='text/markdown',
    setup_requires=setup_requirements,
    cmdclass={"bdist_wheel": FakeBdist}
)
