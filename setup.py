import os
import re
import json
from setuptools import setup


kwargs = {
        'name': 'jelly',
        'version': '0',
        'description': '',
        'packages': ['jelly'],
        'zip_safe': False,
        'scripts': ['scripts/cf'],
        }

setup(**kwargs)



