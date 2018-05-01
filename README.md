# Track Employee Travel

## Requirements

* Python 3.6
* [Pipenv](https://github.com/pypa/pipenv)
* Heroku Toolkitpip3 install pipenv

## Getting Started

### Install dependencies

Install Python3 and pipenv
```bash
# if pipenv is not installed
pip3 install pipenv
```

Install application dependencies
```bash
pipenv install
pipenv shell
```

### Add config
```bash
cp .env.sample to .env
```
update the .env file with configuration variables

### migrate database
```bash
./manage.py migrate
```

### create local super user
```bash
./manage.py createsuperuser
```


### run local server
```bash
./manage.py runserver
```

Open http://localhost:8000 to view it in the browser.
The page will reload if you make edits.
You will also see any errors in the console.

Your server is up and running!
