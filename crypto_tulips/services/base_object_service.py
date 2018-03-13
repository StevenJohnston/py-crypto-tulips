"""
Base Object Service Module
"""

import redis
import json
from enum import Enum
from crypto_tulips.dal.services.redis_service import RedisService

class RequestType(Enum):
    """
    Enumerator to specify to get either to or from
    """
    TO      = 0
    FROM    = 1

class BaseObjectService():
    """
    Base Object Service Class
    """

    @staticmethod
    def _get_objects_to_from_public_key(public_key, to_from, include_mempool, obj, redis_conn = None, pipe = None, rs = None):
        """
        Get all objects to or from a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        to_from         -- RequestType enum: either TO or FROM (defaults as 'TO')
        include_mempool -- True if want results in the mempool as well, False otherwise
        obj             -- object type to retrieve
        redis_conn      -- redis connection if already established
        pipe            -- pipeline if already established

        Returns:
        list        -- list containing objects to the given public key
            OR
        pipe        -- pipe with the query queued for continued use outside this method
        """

        objects = list()

        direction = ""
        if to_from == RequestType.TO:
            direction = "to_addr:"
        elif to_from == RequestType.FROM:
            direction = "from_addr:"
        else:
            direction = "to_addr"

        index_key = obj._to_index()[-1] + ":" + direction + public_key
        mempool_set = obj._to_index()[-1] + ":is_mempool:1"

        if redis_conn == None:
            redis_conn = BaseObjectService._connect()

        if rs == None:
            rs = RedisService()

        # if pipe is not established already, pipe should be executed within this method
        if pipe == None:
            pipe = redis_conn.pipeline()
            if include_mempool:
                # get all of the objects that were sent TO/FROM the given public key
                pipe.smembers(index_key)
            elif not include_mempool:
                # get all of the objects that were sent TO/FROM the given public key without objects in the mempool
                pipe.sdiff(index_key, mempool_set)

            results = pipe.execute()
            for object_hash in results[0]:
                t = rs.get_object_by_full_key(object_hash, obj)
                objects.append(t)
            return objects

        # otherwise, just queue the query and return the pipe
        else:
            if include_mempool:
                # get all of the objects that were sent TO/FROM the given public key
                pipe.smembers(index_key)
            elif not include_mempool:
                # get all of the objects that were sent TO/FROM the given public key without objects in the mempool
                pipe.sdiff(index_key, mempool_set)
            return pipe

    @staticmethod
    def get_objects_from_public_key(public_key, include_mempool, obj, redis_conn = None, pipe = None, rs = None):
        """
        Get all objects sent FROM a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise
        obj             -- either a object or a Memobject empty object (doesn't need to be instantiated)
        redis_conn      -- redis connection if already established
        pipe            -- pipeline if already established
        rs              -- RedisService instance if established

        Returns:
        list        -- list containing objects from the given public key
            OR
        pipe        -- pipe with the query queued for continued use outside this method
        """
        return BaseObjectService._get_objects_to_from_public_key(public_key, RequestType.FROM, include_mempool, obj, redis_conn, pipe, rs)

    @staticmethod
    def get_objects_to_public_key(public_key, include_mempool, obj, redis_conn = None, pipe = None, rs = None):
        """
        Get all objects sent TO a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise
        obj             -- type of object to retrieve
        redis_conn      -- redis connection if already established
        pipe            -- pipeline if already established
        rs              -- RedisService instance if established

        Returns:
        list        -- list containing objects to the given public key
            OR
        pipe        -- pipe with the query queued for continued use outside this method
        """
        return BaseObjectService._get_objects_to_from_public_key(public_key, RequestType.TO, include_mempool, obj, redis_conn, pipe, rs)

    @staticmethod
    def get_objects_by_public_key(public_key, include_mempool, obj):
        """
        Get all objects (to and from) a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise
        obj             -- type of object to retrieve

        Returns:
        list        -- list containing all objects that a given public key was a part of
            AND
        float       -- float containing current balance for the supplied public key
        """
        r = BaseObjectService._connect()
        pipe = r.pipeline()

        rs = RedisService()

        # get indexes for to_addr and from_addr
        pipe = BaseObjectService.get_objects_to_public_key(public_key, include_mempool, obj, pipe = pipe, rs = rs)
        pipe = BaseObjectService.get_objects_from_public_key(public_key, include_mempool, obj, pipe = pipe, rs = rs)
        results = pipe.execute()

        objects = list()

        balance = 0.0

        # get all of the objects that were sent TO the given public key
        for object_hash in results[0]:
            t = rs.get_object_by_full_key(object_hash, obj)
            objects.append(t)
            balance += t.amount

        # get all of the objects that were sent FROM the given public key
        for object_hash in results[1]:
            t = rs.get_object_by_full_key(object_hash, obj)
            objects.append(t)
            balance -= t.amount

        return objects, balance

    @staticmethod
    def get_from_mem_pool(obj):
        r = BaseObjectService._connect()
        rs = RedisService()

        # key to retrieve all object hashes in the mempool (ie object:is_mempool:1)
        name = obj._to_index()[-1] + ':is_mempool:1'
        object_list = r.srandmember(name, 10)

        objects = list()
        for object_hash in object_list:
            t = rs.get_object_by_full_key(object_hash, obj)
            objects.append(t)

        return objects

    @staticmethod
    def remove_from_mem_pool(obj):
        r = BaseObjectService._connect()
        pipe = r.pipeline()

        # change is_mempool to 0
        name = obj._to_index()[-1] + ':' + obj._hash
        pipe.hset(name, 'is_mempool', 0)

        # remove from list of mempool objects
        set_name = obj._to_index()[-1] + ":is_mempool:1"
        pipe.srem(set_name, name)

        # add to list of not-mempool objects
        new_set_name = obj._to_index()[-1] + ":is_mempool:0"
        pipe.sadd(new_set_name, name)

        res = pipe.execute()

    @staticmethod
    def _connect():
        """
        Connect to the redis instance.

        Notes:
        - charset and decode_responses will need to be removed if we want this to be actually stored as bytes (per: https://stackoverflow.com/questions/25745053/about-char-b-prefix-in-python3-4-1-client-connect-to-redis)
        """
        settings = json.load(open('crypto_tulips/config/db_settings.json'))
        host = settings["host"]
        port = settings["port"]
        return redis.StrictRedis(host, port, db=0, charset="utf-8", decode_responses="True")