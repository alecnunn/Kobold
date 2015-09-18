#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='Kobold',
    version='0.1.0',
    description="Kobold is a minimal framework used to design distributed tasks and workers, using RabbitMQ as its delivery queue.",
    long_description=readme + '\n\n' + history,
    author="Alec Nunn",
    author_email='alec.nunn@gmail.com',
    url='https://github.com/alecnunn/Kobold',
    packages=[
        'Kobold',
    ],
    package_dir={'Kobold':
                 'Kobold'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='Kobold',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
