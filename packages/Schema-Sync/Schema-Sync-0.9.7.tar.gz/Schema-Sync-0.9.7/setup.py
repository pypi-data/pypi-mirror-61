#!/usr/bin/env python
# coding:utf-8

from setuptools import setup

setup(
    name='Schema-Sync',
    version='0.9.7',
    description='A MySQL Schema Synchronization Utility',
    author='Mitch Matuson, Mustafa Ozgur',
    url='https://github.com/hhyo/SchemaSync',
    packages=['schemasync'],
    install_requires=['Schema-Object >= 0.5.10'],
    entry_points={
        'console_scripts': [
            'schemasync = schemasync.schemasync:main',
        ]
    },

    keywords=["MySQL", "database", "schema", "migration", "SQL"],

    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
    ],

    long_description="""\
      Schema Sync will generate the SQL necessary to migrate the schema of a source database
      to a target database (patch script), as well as a the SQL necessary to undo the changes
      after you apply them (revert script).
      """
)
