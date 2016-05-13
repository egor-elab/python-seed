#!/bin/sh
python -m cogapp -r -D service_name=${1:-seed} @template_files
cp -r seed/ ${1:-auto}
for f in $(find ${1:-auto} -name '*seed*'); do mv $f ${f/seed/$1}; done
