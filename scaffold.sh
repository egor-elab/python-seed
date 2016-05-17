#!/bin/sh
python -m cogapp -r -D service_name=${1} @template_files
cp -r seed/ ${1}
for f in $(find ${1} -name '*seed*'); do mv $f ${f/seed/$1}; done

source ./venv
mkvirtualenv ${1}
workon .
pip install -r requirements.txt
pip install pytest
deactivate

git remote rm origin
git remote add seed git://github.com/egor-elab/python-seed.git
