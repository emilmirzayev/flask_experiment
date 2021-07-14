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

```sh
flask db upgrade
```
or if you have changes in orm models run the following command

```sh
flask db migrate -m "migration message"
```

## run in container

```sh
docker build -t flask_app .
docker run -p 8080:8080 -d  flaskapp
```
go to address 127.0.0.1:8080/test 