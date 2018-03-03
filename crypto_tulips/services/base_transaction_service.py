"""
Base Transaction Service Module
"""

import redis
import json
from enum import Enum
from dal.services.redis_service import RedisService


class TransactionType(Enum):
    """
    Enumerator to specify transaction type
    """
    TRANSACTION     = 0
    MEM_TRANSACTION = 1

class RequestType(Enum):
    """
    Enumerator to specify to get either to or from
    """
    TO      = 0
    FROM    = 1

class BaseTransactionService():
    """
    Base Transaction Service Class
    """

    @staticmethod
    def _get_transactions_to_from_public_key(public_key, to_from, obj, redis_conn = None, pipe = None, rs = None):
        """
        Get all transactions to or from a given public key

        Arguments:
        public_key  -- string of the public key to query the blockchain with
        to_from     -- RequestType enum: either TO or FROM (defaults as 'TO')
        obj         -- either Transacion or MemTransaction class
        redis_conn  -- redis connection if already established
        pipe        -- pipeline if already established

        Returns:
        list        -- list containing transactions to the given public key
            OR
        pipe        -- pipe with the query queued for continued use outside this method
        """

        transactions = list()

        direction = ""
        if to_from == RequestType.TO:
            direction = "to_addr:"
        elif to_from == RequestType.FROM:
            direction = "from_addr:"
        else:
            direction = "to_addr"

        index_key = obj._to_index()[-1] + ":" + direction + public_key

        if redis_conn == None:
            redis_conn = BaseTransactionService._connect()

        if rs == None:
            rs = RedisService()

        # if pipe is not established already, pipe should be executed within this method
        if pipe == None:
            pipe = redis_conn.pipeline()
            pipe.smembers(index_key)
            # get all of the transactions that were sent TO the given public key
            results = pipe.execute()
            for transaction_hash in results[0]:
                t = rs.get_object_by_full_key(transaction_hash, obj)
                transactions.append(t)
            return transactions

        # otherwise, just queue the query and return the pipe
        else:
            pipe.smembers(index_key)
            return pipe

    @staticmethod
    def get_transactions_from_public_key(public_key, obj, redis_conn = None, pipe = None, rs = None):
        """
        Get all transactions from a given public key

        Arguments:
        public_key  -- string of the public key to query the blockchain with
        obj         -- either a Transaction or a MemTransaction empty object (doesn't need to be instantiated)
        redis_conn  -- redis connection if already established
        pipe        -- pipeline if already established
        rs          -- RedisService instance if established

        Returns:
        list        -- list containing transactions from the given public key
            OR
        pipe        -- pipe with the query queued for continued use outside this method
        """
        return BaseTransactionService._get_transactions_to_from_public_key(public_key, RequestType.FROM, obj, redis_conn, pipe, rs)

    @staticmethod
    def get_transactions_to_public_key(public_key, obj, redis_conn = None, pipe = None, rs = None):
        """
        Get all transactions to a given public key

        Arguments:
        public_key  -- string of the public key to query the blockchain with
        obj         -- either a Transaction or a MemTransaction empty object (doesn't need to be instantiated)
        redis_conn  -- redis connection if already established
        pipe        -- pipeline if already established
        rs          -- RedisService instance if established

        Returns:
        list        -- list containing transactions to the given public key
            OR
        pipe        -- pipe with the query queued for continued use outside this method
        """
        return BaseTransactionService._get_transactions_to_from_public_key(public_key, RequestType.TO, obj, redis_conn, pipe, rs)

    @staticmethod
    def get_transactions_by_public_key(public_key, obj):
        """
        Get all transactions (to and from) a given public key

        Arguments:
        public_key  -- string of the public key to query the blockchain with
        obj         -- either a Transaction or a MemTransaction empty object (doesn't need to be instantiated)

        Returns:
        list        -- list containing all transactions that a given public key was a part of
            AND
        float       -- float containing current balance for the supplied public key
        """
        r = BaseTransactionService._connect()
        pipe = r.pipeline()

        rs = RedisService()

        # get indexes for to_addr and from_addr
        pipe = BaseTransactionService.get_transactions_to_public_key(public_key, obj, pipe = pipe, rs = rs)
        pipe = BaseTransactionService.get_transactions_from_public_key(public_key, obj, pipe = pipe, rs = rs)
        results = pipe.execute()

        transactions = list()

        balance = 0.0

        # get all of the transactions that were sent TO the given public key
        for transaction_hash in results[0]:
            t = rs.get_object_by_full_key(transaction_hash, obj)
            transactions.append(t)
            balance += t.amount

        # get all of the transactions that were sent FROM the given public key
        for transaction_hash in results[1]:
            t = rs.get_object_by_full_key(transaction_hash, obj)
            transactions.append(t)
            balance -= t.amount

        return transactions, balance


    @staticmethod
    def _connect():
        """
        Connect to the redis instance.

        Notes:
        - charset and decode_responses will need to be removed if we want this to be actually stored as bytes (per: https://stackoverflow.com/questions/25745053/about-char-b-prefix-in-python3-4-1-client-connect-to-redis)
        """
        settings = json.load(open('config/db_settings.json'))
        host = settings["host"]
        port = settings["port"]
        return redis.StrictRedis(host, port, db=0, charset="utf-8", decode_responses="True")