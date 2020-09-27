## rhvoice-wrapper-bin
[![RHVoice](https://img.shields.io/badge/RHVoice-1.2.3-lightgrey.svg)](https://github.com/Olga-Yakovleva/RHVoice/tree/1.2.3)
[![PyPI version](https://img.shields.io/pypi/v/rhvoice-wrapper-bin.svg)](https://pypi.org/project/rhvoice-wrapper-bin/)
[![Python versions](https://img.shields.io/badge/python-3.4%2B-blue.svg)](https://pypi.org/project/rhvoice-wrapper-bin/)
[![PyPI - Format](https://img.shields.io/pypi/format/rhvoice-wrapper-bin.svg)](https://pypi.org/project/rhvoice-wrapper-bin/)
[![Build Status](https://travis-ci.com/Aculeasis/rhvoice-wrapper-bin.svg?branch=master)](https://travis-ci.com/Aculeasis/rhvoice-wrapper-bin)
[![Build status](https://ci.appveyor.com/api/projects/status/7msh0o7ljxnhiv3u?svg=true)](https://ci.appveyor.com/project/Aculeasis/rhvoice-wrapper-bin)

Provides [RHVoice](https://github.com/Olga-Yakovleva/RHVoice) libraries for [rhvoice-wrapper](https://github.com/Aculeasis/rhvoice-proxy). Depends on [rhvoice-wrapper-data](https://github.com/Aculeasis/rhvoice-wrapper-data), that contains languages and voices.

If this package installed, `rhvoice-wrapper` will automatically use it by default.

## Install on Linux
This will download and build RHVoice and may take many time
```bash
apt-get install --no-install-recommends build-essential python3-pip python3-setuptools python3-wheel
pip3 install scons lxml
pip3 install rhvoice-wrapper-bin
```

Alternatively, you may install auto build wheel packages from github [releases](https://github.com/Aculeasis/rhvoice-wrapper-bin/releases) (may not work).

## Install on Windows
#### Binary
```bash
python3 -m pip install wheel
python3 -m pip install rhvoice-wrapper-bin --only-binary rhvoice-wrapper-bin
```
#### Build
Install manually: git, Unicode NSIS and Visual Studio 2015 (2013+ must works)
```bash
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install scons lxml
python3 -m pip install rhvoice-wrapper-bin --no-binary rhvoice-wrapper-bin
```
## Usage
`rhvoice-wrapper` will automatically use path to library and data path from `rhvoice-wrapper-bin` (data, of course, provided `rhvoice-wrapper-data`).

#### Get info from library
```python
import rhvoice_wrapper_bin
# All the paths will None in error

# Contains path to the RHVoice library
print(rhvoice_wrapper_bin.lib_path)
# Contains path to the RHVoice data
print(rhvoice_wrapper_bin.data_path)
# Contains path to the RHVoice libraries.
print(rhvoice_wrapper_bin.LIBS_PATH)
# Contains path to the rhvoice-wrapper-bin
print(rhvoice_wrapper_bin.PATH)
```
