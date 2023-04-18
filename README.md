# menu-service
A simple REST Python + MySQL web service that implements CRUD operations on dish menu database.

## How to run it yourself
```bash
git clone https://github.com/Piratux/menu-service
cd menu-service
docker-compose up -d
```

## Documentation
https://documenter.getpostman.com/view/26799355/2s93XsWkQ8

## Test it out
```bash
curl -X GET http://127.0.0.1:5000/dishes
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
