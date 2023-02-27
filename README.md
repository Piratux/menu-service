# menu-service
A simple Python+MySql web service that implements CRUD operations on dish menu database.

## How to run it yourself
```bash
git clone https://github.com/Piratux/menu-service
cd menu-service
docker-compose up -d
```

## Test it out
```bash
curl -d "{\"query\" : \"get_dishes\"}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/process
```
You should see something like this:
```bash
"{\"result\":{\"0\":\"(1, Decimal('4.20'), 'Sea weed')\",\"1\":\"(2, Decimal('0.69'), 'Pop corn')\"}}"
```

## Prettifying output
The curl command above spits out barely readable json. But if you're on linux you can do this:
```bash
pip install pprintjson
curl -d "{\"query\" : \"get_dishes\"}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/process | python3 -c 'x = input(); x = x.replace(r"""\"""", "\""); x = x[1:len(x)-1:]; print(x)' | pprintjson
```
You should see something like this
```json
{
  "result": {
    "0": "(1, Decimal('4.20'), 'Sea weed')",
    "1": "(2, Decimal('0.69'), 'Pop corn')"
  }
}
```

## All supported query examples
Notes:
- All queries are sent and received in json format.
- 2 or more query arguments must be seperated with comma "," symbol.
- Comma "," symbol is not allowed in arguments (such as dish name).
### List supported queries
```bash
curl -d "{\"query\" : \"help\"}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/process
```
### Get dishes
Returns array of dishes with each entry containing (dish_id, price, name).
```bash
curl -d "{\"query\" : \"get_dishes\"}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/process
```
### Add dish [price, name]
```bash
curl -d "{\"query\" : \"add_dish 8.90, Ham Burger\"}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/process
```
### Delete dish [dish_id]
```bash
curl -d "{\"query\" : \"delete_dish 1\"}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/process
```
### Update dish [dish_id, price, name]
```bash
curl -d "{\"query\" : \"update_dish 2, 78.91, Chicken Noodles\"}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/process
```

## Making modifications
To edit the project and build it, in `docker-compose.yml` change
```yml
image: piratux/menu-web-service
```
to
```yml
build: ./
```
then run
```bash
docker-compose build
docker-compose stop
docker-compose up -d
```
