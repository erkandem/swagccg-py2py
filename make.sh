#!/bin/sh
# shell version of make.cmd
# don't forget chmod +x make.sh make_html.sh
activate (){
    . ../.venv/bin/activate
    }

pwd
activate
# delete cached files from previous builds and tests
rm -rf build
rm -rf swagccg.egg-info
rm -rf dist
rm -rf .pytest_cache
rm -rf htmlcov
rm -rf cov_html
rm -rf cov_annotate
rm -rf .pytest_cache

# run to see whether it actually works
python3 -m swagccg -c swagccg/example/config.json

# create new test coverage
pytest --cov-report html:cov_html \
        --cov-report xml:cov.xml \
        --cov-report annotate:cov_annotate\
        --cov=swagccg swagccg/tests

# package the project using setuptools
# setuptools? wheels?
python setup.py sdist bdist_wheel
pdoc --html \
     --html-dir /home/kan/dev/py/sccg-py2py/swagccg-pdocs \
     --overwrite swagccg

# test whether the source is installable
pip uninstall swagccg --yes
pip install -r requirements.txt
pip install .
pip uninstall swagccg --yes

# test whether wheel is installable
pip install dist/swagccg-0.3.0.tar.gz
pip uninstall swagccg --yes

./make_html.sh
pytest -vv
# twine upload dist/*

# Is the virtualenv activated?
# sphinx-build html swagccg/docs/source ../swagccg-py2py-docs


git add .
git commit -m "passed tests auto commit and push"
git push origin master

coverage run -m swagccg --c swagccg/example/config.json

#: '
cd ../swagccg-py2py-docs/html
git add .
git commit -m "passed tests auto-built, commit docs and push to gh-pages"
git push origin gh-pages
cd ../../swagccg-py2py/
#'
