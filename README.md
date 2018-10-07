## rhvoice-wrapper-bin
[![PyPI version](https://img.shields.io/pypi/v/rhvoice-wrapper-bin.svg)](https://pypi.org/project/rhvoice-wrapper-bin/) [![Python versions](https://img.shields.io/pypi/pyversions/rhvoice-wrapper-bin.svg)](https://pypi.org/project/rhvoice-wrapper-bin/) [![PyPI - Format](https://img.shields.io/pypi/format/rhvoice-wrapper-bin.svg)](https://pypi.org/project/rhvoice-wrapper-bin/) [![Build Status](https://travis-ci.org/Aculeasis/rhvoice-wrapper-bin.svg?branch=master)](https://travis-ci.org/Aculeasis/rhvoice-wrapper-bin)

Provides RHVoice libraries for `rhvoice-wrapper`. Depends on `rhvoice-wrapper-data`, that contains languages and voices. 
Linux only.

If this package installed, `rhvoice-wrapper` will automatically use it by default.

## Install
`pip install rhvoice-wrapper-bin --only-binary rhvoice-wrapper-bin`

## Install from source
First, install dependencies to build:

`apt-get install --no-install-recommends scons build-essential python3-pip python3-setuptools python3-wheel`

Install package from source. This download and build RHVoice and may take many time:

`pip install rhvoice-wrapper-bin --no-binary rhvoice-wrapper-bin`

## Usage
`rhvoice-wrapper` will automatically use data path from `rhvoice-wrapper-bin` (but of course of `rhvoice-wrapper-data`).
You must set package library path for LD before run python scripts. You may set `LD_LIBRARY_PATH`, this must be works:
```bash
export LD_LIBRARY_PATH=$(pip3 show rhvoice-wrapper-bin | grep Location | awk '{print $2}')/rhvoice_wrapper_bin/lib/
python3 -u <script using rhvoice_wrapper>
```
#### Get info from library
```python
import rhvoice_wrapper_bin
# All the paths will None in error

# Contains path to the RHVoice library
print(rhvoice_wrapper_bin.lib_path)
# Contains path to the RHVoice data
print(rhvoice_wrapper_bin.data_path)
# Contains path to the RHVoice libraries. Must be set as dynamic libraries path
print(rhvoice_wrapper_bin.LIBS_PATH)
# Contains path to the rhvoice-wrapper-data
print(rhvoice_wrapper_bin.PATH)
```
## Links

- [RHVoice](https://github.com/Olga-Yakovleva/RHVoice)
- [rhvoice-wrapper](https://github.com/Aculeasis/rhvoice-proxy)
- [rhvoice-wrapper-data](https://github.com/Aculeasis/rhvoice-wrapper-data)
