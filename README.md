# menu-service
A simple web service that implements CRUD operations on dish menu database.

## How to run it yourself
```bash
git clone https://github.com/Piratux/menu-service
cd menu-service
docker-compose up -d
docker-compose run -p 5000:5000 service
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
