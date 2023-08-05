# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiosqlembic', 'aiosqlembic.models']

package_data = \
{'': ['*'], 'aiosqlembic': ['sql/metadata/*', 'templates/*']}

install_requires = \
['aiosql>=3.0.0,<4.0.0',
 'alembic>=1.3.2,<2.0.0',
 'asyncpg>=0.20.1,<0.21.0',
 'jinja2>=2.11.0,<3.0.0',
 'migra>=1.0.1575954682,<2.0.0',
 'pydantic>=1.3,<2.0',
 'toml>=0.10.0,<0.11.0',
 'typer>=0.0.8,<0.0.9']

entry_points = \
{'console_scripts': ['aiosqlembic = aiosqlembic.main:app']}

setup_kwargs = {
    'name': 'aiosqlembic',
    'version': '0.1.0',
    'description': 'Migrations powered by aiosql',
    'long_description': ".. image:: https://gitlab.com/euri10/aiosqlembic/badges/master/pipeline.svg\n    :target: https://gitlab.com/euri10/aiosqlembic/-/commits/master\n    :alt: pipeline status\n.. image:: https://gitlab.com/euri10/aiosqlembic/badges/master/coverage.svg\n    :target: https://gitlab.com/euri10/aiosqlembic/-/commits/master\n    :alt: coverage report\n.. image:: https://readthedocs.org/projects/aiosqlembic/badge/?version=latest\n    :target: https://aiosqlembic.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\nReadme\n======\n\nAiosqlembic aims at running database migrations powered by the awesome `aiosql <https://github.com/nackjicholson/aiosql>`_\n\nIt currently uses the also excellent `migra <https://github.com/djrobstep/migral>`_\n\nIt is in development and likely to break\n\nInstallation\n------------\n\nRun :code:`pip install aiosqlembic`\n\nDocumentation\n-------------\n\nIt's here `here <https://aiosqlembic.readthedocs.io/en/latest/index.html>`_\n\nUsage\n-----\n\nRun :code:`aiosqlembic --help`\n",
    'author': 'euri10',
    'author_email': 'benoit.barthelet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/euri10/aiosqlembic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
