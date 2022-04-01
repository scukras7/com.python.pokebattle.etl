# Pokemon ETL

Python script to load select [Pokemon API](www.pokemonapi.co) data into MongoDB

### Contents
1. [Requirements](#requirements)
1. [Setup](#setup)
1. [Execute](#execute)

### Requirements
1. Python 3+

### Setup
1. Create file in project root called **.env.production** with the following fields:
```text
MONGO_HOST=
MONGO_PORT=
MONGO_USER=
MONGO_PASSWD=
MONGO_DB=
MONGO_AUTHDB=
```
1. Create virtualenv:
```sh
$ virutalenv --python=python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Execute
1. To execute the ETL scripts:
```sh
$ source venv/bin/activate
$ cd etl
$ python3 etl.py
$ python3 addPokemonDbSprites.py
$ python3 addTypeModifiers.py
```