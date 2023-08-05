# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_dns',
 'async_dns.core',
 'async_dns.core.config',
 'async_dns.resolver',
 'async_dns.server']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'async-dns',
    'version': '1.0.7',
    'description': 'Asynchronous DNS client and server',
    'long_description': None,
    'author': 'Gerald',
    'author_email': 'i@gerald.top',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gera2ld/async_dns',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
