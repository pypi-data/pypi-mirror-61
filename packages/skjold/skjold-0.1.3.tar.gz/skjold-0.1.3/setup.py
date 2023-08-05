# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['skjold', 'skjold.sources']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'poetry-semver>=0.1.0,<0.2.0',
 'pyyaml>=5.3,<6.0',
 'requests>=2.22.0,<3.0.0',
 'tomlkit>=0.5.8,<0.6.0']

entry_points = \
{'console_scripts': ['skjold = skjold.cli:cli']}

setup_kwargs = {
    'name': 'skjold',
    'version': '0.1.3',
    'description': 'Security audit Python project dependencies against security advisory databases.',
    'long_description': '![](https://img.shields.io/pypi/v/skjold?color=black&label=PyPI&style=flat-square)\n![](https://img.shields.io/pypi/status/skjold?color=black&style=flat-square)\n![](https://img.shields.io/pypi/pyversions/skjold?color=black&logo=python&logoColor=white&style=flat-square)\n![](https://img.shields.io/pypi/l/skjold?color=black&label=License&style=flat-square)\n\n```\n        .         .    .      Skjold /skjɔl/\n    ,-. | , . ,-. |  ,-|\n    `-. |<  | | | |  | |      Security audit python project dependencies\n    `-\' \' ` | `-\' `\' `-´      against several security advisory databases.\n           `\'\n```\n\n## Introduction\nIt currently supports fetching advisories from the following sources:\n\n- [GitHub Advisory Database](https://github.com/advisories)\n- [PyUP.io safety-db](https://github.com/pyupio/safety-db)\n- [GitLab gemnasium-db](https://gitlab.com/gitlab-org/security-products/gemnasium-db)\n\nUnless configured explicitly `skjold` will run the given packages against all of them. There is (currently) no de-duplication meaning that using all of them could result in _a lot_ of duplicates. Source can be added disabled by setting `sources` list (see [Configuration](#configuration)).\n\n## Motivation\nSkjold was initially created for myself to replace `safety`. Which appears to no longer receive monthly updates (see [pyupio/safety-db #2282](https://github.com/pyupio/safety-db/issues/2282)). I wanted something I can run locally and use for my local or private projects/scripts.\n\nI currently also use it during CI builds and before deploying/publishing containers or packages.\n\n## Installation\n`skjold` can be installed from either [PyPI](https://pypi.org/project/skjold/) or directly from [Github](https://github.com/twu/skjold) using `pip`:\n\n```sh\npip install git+https://github.com/twu/skjold.git@vX.X.X  # Install from Github\npip install skjold                                        # Install from PyPI\n```\n\nThis should provide a script named `skjold` that can then be invoked. See [Usage](#usage).\n\n## Usage\n```sh\n$ pip freeze | skjold -v audit --source gemnasium -\n```\n\nWhen running `audit` one can either provide a path to a _frozen_ `requirements.txt`, a `poetry.lock` or a `Pipfile.lock` file. Alternatively, dependencies can also be passed in via `stdin`  (formatted as `package==version`).\n\n`skjold` will maintain a local cache (under `cache_dir`) that will expire automatically after `cache_expires` has passed. The `cache_dir` and `cache_expires` can be adjusted by setting them in  `tools.skjold` section of the projects `pyproject.toml` (see [Configuration](#configuration) for more details). The `cache_dir`will be created automatically, and by default unless otherwise specified will be located under `$HOME/.skjold/cache`.\n\nFor further options please read `skjold --help` and/or `skjold audit --help`.\n\n### Examples\n\nAll examples involving `github` assume that `SKJOLD_GITHUB_API_TOKEN` is already set (see [Github](#github)).\n\n```sh\n# Using pip freeze. Checking against GitHub only.\n$ pip freeze | skjold audit -s github -\n\n# Be verbose. Read directly from supported formats.\n$ skjold -v audit requirements.txt\n$ skjold -v audit poetry.lock\n$ skjold -v audit Pipenv.lock\n\n# Using poetry.\n$ poetry export -f requirements.txt | skjold audit -s github -s gemnasium -s pyup -\n\n# Using poetry, format output as json and pass it on to jq for additional filtering.\n$ poetry export -f requirements.txt | skjold audit -o json -s github - | jq \'.[0]\'\n\n# Using Pipenv, checking against Github\n$ pipenv run pip freeze | skjold audit -s github -\n\n# Checking a single package via stdin against Github and format findings as json.\necho "urllib3==1.23" | skjold audit -o json -r -s github -\n[\n  {\n    "severity": "HIGH",\n    "name": "urllib3",\n    "version": "1.23",\n    "versions": "<1.24.2",\n    "source": "github",\n    "summary": "High severity vulnerability that affects urllib3",\n    "references": [\n      "https://nvd.nist.gov/vuln/detail/CVE-2019-11324"\n    ],\n    "url": "https://github.com/advisories/GHSA-mh33-7rrq-662w"\n  }\n]\n```\n\n### Configuration\n\n`skjold` can read its configuration from the `tools.skjold` section of a projects  `pyproject.toml`. Arguments specified via the command-line should take precedence over any configured or default value.\n\n```toml\n[tool.skjold]\nsources = ["github", "pyup", "gemnasium"]  # Sources to check against.\nreport-only = true                         # Report only, always exit with zero.\nreport-format = \'json\'                     # Output findings as `json`. Default is \'cli\'.\ncache_dir = \'.skylt_cache\'                 # Cache location (default: `~/.skjold/cache`).\ncache_expires = 86400                      # Cache max. age.\nverbose = true                             # Be verbose.\n```\n\nTo take a look at the current configuration / defaults run:\n```shell\n$ skjold config\nsources: [\'pyup\', \'github\', \'gemnasium\']\nreport_only: True\nreport_format: json\nverbose: False\ncache_dir: .skjold_cache\ncache_expires: 86400\n```\n\n#### Github\n\nFor the `github` source to work you\'ll need to provide a Github API Token via an `ENV` variable named `SKJOLD_GITHUB_API_TOKEN`. You can [create a new Github Access Token here](https://github.com/settings/tokens). You *do not* have to give it *any* permissions as it is only required to query the [GitHub GraphQL API v4](https://developer.github.com/v4/) API.\n\n### Version Control Integration\nTo use `skjold` with the excellent [pre-commit](https://pre-commit.com/) framework add the following to the projects `.pre-commit-config.yaml` after [installation](https://pre-commit.com/#install).\n\n```yaml\nrepos:\n  - repo: https://github.com/twu/skjold\n    rev: vX.X.X\n    hooks:\n    - id: skjold\n      name: "skjold: Auditing dependencies for known vulnerabilities."\n      entry: skjold audit\n      language: python\n      language_version: python3\n      files: ^(poetry\\.lock|Pipfile\\.lock|requirements.*\\.txt)$\n```\n\nAfter running `pre-commit install` the hook should be good to go. To configure `skjold` in this scenario I recommend to add the entire configuration to the projects `pyproject.toml` instead of manipulating the hook `args`. See this projects [pyproject.toml](./pyproject.toml) for an example.\n\n## Contributing\nPull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n',
    'author': 'Thomas Wurmitzer',
    'author_email': 't.wurmitzer+github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/twu/skjold',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
