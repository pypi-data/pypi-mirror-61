# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ratus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ratus',
    'version': '0.0.1',
    'description': 'Simple expression language.',
    'long_description': None,
    'author': 'Nick Spain',
    'author_email': 'nicholas.spain96@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
