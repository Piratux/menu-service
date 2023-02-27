f = open("res.json", "r")
x = f.read()
x = x.replace('\\"', '"')
x = x[1:len(x)-1:]

print(x)