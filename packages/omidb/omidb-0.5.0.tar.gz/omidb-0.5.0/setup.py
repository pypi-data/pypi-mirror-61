# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omidb', 'omidb.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'loguru>=0.4.1,<0.5.0',
 'matplotlib>=3.1.2,<4.0.0',
 'pydicom>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['omidb = omidb:commands.main']}

setup_kwargs = {
    'name': 'omidb',
    'version': '0.5.0',
    'description': 'Python package and CLI for The OPTIMAM Mammography Image Database (OMI-DB)',
    'long_description': None,
    'author': 'Dominic Ward',
    'author_email': 'dominic.ward1@nhs.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
