import os

import versioneer

versioneer.VCS = 'git'
versioneer.versionfile_source = 'deployer/_version.py'
versioneer.versionfile_build = 'deployer/_version.py'
versioneer.tag_prefix = '' # tags are like 1.2.0
versioneer.parentdir_prefix = 'deployer-' # dirname like 'myproject-1.2.0'

from setuptools import setup, find_packages

setup(
    name="docker-deployer",
    version=versioneer.get_version(),
    description="A Fabric framework for Docker deployment based on Docker-Compose.",
    long_description=open('README.rst').read(),
    author="Remi Barraquand",
    author_email="dev@remibarraquand.com",
    url="https://github.com/barraq/docker-deployer",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Clustering',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='LICENSE', requires=['fabric', 'configparser'],
    cmdclass=versioneer.get_cmdclass()
)