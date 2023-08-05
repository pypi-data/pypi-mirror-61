# zenodoclient

[![Build Status](https://travis-ci.org/shh-dlce/zenodoclient.svg?branch=master)](https://travis-ci.org/shh-dlce/zenodoclient)
[![codecov](https://codecov.io/gh/shh-dlce/zenodoclient/branch/master/graph/badge.svg)](https://codecov.io/gh/shh-dlce/zenodoclient)
[![Requirements Status](https://requires.io/github/cldf/zenodoclient/requirements.svg?branch=master)](https://requires.io/github/cldf/zenodoclient/requirements/?branch=master)
[![PyPI](https://img.shields.io/pypi/v/zenodoclient.svg)](https://pypi.org/project/zenodoclient)

# Usage

Install this package either from the repository (run, after cloning the repository, `python setup.py install`) or using `pip`. Then create an API access token [here](https://zenodo.org/account/settings/applications/tokens/new/). Then:
```
zenodo --access-token $YOURTOKEN ls
```
