from crypto_tulips.hashing.crypt_hashing_wif import EcdsaHashing
import json

class Hashable:
    _hash = ''
    # Returns the object that will be used to get the hash for the blockchain.
    # Since some objects have aditional members this method allows us to remove these non-block related members
    def get_hashable(self): raise NotImplementedError

    # updates the _hash of the object
    def update_hash(self):
        self._hash = self.get_hash()

    # updates the _hash of the object
    def get_hash(self):
        hashable = self.get_hashable()
        return EcdsaHashing.hash_object(hashable)

    # Used to get the hashable version of an object.
    # Use this with a the map function
    @staticmethod
    def get_hashable_callback(hashableObject):
        return hashableObject.get_hashable()

    def valid_hash(self):
        return self.get_hash() == self._hash