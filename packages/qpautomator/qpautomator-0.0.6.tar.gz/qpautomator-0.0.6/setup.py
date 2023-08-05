#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


requires = [
    "urllib3>=1.7.1",
	"requests==2.22.0",
]

test_requires = [

]

setup(
    name='qpautomator',
    version='0.0.6',
    description='automator on QPython3L',
    long_description='automator on QPython3L',
    author='mrsha',
    author_email='mrsha1195@163.com',
    url='https://github.com/qpautomator/xxxL',
    download_url='https://github.com/qpautomator/xxxL',
    keywords=[
        'testing', 'android', 'qpautomator'
    ],
    install_requires=requires,
    tests_require=test_requires,
    test_suite="nose.collector",
    packages=['qpautomator'],
    package_data={
        'qpautomator': [
        ]
    },
    include_package_data=True,
    license='MIT',
    platforms='any',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing'
    )
)
