#!/bin/sh
# $./make.sh
# don't forget chmod +x make.sh

activate_environment (){
    . ../.venv/bin/activate
    }

remove_old_builds(){
    rm -rf build
    rm -rf swagccg.egg-info
    rm -rf dist
    rm -rf .pytest_cache
    rm -rf htmlcov
    rm -rf cov_html
    rm -rf cov_annotate
    rm -rf .pytest_cache
}

did_pytest_pass(){
    pytest_response=""
    pytest_response=$(pytest -q -x --tb=no  | grep 'F')
    if [ "$pytest_response" != "" ]; then
        echo "pytest failed. Back to debugging maestro!"
        exit 1
    else
       echo "pytest passed. Continuing script execution"
    fi
}


activate_environment
remove_old_builds
did_pytest_pass


# run to see whether it actually works
python3 -m swagccg -c swagccg/example/config.json

# create new test coverage report
pytest --cov-report html:cov_html \
    --cov-report xml:cov.xml \
    --cov-report annotate:cov_annotate\
    --cov=swagccg swagccg/tests


# test whether the source code is installable
pip uninstall swagccg --yes
pip install -r requirements.txt
pip install .
pip uninstall swagccg --yes

# package the project using setuptools
# setuptools and wheels installed?
python setup.py sdist bdist_wheel

# test whether dist tar-ball is installable
pip install dist/swagccg-0.3.1.tar.gz
pip uninstall swagccg --yes

# test whether dist tar-ball is installable
pip install dist/swagccg-0.3.1-py3-none-any.whl
pip uninstall swagccg --yes

# translate the markdown readme to .rst (python-sphinx native format)
pandoc -f markdown -t rst -o swagccg/docs/source/README.rst README.md

# initiate verbose pytest
pytest -vv

# re-build sphinx docs
sphinx-build -b html swagccg/docs/source ../swagccg-py2py-docs

# create coverage report
coverage run -m swagccg --c swagccg/example/config.json

#: '
# commit source changes
git add .
git commit -m "passed tests auto commit and push source"
git push origin master
#'

# commit documentation changes
#: '
cd ../swagccg-py2py-docs/html
git add .
git commit -m "passed tests auto-built, commit docs and push to gh-pages"
git push origin gh-pages
cd ../../swagccg-py2py/
#'

## upload build to pypi
## usage explained at https://github.com/pypa/twine
# twine upload dist/*

