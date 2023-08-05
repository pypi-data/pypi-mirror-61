# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybreak']

package_data = \
{'': ['*']}

install_requires = \
['prompt-toolkit>=3.0,<4.0']

extras_require = \
{':python_version == "3.6"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['pybreak = pybreak.run:run']}

setup_kwargs = {
    'name': 'pybreak',
    'version': '0.2.0.dev0',
    'description': 'pybreak',
    'long_description': None,
    'author': 'Darren Burns',
    'author_email': 'darren.burns@fanduel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
