# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nyaacli', 'nyaacli.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'colorama>=0.4.1,<0.5.0',
 'feedparser>=5.2,<6.0',
 'guessit>=3.0,<4.0',
 'questionary>=1.5.1,<2.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['nyaa = nyaacli.cli:main', 'nyaa-cli = nyaacli.cli:main']}

setup_kwargs = {
    'name': 'nyaacli',
    'version': '0.1.6',
    'description': 'A CLI for downloading Anime from https://nyaa.si',
    'long_description': '# Nyaa-cli [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![nyaacli](https://img.shields.io/pypi/pyversions/nyaacli)](https://pypi.org/project/nyaacli/) [![nyaa.si](https://img.shields.io/badge/-nyaa.si-green)](https://nyaa.si)\n\n\nA CLI for downloading Anime from https://nyaa.si making use of their RSS Feed and [python-libtorrent](https://github.com/arvidn/libtorrent/blob/RC_1_2/docs/python_binding.rst)\n\n[CHANGELOG](CHANGELOG.md)\n\n---\n\n![image](https://user-images.githubusercontent.com/37747572/69002323-bb2ea100-08cb-11ea-9b47-20bd9870c8c0.png)\n\n---\n\n![image](https://user-images.githubusercontent.com/37747572/69002293-33e12d80-08cb-11ea-842e-02947726185d.png)\n\n---\n\n![image](https://user-images.githubusercontent.com/37747572/69002363-ad2d5000-08cc-11ea-9360-76bf1598512d.png)\n\n---\n\n## Installing\n\n- `python3 -m pip install nyaacli --user`\n  - *Note:* python-libtorrent will still need to be downloaded separately as shown below\n\n- This Program depends on python3-libtorrent, which can be installed using Apt with `sudo apt install python3-libtorrent` or can be built from source here: [python-libtorrent](https://github.com/arvidn/libtorrent/blob/RC_1_2/docs/python_binding.rst)\n\n---\n\n## Usage\n\n- **Help:** `nyaa --help` or `nyaa-cli --help`\n\n- `nyaa "Anime Name" <Episode Number (Optional)> -o <Output Folder (Default: ~/Videos/Anime)>`\n  - **Example:**\n    ```bash\n    # Downloading Episode 14 of \'Steins;gate\' to \'~/Anime/Steins;Gate\'\n    nyaa "Steins;Gate" 14 -o ~/Anime/Steins\\;Gate\n    ```\n  - Then select the entry you want to Download\n',
    'author': 'John Victor',
    'author_email': 'johnvictorfs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/johnvictorfs/nyaa-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
