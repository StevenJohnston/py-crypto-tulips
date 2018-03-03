"""
Module to store objects in the redis database.
"""

import redis
import json
import inspect
from crypto_tulips.logger import crypt_logger

class HashService:
    """
    Service to generically interact with redis. Designed for use with objects that need to be stored with multiple fields (ie: transactions, contracts).
    The object that is being stored will need a field named prefix to prefix the key that will be used for redis.
    It will also need a field that contains the prefix with '_hash' afterwards.
    (ie: the prefix used in the transaction object is 'transaction' which will result in the key: 'transaction:transaction_hash')
    """

    _host = ""
    _port = ""
    _prefix = "prefix"

    def __init__(self):
        """
        Constructor

        Gets the host and port from config/db_settings.json for redis
        """
        settings = json.load(open('crypto_tulips/config/db_settings.json'))
        self.host = settings["host"]
        self.port = settings["port"]
        crypt_logger.Logger.log("HashService Initialized with redis running on " + self.host + ":" + self.port, 0, crypt_logger.LoggingLevel.INFO)


    def store_hash(self, obj):
        """
        Store an object in redis.
        Object required a field called 'prefix' and another field called prefix+'_hash' to create the key.
        Uses reflection to get the fields of an object to store them.

        Arguments:
        obj -- object to be stored in redis
        """
        attr_dict = self._get_attributes(obj)
        prefix = attr_dict.get(self._prefix)

        r = self._connect()
        pipe = r.pipeline()
        # name will be the prefix specified in the object + _hash
        name = prefix + ":" + attr_dict.get(prefix + "_hash")

        # iterate through fields
        for k, v in attr_dict.items():
            if k != self._prefix:
                pipe.hset(name, k, v)
        print(pipe)
        return pipe.execute()


    def _get_attributes(self, obj):
        """
        Uses reflection to get attributes of an object

        Arguments:
        obj -- object to get the attributes of
        """
        # get class attributes that aren't routines:
        attributes = inspect.getmembers(obj, lambda a: not(inspect.isroutine(a)))
        # further refine to only get the attributes:
        attributes = [attr for attr in attributes if not(attr[0].startswith('__') and attr[0].endswith('__'))]
        return dict(attributes)


    def get_object_by_hash(self, obj_hash, obj, pipe = None):
        """
        Get an entire object by it's hash

        Arguments:
        obj_hash    -- hash of the object to be retrieved
        obj         -- object's class to determine properties to retrieve
        pipe        -- pipeline if this is part of a transaction
        """
        attr_dict = self._get_attributes(obj)
        name = str(attr_dict.get(self._prefix)) + ":" + obj_hash

        if pipe is None:
            r = self._connect()
            pipe = r.pipeline()

        keys = list()
        for key, value in attr_dict.items():
            if key != self._prefix:
                pipe.hget(name, key)
                keys.append(key)
        values = pipe.execute()
        return dict(zip(keys, values))



    def get_field(self, obj_prefix, obj_hash, field_name, pipe = None):
        """
        Get a specific field for an object.

        Argument:
            obj_hash    -- hash of the object to retrieve the field from
            field_name  -- name of the field to retrieve
            pipe        -- pipeline if this is part of a transaction


        Returns:
            str         -- value of field specified
                OR
            pipeline    -- if pipeline was supplied, will return the pipeline for more operations
        """
        if pipe is None:
            r = self._connect()
            pipe = r.pipeline()
            pipe = pipe.hget(obj_prefix + ":" + obj_hash, field_name)
            return pipe.execute()
        else:
           return pipe.hget(obj_hash, field_name)


    def _connect(self):
        """
        Connect to the redis instance.

        Notes:
        - charset and decode_responses will need to be removed if we want this to be actually stored as bytes (per: https://stackoverflow.com/questions/25745053/about-char-b-prefix-in-python3-4-1-client-connect-to-redis)
        """
        return redis.StrictRedis(self.host, self.port, db=0, charset="utf-8", decode_responses="True")