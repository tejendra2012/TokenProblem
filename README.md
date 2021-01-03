# TokenProblem

## Setup

1. The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/tejendrasingh/TokenProblem.git
$ cd TokenProblem
```

2. Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv -p /usr/bin/python3 env
$ source env/bin/activate
```

3. Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:

4. Create database tables:
```sh
(env)$ python manage.py makemigrations api
(env)$ python manage.py migrate

## Starting the web server

1. Run python application:
```sh
(env)$ python manage.py runserver
```
Or
```sh
(env)$ python manage.py runserver 0.0.0.0:8080

