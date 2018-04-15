import redis

from crypto_tulips.dal.objects.signed_contract import SignedContract
from crypto_tulips.dal.services.redis_service import RedisService

class SignedContractFilter:
    RATE = 'signed_contracts:rate'
    AMOUNT = 'signed_contracts:amount'
    SIGNED = 'signed_contracts:signed_date'
    DURATION = 'signed_contracts:duration'

    def __init__(self, key, minimum, maximum):
        self.key = key
        self.minimum = minimum
        self.maximum = maximum

class SignedContractService:

    @staticmethod
    def store_signed_contract(signed_contract, pipe = None):
        """
        Store a signed contract in the database.

        Arguments:
        signed_contract -- signed contract object to be store in the database

        Returns:
        list        -- list containing results of each query used to store an object (0s and 1s)
                    0s indicate that the field was updated (already present)
                    1s indicate that the field is new and was stored
            OR
        pipeline    -- pipeline object to continue inserting into redis with (if pipe was passed in)
        """
        rs = RedisService()
        rs.store_object(signed_contract)
        r = rs._connect()
        pipe_created = False
        if pipe == None:
            pipe = r.pipeline()
            pipe_created = True
        pipe.zadd(SignedContractFilter.RATE, signed_contract.rate, signed_contract._hash)
        pipe.zadd(SignedContractFilter.AMOUNT, signed_contract.amount, signed_contract._hash)
        pipe.zadd(SignedContractFilter.SIGNED, signed_contract.signed_timestamp, signed_contract._hash)
        pipe.zadd(SignedContractFilter.DURATION, signed_contract.duration, signed_contract._hash)


        if pipe_created:
            return pipe.execute()
        else:
            return pipe

    @staticmethod
    def get_signed_contract_by_hash(signed_contract_hash):
        """
        Get a signed contract by it's hash.

        Arguments:
        signed_contract_hash   -- string of signed contract's hash to retrieve

        Returns:
        signed contract    -- signed contract object
        """
        rs = RedisService()
        return rs.get_object_by_hash(signed_contract_hash, SignedContract)

    @staticmethod
    def get_signed_contract_by_full_key(signed_contract_key):
        """
        Get a signed contract by it's full key.

        Arguments:
        signed_contract_key    -- string on signed contract's key to retrieve

        Returns:
        signed contract    -- signed contract object
        """
        rs = RedisService()
        return rs.get_object_by_full_key(signed_contract_key, SignedContract)

    @staticmethod
    def get_signed_contracts_by_filter(signed_contract_filters, include_mempool):
        """
        Get signed contracts by a filter.

        Arguments:
        signed_contract_filters    -- list of SignedContractFilter objects to filter database on
        include_mempool     -- True if results should include those in the mempool, false otherwise

        Returns:
        list    -- list of signed contracts based on filters passed in
        """
        rs = RedisService()
        r = rs._connect()

        signed_contract_hashes = set()
        temp_hashes = set()
        mempool_list = list()
        mempool_set = set()

        if not include_mempool:
            mempool_list = r.smembers('signed_contract:is_mempool:0')
            for mem_hash in mempool_list:
                mempool_set.add(mem_hash[16:]) # remove 'signed_contract:' from the beginning of the key

        if not signed_contract_filters:
            in_mempool_list = r.smembers('signed_contract:is_mempool:1')
            in_mempool_set = set()
            for mem_hash in in_mempool_list:
                in_mempool_set.add(mem_hash[16:]) # remove 'contract:' from the beginning of the key

            if include_mempool:
                signed_contract_hashes = in_mempool_set.union(mempool_set)
            else:
                signed_contract_hashes = in_mempool_set.copy()
        else:
            for signed_contract_filter in signed_contract_filters:
                print("key: " + signed_contract_filter.key + " | range: " + str(signed_contract_filter.minimum) + "->" + str(signed_contract_filter.maximum))
                hashes = r.zrangebyscore(signed_contract_filter.key, signed_contract_filter.minimum, signed_contract_filter.maximum)
                temp_hashes = set(hashes)
                # if first filter
                if len(signed_contract_hashes) == 0:
                    signed_contract_hashes = temp_hashes.copy()
                    # if mempool signed_contracts are to be ignored
                    if not include_mempool:
                        signed_contract_hashes = signed_contract_hashes.intersection(mempool_set)
                    temp_hashes.clear()
                else:
                    # after first filter
                    signed_contract_hashes = signed_contract_hashes.intersection(temp_hashes)

        signed_contracts = list()
        for signed_contract_hash in signed_contract_hashes:
            signed_contract = rs.get_object_by_hash(signed_contract_hash, SignedContract, r)
            signed_contracts.append(signed_contract)

        signed_contracts.sort(key=lambda sc: (sc.created_timestamp))
        return signed_contracts[:50]

    @staticmethod
    def get_all_signed_contracts_by_contract_hash(contract_hash):
        rs = RedisService()
        r = rs._connect()
        keys = r.smembers('signed_contract:parent_hash:' + contract_hash)

        signed_contracts = list()
        for key in keys:
            signed_contract = rs.get_object_by_full_key(key, SignedContract)
            signed_contracts.append(signed_contract)
        return signed_contracts

    @staticmethod
    def get_all_open_signed_contracts():
        # only gets open signed_contracts not in the mempool
        rs = RedisService()
        r = rs._connect()

        keys = r.smembers('signed_contract:is_mempool:0')
        open_signed_contracts = []
        for key in keys:
            signed_contract = SignedContractService.get_signed_contract_by_full_key(key)
            if not r.exists('terminated_contract:' + signed_contract._hash):
                open_signed_contracts.append(signed_contract)
        return sorted(open_signed_contracts, key=lambda sc: (sc.signed_timestamp + sc.duration))


    @staticmethod
    def get_all_signed_contracts_by_owner(owner):
        rs = RedisService()
        r = rs._connect()

        keys = r.smembers('signed_contract:parent_owner:' + owner)
        signed_contracts = []
        for key in keys:
            signed_contract = SignedContractService.get_signed_contract_by_full_key(key)
            signed_contracts.append(signed_contract)
        return signed_contracts


    @staticmethod
    def get_all_signed_contracts_by_contract_hash(contract_hash):
        rs = RedisService()
        r = rs._connect()

        keys = r.smembers('signed_contract:parent_hash:' + contract_hash)
        signed_contracts = []
        for key in keys:
            signed_contract = SignedContractService.get_signed_contract_by_full_key(key)
            signed_contracts.append(signed_contract)
        return signed_contracts


    @staticmethod
    def get_all_signed_contracts_by_from_addr(from_addr):
        rs = RedisService()
        r = rs._connect()

        keys = r.smembers('signed_contract:from_addr:' + from_addr)
        signed_contracts = []
        for key in keys:
            signed_contract = SignedContractService.get_signed_contract_by_full_key(key)
            signed_contracts.append(signed_contract)
        return signed_contracts



