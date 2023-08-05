# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py17track']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'async-timeout>=3.0.1,<4.0.0',
 'attrs>=19.3.0,<20.0.0']

setup_kwargs = {
    'name': 'py17track',
    'version': '2.2.5',
    'description': 'A Simple Python API for 17track.net',
    'long_description': '# 📦 py17track: A Simple Python API for 17track.net\n\n[![CI](https://github.com/bachya/py17track/workflows/CI/badge.svg)](https://github.com/bachya/py17track/actions)\n[![PyPi](https://img.shields.io/pypi/v/py17track.svg)](https://pypi.python.org/pypi/py17track)\n[![Version](https://img.shields.io/pypi/pyversions/py17track.svg)](https://pypi.python.org/pypi/py17track)\n[![License](https://img.shields.io/pypi/l/py17track.svg)](https://github.com/bachya/py17track/blob/master/LICENSE)\n[![Code Coverage](https://codecov.io/gh/bachya/py17track/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/py17track)\n[![Maintainability](https://api.codeclimate.com/v1/badges/af60d65b69d416136fc9/maintainability)](https://codeclimate.com/github/bachya/py17track/maintainability)\n[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)\n\n`py17track` is a simple Python library to track packages in\n[17track.net](http://www.17track.net/) accounts.\n\nSince this is uses an unofficial API, there\'s no guarantee that 17track.net\nwill provide every field for every package, all the time. Additionally, this\nAPI may stop working at any moment.\n\n# Python Versions\n\n`py17track` is currently supported on:\n\n* Python 3.6\n* Python 3.7\n* Python 3.8\n\n# Installation\n\n```python\npip install py17track\n```\n\n# Usage\n\n`py17track` starts within an\n[aiohttp](https://aiohttp.readthedocs.io/en/stable/) `ClientSession`:\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\n\nfrom py17track import Client\n\n\nasync def main() -> None:\n    """Create the aiohttp session and run the example."""\n    async with ClientSession() as websession:\n      # YOUR CODE HERE\n\n\nasyncio.get_event_loop().run_until_complete(main())\n```\n\nCreate a client then get to it:\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\n\nfrom py17track import Client\n\n\nasync def main() -> None:\n    """Create the aiohttp session and run the example."""\n    async with ClientSession() as websession:\n      client = Client(websession)\n\n      # Login to 17track.net:\n      await client.profile.login(\'<EMAIL>\', \'<PASSWORD>\')\n\n      # Get the account ID:\n      client.profile.account_id\n      # >>> 1234567890987654321\n\n      # Get a summary of the user\'s packages:\n      summary = await client.profile.summary()\n      # >>> {\'In Transit\': 3, \'Expired\': 3, ... }\n\n      # Get all packages associated with a user\'s account:\n      packages = await client.profile.packages()\n      # >>> [py17track.package.Package(..), ...]\n\n\nasyncio.get_event_loop().run_until_complete(main())\n```\n\nEach `Package` object has the following info:\n\n* `destination_country`: the country the package was shipped to\n* `friendly_name`: the human-friendly name of the package\n* `info`: a text description of the latest status\n* `location`: the current location (if known)\n* `origin_country`: the country the package was shipped from\n* `package_type`: the type of package (if known)\n* `status`: the overall package status ("In Transit", "Delivered", etc.)\n* `tracking_info_language`: the language of the tracking info\n* `tracking_number`: the all-important tracking number\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/bachya/py17track/issues)\n  or [initiate a discussion on one](https://github.com/bachya/py17track/issues/new).\n2. [Fork the repository](https://github.com/bachya/py17track/fork).\n3. Install the dev environment: `make init`.\n4. Enter the virtual environment: `source .venv/bin/activate`\n5. Code your new feature or bug fix.\n6. Write a test that covers your new functionality.\n7. Update `README.md` with any new documentation.\n8. Run tests and ensure 100% code coverage: `make coverage`\n9. Ensure you have no linting errors: `make lint`\n10. Ensure you have no typed your code correctly: `make typing`\n11. Add yourself to `AUTHORS.md`.\n12. Submit a pull request!\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bachya/py17track',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
