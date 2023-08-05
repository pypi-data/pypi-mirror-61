# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lgbsttracker',
 'lgbsttracker.entities',
 'lgbsttracker.services',
 'lgbsttracker.services.store',
 'lgbsttracker.services.store._experiment_registry',
 'lgbsttracker.store',
 'lgbsttracker.store.db',
 'lgbsttracker.store.db_migrations',
 'lgbsttracker.store.db_migrations.versions',
 'lgbsttracker.store.experiment',
 'lgbsttracker.store.experiment.dbmodels',
 'lgbsttracker.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp',
 'alembic>=1.3.3,<2.0.0',
 'asynctest>=0.13.0,<0.14.0',
 'autoflake>=1.3.1,<2.0.0',
 'click',
 'entrypoints',
 'fastapi>=0.48.0,<0.49.0',
 'google-api',
 'google-api-core',
 'grpcio',
 'grpcio-tools',
 'lock>=2018.3.25,<2019.0.0',
 'numpy',
 'pandas>=0.25.3,<0.26.0',
 'prometheus-client',
 'protoc_gen_swagger',
 'psycopg2',
 'pydantic>=1.4,<2.0',
 'pytest-aiohttp>=0.3.0,<0.4.0',
 'pytest-asyncio>=0.10.0,<0.11.0',
 'python-dateutil',
 'querystring_parser',
 'requests',
 'sqlalchemy',
 'sqlalchemy-utils']

entry_points = \
{'console_scripts': ['lgbsttracker = lgbsttracker.cli:cli']}

setup_kwargs = {
    'name': 'lgbsttracker',
    'version': '0.0.2',
    'description': '0.0.2',
    'long_description': '<H1>lgbsttracker</H1>\n<p align="center">\n<img src="https://img.shields.io/github/last-commit/py4mac/lgbsttracker.svg">\n<a href="https://github.com/py4mac/" target="_blank">\n    <img src="https://github.com/py4mac/lgbsttracker/workflows/Test/badge.svg" alt="Test">\n</a>\n<a href="https://codecov.io/gh/py4mac/lgbsttracker" target="_blank">\n    <img src="https://codecov.io/gh/py4mac/lgbsttracker/branch/master/graph/badge.svg" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/lgbsttracker" target="_blank">\n    <img src="https://badge.fury.io/py/lgbsttracker.svg" alt="Package version">\n</a>\n</p>\n\n---\n\n**Trello Plan**: <a href="https://trello.com/b/lGICXLqL/lgbsttracker" target="_blank">https://trello.com/b/lGICXLqL/lgbsttracker</a>\n\n**Documentation**: <a href="https://py4mac.github.io/lgbsttracker" target="_blank">https://py4mac.github.io/lgbsttracker</a>\n\n**Source Code**: <a href="https://github.com/py4mac/lgbsttracker" target="_blank">https://github.com/py4mac/lgbsttracker</a>\n\n---\n\n## Requirements\n\nPython 3.6+\n\n\n## Installation\n\n```bash\npip install lgbsttracker\n```\n\n## Example\n\n### Use it\n\n\n(Work in progress)\n\n## Environment variables\n\n| Variable Name |  Description | Default value |\n| --- | --- | --- |\n| EXPERIMENT_STORAGE_URI | DB Experiment Storage URI | Mandatory: to be set by the user before using library |\n| SQL_DB_THREAD_POOL_EXECUTOR_SIZE | Thread pool size | 100 |\n| MIN_CONNECTION_POOL_SIZE | Minimum pool size connection | 10 |\n| MAX_CONNECTION_POOL_SIZE | Maxiumum pool size connection | 20 |\n| CONNECTION_POOL_RECYCLE_TIME | Pool connection recycle time | 30 |\n\n## References\n\n* https://github.com/mlflow/mlflow/\n* https://github.com/undera/pylgbst\n* https://github.com/tiangolo/fastapi\n* https://github.com/aalhour/cookiecutter-aiohttp-sqlalchemy/\n\n## License\n\nThis project is licensed under the terms of the MIT license.',
    'author': 'Py4mac',
    'author_email': 'boisbu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/py4mac/lgbsttracker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
