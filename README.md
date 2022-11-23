# PyInvest


## Installation
```bash
# update python pip
python -m pip install -U pip
# clone latest repo
git clone https://github.com/crj1998/PyInvest.git
cd PyInvest
# install dependency package 
pip install -r requirements.txt
```
## Build
### Code Style check
```
python -m pylint --rcfile .pylintrc pyinvest
```
### Unit Test
```bash
python -m pytest
python -m pytest test/test_setup.py::TestSetup::test_version -v -s
```
## Develop
### ide.csdn
```bash
# Configure the pip source
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# Upgrade pip
python -m pip install -U pip
mkdir /ide/workspace/lib
# install dependency package 
pip install -r requirements.txt -t /ide/workspace/lib --force-reinstall
export PYTHONPATH=$PYTHONPATH:/ide/workspace/lib
```
