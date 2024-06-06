#!/bin/sh

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv install 3.10.14 -s
pyenv virtualenv 3.10.14 lights-control
./update-deps.sh
