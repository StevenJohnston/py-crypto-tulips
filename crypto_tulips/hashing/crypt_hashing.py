"""
Hashing Module
"""

import hashlib
import json
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


class Hashing:
    """
    The Hashing Class that has static methods to help with different type of hashing
    """

    @staticmethod
    def hashing_block(json_block):
        """ Generates and returns a sha256 hash

        Keyword arugments:
        json_block -- JSON string

        Returns:
        string -- Returns the sha256 hash of the JSON string provided
        """
        return hashlib.sha256((json.dumps(json_block)).encode('utf-8')).hexdigest()

    @staticmethod
    def hashing_transaction(transaction_format):
        """ Return a sha256 base on a string

        Keyword arugments:
        transaction_format -- a string that should be formated with pipes

        Returns:
        string -- Returns the sha256 hash of base on the string provided
        """
        return hashlib.sha256(transaction_format.encode('utf-8')).hexdigest()

    @staticmethod
    def generate_rsa_key(secret):
        """ Generates a public and private key

        Keyword arugments:
        secret -- passphrase

        Returns:
        pub_key -- public key
        key -- private key
        """
        key = RSA.generate(2048)
        key.exportKey(passphrase=secret, pkcs=8, protection="scryptAndAES128-CBC")
        pub_key = key.publickey()
        return pub_key.exportKey().decode(), key.exportKey().decode()

    @staticmethod
    def encode_signature_of_data(data, private_key):
        """ A wrapper function that return a signiture base on the private key and data
        but you can provide a string for this function

        Keyword arugments:
        data -- data that being pass to be signed
        private_key -- Private Key

        Returns:
        signature_of_data() -- the signiture of the sign data
        """
        data_as_bytes = str.encode(data)
        return Hashing.signature_of_data(data_as_bytes, private_key)


    @staticmethod
    def signature_of_data(data, private_key):
        """ Returns a signiture base on the private key and data

        Keyword arugments:
        data -- data that being pass to be signed
        private_key -- Private Key

        Returns:
        signature -- the signiture of the sign data
        """
        hash_message = SHA256.new(data)
        pkey = RSA.import_key(private_key)
        signature = pkcs1_15.new(pkey).sign(hash_message)
        return signature

    @staticmethod
    def encode_validate_signature(data, pub_key, signature):
        """ A wrapper function that Validate the signiture base on the data, public key and a signiture
        but you can provide a string for this function

        Keyword arugments:
        data -- data that being pass to be signed
        pub_key -- public key
        data -- data to be validiated

        Returns:
        validate_signature() -- If the signiture is valided or not
        """
        data_as_bytes = str.encode(data)
        return Hashing.validate_signature(data_as_bytes, pub_key, signature)



    @staticmethod
    def validate_signature(data, pub_key, signature):
        """ Validate the signiture base on the data, public key and a signiture

        Keyword arugments:
        data -- data that being pass to be signed
        pub_key -- public key
        data -- data to be validiated

        Returns:
        bool -- If the signiture is valided or not
        """
        rsakey = RSA.importKey(pub_key)
        hash_data = SHA256.new(data)
        try:
            pkcs1_15.new(rsakey).verify(hash_data, signature)
            print("The signature is valid.")
            return True
        except (ValueError, TypeError):
            print("The signature is not valid.")
            return False

    @staticmethod
    def get_public_key(private_key):
        """ Get the public key base on the private key

        Keyword arugments:
        private_key -- Private Key

        Returns:
        pub_key -- Public Key
        """
        key = RSA.importKey(private_key)
        pub_key = key.publickey()
        return pub_key.exportKey().decode()

