# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quick-datasets']

package_data = \
{'': ['*']}

install_requires = \
['attrdict>=2.0.1,<3.0.0',
 'click>=7.0,<8.0',
 'loguru>=0.4.0,<0.5.0',
 'pandas>=0.25.3,<0.26.0',
 'tqdm>=4.41.1,<5.0.0']

entry_points = \
{'console_scripts': ['train = train:run']}

setup_kwargs = {
    'name': 'quick-datasets',
    'version': '0.3.0',
    'description': 'Datasets for machine learning and deep learning tasks',
    'long_description': '# datasets',
    'author': 'Soumendra Dhanee',
    'author_email': 'soumendra@gmail.com',
    'maintainer': 'Soumendra Dhanee',
    'maintainer_email': 'soumendra@gmail.com',
    'url': 'https://github.com/soumendra/quick-datasets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.5,<4.0.0',
}


setup(**setup_kwargs)
