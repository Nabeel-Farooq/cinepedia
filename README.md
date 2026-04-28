App for writing reviews and rate.

## Why ?
To self hosted reviews about everything (films, series, games..) and rate them

## Requirements
- [Last.fm API key](http://www.last.fm/fr/api) to retrieve artists info (can be disable in source)
- Python 2.7 and later
- SQL database

## Deploying
- Create SQL database and configure connexion in config.py file [doc](http://flask-sqlalchemy.pocoo.org/2.1/config/)
- Create database structure
```sh
$ ./db_create.py
```
- Install app dependencies with [pip](https://pip.pypa.io/en/stable/installing/)
```sh
$ pip install -r requirements.txt
```
- Start app. Exemple invocations :
```sh
$ ./run.py --host 0.0.0.0
$ ./run.py --host 127.0.1.1 --port 8000
$ ./run.py --debug
```

## Enjoy !
