#!/bin/sh

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv activate lights-control

pip install --upgrade setuptools pip
pip install wheel pip-tools

pip-compile "$@"
pip-sync requirements.txt
