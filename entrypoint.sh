#!/bin/bash

set -o errexit

echo "Architecture: $(dpkg --print-architecture)"
echo "Environment: $(uname -a)"

apt-get update -qq
apt-get install --no-install-recommends -y -qq git scons build-essential python3 python3-pip python-lxml flac libspeechd-dev pkg-config
python3 -m pip install -U pip
python3 -m pip install -U setuptools wheel

git config --global --add safe.directory /workd
python3 setup.py bdist_wheel --dist-dir=github

pip3 install github/*.whl
git clone --depth=1 https://github.com/Aculeasis/rhvoice-proxy
cd rhvoice-proxy
PYTHONIOENCODING=utf-8 python3 -m unittest discover -v -s rhvoice_wrapper/tests/
