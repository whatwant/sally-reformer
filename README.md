[![Gitter](https://badges.gitter.im/whatwant/community.svg)](https://gitter.im/whatwant/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)


## Python Virtual Environment

### pip upgrade
```bash
> python -m pip install --upgrade pip
```

### virtualenv install
```bash
> pip install virtualenv virtualenvwrapper-win
```

### create/activate virtualenv
```bash
> mkvirtualenv .venv
```

### deactivate virtualenv
```bash
> deactivate
```

### remove virtualenv
```bash
> rmvirtualenv .venv
```






# sally-reformer
Pattern-matching file name change python script

## Run sally-reformer
Follow the steps below to launch sally-reformer:
### Edit pattern
```
$ nano ./pattern.csv
```
### Run sally-reformer
```
usage: sally-reformer.py [-h] -p PATTERN_FILEPATH [-s SOURCE_DIRECTORY]

This code is written for rename filename with pattern

optional arguments:
  -h, --help            show this help message and exit
  -p PATTERN_FILEPATH, --pattern PATTERN_FILEPATH
                        pattern filepath
  -s SOURCE_DIRECTORY, --source SOURCE_DIRECTORY
                        source directory

```
