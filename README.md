## create virtualenv and install requirements

```sh
python3 -m venv .venv
pip install -r requirements.txt
```

## run app
```sh
export settings=dev
python server.py
```
or
```sh
export settings=dev
export FLASK_APP=server
export FLASK_ENV=development
flask run
```

or
```sh
$env:settings="dev"
$env:FLASK_APP="server"
$env:FLASK_ENV="development"
flask run
```

## run migrations
if you have changes in orm models run the following command

```sh
flask db init
flask db migrate -m "migration message"

```

```sh
flask db upgrade
```
or

## run in container

```sh
docker build -t flask_app .
docker run -p 8080:8080 -d  flaskapp
```

```sh
docker-compose up --build
# If you want to enter inside of container
docker ps
# Copy the flask container name (example: flask_experiment_flask_1) 
docker exec -ti flask_experiment_flask_1 /bin/bash
```
go to address 127.0.0.1:8080/test 