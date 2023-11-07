#!/usr/bin/env python

from setuptools import setup
import json

with open('./version.json', 'r') as f:
    verinfo = json.load(f)

setup(name=verinfo['pname'],
      version=verinfo['version'],
      description='State manager for nixos/home-manager',
      install_requires=[
          'fastbencode',
          'schema',
      ],
      packages=['statemanager'],
      scripts=['statemountd', 'mkrequest'],
     )
