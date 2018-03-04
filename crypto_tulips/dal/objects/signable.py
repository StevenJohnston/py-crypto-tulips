from crypto_tulips.hashing.crypt_hashing import Hashing
import json

class Signable:
    def get_signable(self): raise NotImplementedError

    # updates the _hash of the object
    def update_signature(self, private_key):
        self._hash = self.get_signature(private_key)

    # updates the _hash of the object
    def get_signature(self, private_key):
        signable = self.get_signable()
        return Hashing.signature_of_data(signable, private_key)

    # Used to get the hashable version of an object.
    # Use this with a the map function
    @staticmethod
    def get_signable_callback(signableObject):
        return signableObject.get_signable()