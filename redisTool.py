import json
from redis import Redis

r = Redis(host="192.168.8.40",db=6)
# print r.config_get("bind")

# print r.hgetall("hash")


my_dict = {
    "a": 1,
    "b": 2,
    "c": 3
}
print r.rpush("test", 5)
# print r.lpop("test")
