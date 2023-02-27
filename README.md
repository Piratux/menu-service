# menu-service
A simple web service that implements CRUD operations on dish menu database.

## How to run it yourself
```
git clone https://github.com/Piratux/menu-service
cd menu-service
docker-compose up -d
docker-compose run -p 5000:5000 service
```

## Test it out
```
curl -d "{\"query\" : \"get_dishes\"}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/process
```
