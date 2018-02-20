import redis
import json
import inspect

class HashService:
    _host = ""
    _port = ""
    _prefix = "prefix"

    def __init__(self):
        settings = json.load(open('db_settings.json'))
        self.host = settings["host"]
        self.port = settings["port"]

    def store_hash(self, obj):
        attr_dict = self._get_attributes(obj)
        prefix = attr_dict.get(self._prefix)
        print(attr_dict)
        r = self._connect()
        # name will be the prefix specified in the object + _hash
        name = prefix + ":" + attr_dict.get(prefix + "_hash")
        print(name)

        for k, v in attr_dict.items():
            if k != self._prefix:
                print("Storing: " + k + "->" + str(v))
                r.hset(name, k, v)
                print("Success.")

    def _get_attributes(self, obj):
        # get class attributes that aren't routines:
        attributes = inspect.getmembers(obj, lambda a: not(inspect.isroutine(a)))
        # further refine to only get the attributes:
        attributes = [attr for attr in attributes if not(attr[0].startswith('__') and attr[0].endswith('__'))]
        return dict(attributes)

    def _connect(self):
        return redis.StrictRedis(self.host, self.port, db=0, charset="utf-8", decode_responses="True")