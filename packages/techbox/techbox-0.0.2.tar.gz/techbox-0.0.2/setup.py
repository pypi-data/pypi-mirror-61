#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
from techbox import __version__ as version

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
        'gitpython',
        'fire',
        ]

setup_requirements = [
        'pytest-runner',
        ]

test_requirements = [
        'pytest>=3',
        'tox',
        ]

setup(
    author="Barak Avrahami",
    author_email='barak1345@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A toolbox packed with dependencies",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='techbox',
    name='techbox',
    packages=find_packages(include=['techbox', 'techbox.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/andecy64/techbox',
    version=version,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "techbox = techbox.cli:ep",
            ]
        },
    )
