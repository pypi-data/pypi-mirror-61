# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'pyborg'}

packages = \
['pyborg', 'pyborg.mod', 'pyborg.util']

package_data = \
{'': ['*']}

modules = \
['pyborg_entrypoint']
install_requires = \
['Mastodon.py>=1.4,<2.0',
 'PyTumblr>=0.1.0,<0.2.0',
 'aiohttp',
 'arrow>=0.15,<0.16',
 'attrs>=19.1,<20.0',
 'bottle>=0.12.17,<0.13.0',
 'click>=7.0,<8.0',
 'discord.py>=1.2.3,<2.0.0',
 'filelock>=3.0,<4.0',
 'humanize>=0.5.1,<0.6.0',
 'irc>=18,<19',
 'lxml>=4.3,<5.0',
 'matplotlib>=3.1.2,<4.0.0',
 'networkx>=2.4,<3.0',
 'praw>=6.3,<7.0',
 'prompt_toolkit>=3,<4',
 'requests',
 'statsd>=3.3,<4.0',
 'tabulate>=0.8.5,<0.9.0',
 'toml>=0.10.0,<0.11.0',
 'tox>=3.13.2,<4.0.0',
 'tweepy>=3.7,<4.0',
 'typing_extensions>=3.7.4,<4.0.0',
 'venusian>=3,<4']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.3.0,<2.0.0'],
 'nlp': ['nltk>=3.4.5,<4.0.0'],
 'subtitles': ['aeidon>=1.7.0,<2.0.0']}

entry_points = \
{'console_scripts': ['pyborg = pyborg_entrypoint:cli_base']}

setup_kwargs = {
    'name': 'pyborg',
    'version': '2.0.0a7',
    'description': 'Markov chain (chat) bot for a suite for modern services (discord, irc, twitter, mastodon, file, linein)',
    'long_description': '\ufeffPyborg is a markov chain bot for many protocols (Discord, IRC, Twitter, etc.) that generates replies based on messages and it\'s database.\n\n[![PyPI](https://img.shields.io/pypi/v/pyborg)](https://pypi.org/project/pyborg/)\n[![codecov status](https://codecov.io/gh/jrabbit/pyborg-1up/branch/master/graph/badge.svg)](https://codecov.io/gh/jrabbit/pyborg-1up)\n[![CI status](https://travis-ci.org/jrabbit/pyborg-1up.svg)](https://travis-ci.org/jrabbit/pyborg-1up)\n[![Documentation Status](https://readthedocs.org/projects/pyborg/badge/?version=latest)](https://pyborg.readthedocs.io/en/latest/?badge=latest)\n\nInstall\n--------\nWe\'re on the cheeseshop! Yay!\n\n`pip install pyborg`\n\nIf you want the latest git via pip you\'ll need to install it via [poetry.](https://poetry.eustace.io/docs/)\n\nTesting releases can be found via:\n\n`pip install --pre pyborg`\n\n\nNote that we\'re using Python 3.6+ (for fancy type declarations).\n\nPython 2 support was [dropped with](https://pythonclock.org/) the release of pyborg 2.0.\n\n\nThere are two extras "nlp" and "subtitles". e.g. `pip install pyborg[nlp]`\n\n\nBasic Usage\n-----------\n\n`pyborg` is our new unified pyborg command line interface.\n\n\nDocumentation\n-------------\n\n[Docs can be found on RTD.](http://pyborg.readthedocs.io/en/latest/)\n\n\nNotes\n-----\n\nPyborg is skipping version 1.3; this was used for a transitory database/"brain" restructuring that was underwhelming. \n\nAncient original tarballs were hosted at Gna! which is now gone. [Thankfully Internet Archive has a copy!](https://web.archive.org/web/20170225141934/http://download.gna.org/pyborg/) \n\nPyborg was originally developed by Tom Morton and Sébastien Dailly.\n\n\nSuggested NLTK data\n-------------------\n\nPyborg can use nltk tagging and tokenizing when installed and configured. Tagging requires `averaged_perceptron_tagger` and tokenization requires `punkt`.\n',
    'author': 'Jack Laxson',
    'author_email': 'jackjrabbit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jrabbit/pyborg-1up',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
