#!/bin/bash

set -o errexit

echo "Architecture: $(dpkg --print-architecture)"
echo "Environment: $(uname -a)"

apt-get update -qq
apt-get install --no-install-recommends -y -qq git scons build-essential python3 python3-pip
python3 -m pip install -U pip
python3 -m pip install -U setuptools wheel

python3 setup.py bdist_wheel --dist-dir=github
