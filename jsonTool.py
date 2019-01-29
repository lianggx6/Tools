import json

my_dict = {
    "a": 1,
    "b": 2,
    "c": 3
}
j = json.dumps(my_dict)
print j
temp = json.loads(j)
print type(temp)
