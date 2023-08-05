# See LICENSE for details

#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [ 'GitPython>=2.1.11', 'PyYAML>=5.1.1', 'Click>=7.0', 'colorlog']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author='InCore Semiconductors Pvt. Ltd.',
    author_email='lavanya@incoresemi.com',
    python_requires='>=3.5',
    classifiers=[
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: BSD License",
          "Development Status :: 4 - Beta"
    ],
    description="GitLab Repository Manager",
    entry_points={
        'console_scripts': [
            'repomanager=repomanager.main:cli',
        ],
    },
    install_requires=requirements,
    license='BSD-3-Clause',
    long_description=readme + '\n\n',
    include_package_data=True,
    keywords='repomanager',
    name='repomanager',
    packages=find_packages(include=['repomanager', 'repomanager.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/incoresemi/utils/repomanager',
    version='1.0.10',
    zip_safe=False,
)
