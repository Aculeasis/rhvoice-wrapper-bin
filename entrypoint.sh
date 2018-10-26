#!/bin/bash

set -o errexit

echo "Architecture: $(dpkg --print-architecture)"
echo "Environment: $(uname -a)"

apt-get update -qq
apt-get install --no-install-recommends -y -qq git scons build-essential python3 python3-pip lame opus-tools flac
python3 -m pip install -U pip
python3 -m pip install -U setuptools wheel

python3 setup.py bdist_wheel --dist-dir=github

python3 -m pip install --no-cache-dir github/*.whl
git clone --depth=1 https://github.com/Aculeasis/rhvoice-proxy
cd rhvoice-proxy
python3 -m unittest discover -v -s rhvoice_wrapper/tests/
