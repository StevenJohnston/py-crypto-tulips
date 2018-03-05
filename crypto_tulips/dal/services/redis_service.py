"""
Module to store objects in the redis database.
"""

import redis
import json
import inspect
from crypto_tulips.logger.crypt_logger import Logger, LoggingLevel

class RedisService:
    """
    Service to generically interact with redis. Designed for use with objects that need to be stored with multiple
    fields (ie: transactions, contracts).
    The object that is being stored will need:
    - a static method called _to_index(self) that returns a list of fields as strings indicating the fields to be indexed. The final string should be the 'table' name
    - a static method called from_dict(dictionary) that sets the fields of a given object from a dictionary of field, values
    - a field named '_hash' to use as the main key for redis

    For example:
        The 'table' name used in the transaction object is 'transaction' which will result in the key:
            'transaction:_hash'
        and indexed fields like:
            'transaction:indexed_field_name:value'
    """

    _host = ""
    _port = ""
    _prefix = "prefix"
    _hash = "_hash"

    def __init__(self):
        """
        Constructor

        Gets the host and port from config/db_settings.json for redis
        """
        settings = json.load(open('crypto_tulips/config/db_settings.json'))
        self.host = settings["host"]
        self.port = settings["port"]
        Logger.log("HashService Initialized with redis running on " + self.host + ":" + self.port, 0, LoggingLevel.INFO)

    def store_object(self, obj, redis_conn = None, pipe = None):
        """
        Store an object in redis.
        Uses reflection to get the fields of an object to store them.

        Arguments:
        obj         -- object to be stored in redis
        redis_conn  -- redis connection if already established
        pipe        -- pipeline if already established

        Returns:
        list    -- list containing results of each query used to store an object (0s and 1s)
                0s indicate that the field was updated (already present)
                1s indicate that the field is new and was stored
        """
        attr_dict = self._get_attributes(obj)


        if redis_conn == None :
            redis_conn = self._connect()

        if pipe == None:
            pipe = redis_conn.pipeline()
        # name will be the prefix specified in the object + _hash
        obj_field_keys = obj._to_index()
        prefix = obj_field_keys[-1]
        name = prefix + ":" + attr_dict.get(self._hash)

        # iterate through fields
        for k, v in attr_dict.items():
            if k != self._prefix:
                pipe.hset(name, k, v)
                # if we want the field to be indexed:
                if (k != self._hash) and (obj._to_index().__contains__(k)):
                    # index the field as 'prefix:field_name:field_value', and the transaction key
                    pipe.sadd(prefix + ":" + k + ":" + str(v), name)
        return pipe.execute()

    def _get_attributes(self, obj):
        """
        Uses reflection to get attributes of an object

        Arguments:
        obj     -- object to get the attributes of

        Returns:
        dict    -- dictionary containing the attributes of the object
        """
        # get class attributes that aren't routines:
        attributes = inspect.getmembers(obj, lambda a: not(inspect.isroutine(a)))
        # further refine to only get the attributes:
        attributes = [attr for attr in attributes if not(attr[0].startswith('__') and attr[0].endswith('__'))]
        return dict(attributes)

    def get_object_by_full_key(self, obj_key, obj, redis_conn = None):
        """
        Get an entire object by it's hash

        Arguments:
        obj_key     -- key of object to retrieve (include prefix here)
        obj         -- object's class to determine properties to retrieve
        redis_conn  -- redis connection if already established

        Returns:
        obj         -- object retrieved from redis, populated with values
        """
        # get attributes of object
        attr_dict = self._get_attributes(obj)

        # if no already established redis connection, connect
        if redis_conn == None:
            redis_conn = self._connect()

        # create a pipeline to queue commands
        pipe = redis_conn.pipeline()

        keys = list()
        print(keys)
        # iterate through attributes of object
        for key, value in attr_dict.items():
            # queue hget
            pipe.hget(obj_key, key)
            # add key to list of keys
            keys.append(key)
        # execute queue of commands, save values
        values = pipe.execute()

        # instantiate object from dictionary with keys and values
        obj = obj.from_dict(dict(zip(keys, values)))
        return obj

    def get_object_by_hash(self, obj_hash, obj, redis_conn = None):
        """
        Get an object given just it's hash.
        - Use this if you don't want to specify the prefix and have it gathered from the object

        Arguments:
        obj_hash    -- hash of object to retrieve
        obj         -- object's class to determine properties to retrieve
        redis_conn  -- redis connection if already established

        Returns:
        obj         -- object retrieved from redis, populated with values
        """
        # get attributes of object
        # prepend prefix and ":" to the obj_hash
        name = obj._to_index()[-1] + ":" + obj_hash

        return self.get_object_by_full_key(name, obj, redis_conn)

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