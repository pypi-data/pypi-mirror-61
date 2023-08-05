# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stail']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'colorama>=0.4.3,<0.5.0', 'pyfiglet>=0.8.post1,<0.9']

entry_points = \
{'console_scripts': ['stail = stail:main']}

setup_kwargs = {
    'name': 'stail',
    'version': '0.1.1',
    'description': 'Step Function tailing CLI tool',
    'long_description': '',
    'author': 'Iman Kamyabi',
    'author_email': 'contact@imankamyabi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/imankamyabi/stail',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
