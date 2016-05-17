This repository is intended to be cloned to help you kickstart a new
microservice. You should run:
    git clone python-seed/.git yourservicename
    cd yourservicename
    sh scaffold.sh yourservicename
    git add -A
    git commit

Global python dependencies:
    cogapp
    coverage
    eventlet
    tox

On Windows you also need to do this (as administrator, outside any virtualenv):
    cd `dirname \`which python\``/Scripts
    cp virtualenvwrapper.sh{,.exe}
    cd -
