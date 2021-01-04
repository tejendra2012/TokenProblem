# TokenProblem

## Setup

1. Install Redis Server on deployed machine.
```sh
$ sudo apt install redis-server
$ redis-cli config set notify-keyspace-events Ex
```

2. The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/tejendrasingh/TokenProblem.git
$ cd TokenProblem
```

3. Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv -p /usr/bin/python3 env
$ source env/bin/activate
```

4. Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:

5. Create database tables:
```sh
(env)$ python manage.py makemigrations api
(env)$ python manage.py migrate
```

## Starting the web server

1. Run python application:
```sh
(env)$ python manage.py runserver
```
Or
```sh
(env)$ python manage.py runserver 0.0.0.0:8080
```

## Test the API using Curl Command.

1. Create Token API

### Request:

```sh
(home)$curl -X GET "http://127.0.0.1:8080/api/v1/create-token"
```

### Response:

{
    "Token": "f57b53eadf1e617bc7129160f642b75b6c32dcf9"
}

2. Assign Token API.

### Request:

```sh
(home)$ curl -X POST 'http://127.0.0.1:8080/api/v1/assign-token' -d '{"username":"tejendra"}'
```

### Response:
{
    "Token": "f57b53eadf1e617bc7129160f642b75b6c32dcf9"
}

3. Unblock Token API.

### Request:

```sh
(home)$ curl -X POST 'http://127.0.0.1:8080/api/v1/unblock-token' -d '{"username":"tejendra","Token":"f57b53eadf1e617bc7129160f642b75b6c32dcf9"}'
```

### Response:
{
    "Unblock-Token": "f57b53eadf1e617bc7129160f642b75b6c32dcf9"
}

4. Remove Token API.

### Request

```sh
(home)$ curl -X POST 'http://127.0.0.1:8080/api/v1/remove-token' -d '{"username":"tejendra","Token":"f57b53eadf1e617bc7129160f642b75b6c32dcf9"}'
```

### Response:
{
    "Removed-Token": "f57b53eadf1e617bc7129160f642b75b6c32dcf9"
}

5. Keep Alive Token API.

### Request:

```sh
(home)$ curl -X POST 'http://127.0.0.1:8080/api/v1/keep-alive-token' -d '{"username":"tejendra","Token":"f57b53eadf1e617bc7129160f642b75b6c32dcf9"}'
```

### Response:
{
    "Keep-Alive-Token": "f57b53eadf1e617bc7129160f642b75b6c32dcf9"
}

