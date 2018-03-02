"""
Transaction Service Module
"""
import redis
import json
from dal.objects.transaction import Transaction
from dal.services.hash_service import HashService

class TransactionService:
    """
    Transaction Service
    """

    @staticmethod
    def create_new_transaction():
        """
        Method Comment
        """
        pass

    @staticmethod
    def verfiy_rsa():
        """
        Method Comment
        """
        pass

    @staticmethod
    def verify_ownership_of_funds():
        """
        Method Comment
        """
        pass

    @staticmethod
    def _get_transactions_to_from_public_key(public_key, to_from, redis_conn = None, pipe = None, hs = None):
        """
        Get all transactions to or from a given public key

        Arguments:
        public_key  -- string of the public key to query the blockchain with
        to_from     -- get either transactions to or from: 0 is to, 1 is from. Defaults as 'to'
        redis_conn  -- redis connection if already established
        pipe        -- pipeline if already established

        Returns:
        list        -- list containing transactions to the given public key
            OR
        pipe        -- pipe with the query queued for continued use outside this method
        """

        transactions = list()

        direction = ""
        if to_from == 0:
            direction = "to_addr:"
        elif to_from == 1:
            direction = "from_addr:"
        else:
            direction = "to_addr"

        index_key = Transaction.prefix + ":" + direction + public_key

        if redis_conn == None:
            redis_conn = TransactionService._connect()

        if hs == None:
            hs = HashService()

        # if pipe is not established already, pipe should be executed within this method
        if pipe == None:
            pipe = redis_conn.pipeline()
            pipe.smembers(index_key)
            # get all of the transactions that were sent TO the given public key
            results = pipe.execute()
            for transaction_hash in results[0]:
                t = hs.get_object_by_full_key(transaction_hash, Transaction)
                transactions.append(t)
            return transactions

        # otherwise, just queue the query and return the pipe
        else:
            pipe.smembers(index_key)
            return pipe

    @staticmethod
    def get_transactions_from_public_key(public_key, redis_conn = None, pipe = None, hs = None):
        """
        Get all transactions from a given public key

        Arguments:
        public_key  -- string of the public key to query the blockchain with
        redis_conn  -- redis connection if already established
        pipe        -- pipeline if already established
        hs          -- HashService instance if established

        Returns:
        list        -- list containing transactions from the given public key
            OR
        pipe        -- pipe with the query queued for continued use outside this method
        """
        return TransactionService._get_transactions_to_from_public_key(public_key, 1, redis_conn, pipe, hs)

    @staticmethod
    def get_transactions_to_public_key(public_key, redis_conn = None, pipe = None, hs = None):
        """
        Get all transactions to a given public key

        Arguments:
        public_key  -- string of the public key to query the blockchain with
        redis_conn  -- redis connection if already established
        pipe        -- pipeline if already established
        hs          -- HashService instance if established

        Returns:
        list        -- list containing transactions to the given public key
            OR
        pipe        -- pipe with the query queued for continued use outside this method
        """
        return TransactionService._get_transactions_to_from_public_key(public_key, 0, redis_conn, pipe, hs)

    @staticmethod
    def get_transactions_by_public_key(public_key):
        """
        Get all transactions (to and from) a given public key

        Arguments:
        public_key  -- string of the public key to query the blockchain with

        Returns:
        list        -- list containing all transactions that a given public key was a part of
            AND
        float       -- float containing current balance for the supplied public key
        """
        r = TransactionService._connect()
        pipe = r.pipeline()

        hs = HashService()

        # get indexes for to_addr and from_addr
        pipe = TransactionService.get_transactions_to_public_key(public_key, pipe = pipe, hs = hs)
        pipe = TransactionService.get_transactions_from_public_key(public_key, pipe = pipe, hs = hs)
        results = pipe.execute()

        transactions = list()

        balance = 0.0

        # get all of the transactions that were sent TO the given public key
        for transaction_hash in results[0]:
            t = hs.get_object_by_full_key(transaction_hash, Transaction)
            transactions.append(t)
            balance += t.amount

        # get all of the transactions that were sent FROM the given public key
        for transaction_hash in results[1]:
            t = hs.get_object_by_full_key(transaction_hash, Transaction)
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