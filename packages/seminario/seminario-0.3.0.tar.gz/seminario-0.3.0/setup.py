# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seminario', 'seminario.config', 'seminario.utils']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.0,<2.0.0', 'pdfkit>=0.6.1,<0.7.0', 'wkhtmltopdf>=0.2,<0.3']

setup_kwargs = {
    'name': 'seminario',
    'version': '0.3.0',
    'description': 'Python package for seminar organization.',
    'long_description': None,
    'author': 'Shota Imaki',
    'author_email': 'shota.imaki@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
