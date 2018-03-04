from crypto_tulips.hashing.crypt_hashing import Hashing
import collections
import json

class Signable:
    signature = ''
    def get_signable(self): raise NotImplementedError

    # updates the _hash of the object
    def update_signature(self, private_key):
        self.signature = self.get_signature(private_key)

    # updates the _hash of the object
    def get_signature(self, private_key):
        signable = self.get_signable()
        signable_string = json.dumps(signable, sort_keys=True)
        return Hashing.str_signature_of_data(signable_string, private_key)

    # Used to get the hashable version of an object.
    # Use this with a the map function
    @staticmethod
    def get_signable_callback(signableObject):
        return signableObject.get_signable()