# menu-service
A simple REST Python + MySQL web service that implements CRUD operations on dish menu database.

## How to run it yourself
```bash
git clone https://github.com/Piratux/menu-service
cd menu-service
docker-compose up -d
```

## Test it out
```bash
curl -X GET http://127.0.0.1:5000/dishes
```

## Try service with python client
```bash
pip install requests
py client.py
```

## Making modifications
To edit the project and build it, in `docker-compose.yml` change
```yml
image: piratux/menu-web-service
# build: .
```
to
```yml
# image: piratux/menu-web-service
build: .
```
then run
```bash
docker-compose build
docker-compose stop service -t 1
docker-compose up -d
```
or alternatively
```bash
rebuild.bat
```
