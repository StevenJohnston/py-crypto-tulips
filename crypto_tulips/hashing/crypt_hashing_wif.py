import hashlib
import ecdsa
from ecdsa import VerifyingKey, SECP256k1, SigningKey, NIST384p
from ecdsa.keys import SigningKey
from binascii import hexlify, unhexlify
class EcdsaHashing:
    """
    The Hashing Class that has static methods to help with different type of hashing
    """
    @staticmethod
    def hash_string(str_to_hash):
        """ Generates and returns a sha256 hash

        Keyword arugments:
        str_to_hash -- string to hash

        Returns:
        string -- Returns the sha256 hash of the string provided
        """
        return hashlib.sha256(str_to_hash.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_object(object_to_hash):
        """ Generates and returns a sha256 hash

        Keyword arugments:
        object_to_hash -- object to hash

        Returns:
        string -- Returns the sha256 hash of the object provided
        """
        return hashlib.sha256(json.dumps(object_to_hash, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()

    @staticmethod
    def recover_pubic_key(private_key):
        return private_key.get_verifying_key()

    @staticmethod
    def recover_public_key_str(private_key_str):
        sk = SigningKey.from_string(unhexlify(private_key_str), curve=ecdsa.SECP256k1, hashfunc = hashlib.sha256)
        public_key_hex = sk.get_verifying_key()
        return public_key_hex.to_string().hex()

    @staticmethod
    def verify_signature(public_key_hex, signature, message):
        vk = VerifyingKey.from_string(unhexlify(public_key_hex.to_string().hex()), curve=ecdsa.SECP256k1, hashfunc = hashlib.sha256)
        try:
            print("Valid")
            return vk.verify(unhexlify(signature), message.encode('utf-8'))
        except ecdsa.BadSignatureError:
            print("Not Valid")
            return False

    @staticmethod
    def verify_signature_hex(public_key_hex_str, signature, message):
        vk = VerifyingKey.from_string(unhexlify(public_key_hex_str), curve=ecdsa.SECP256k1, hashfunc = hashlib.sha256)
        try:
            print("Valid")
            return vk.verify(unhexlify(signature), message.encode('utf-8'))
        except ecdsa.BadSignatureError:
            print("Not Valid")
            return False

    @staticmethod
    def generate_key_pair():
        private_key_hex = SigningKey.generate(curve=SECP256k1, hashfunc=hashlib.sha256)
        public_key_hex = private_key_hex.get_verifying_key()
        priv_string=(private_key_hex.to_string()).hex()
        pub_string = (public_key_hex.to_string()).hex()
        print(priv_string)
        print(pub_string)
        return public_key_hex, private_key_hex

    @staticmethod
    def generate_key_pair_str():
        private_key_hex = SigningKey.generate(curve=SECP256k1, hashfunc=hashlib.sha256)
        public_key_hex = private_key_hex.get_verifying_key()
        priv_string=(private_key_hex.to_string()).hex()
        pub_string = (public_key_hex.to_string()).hex()
        return priv_string, pub_string

    @staticmethod
    def sign_message(message, private_key):
        return hexlify(private_key.sign(message.encode('utf-8'), hashfunc=hashlib.sha256))

    @staticmethod
    def sign_message_hex(privkey, message):
        sk = SigningKey.from_string(unhexlify(privkey), curve=ecdsa.SECP256k1, hashfunc = hashlib.sha256)
        return hexlify(sk.sign(message.encode('utf-8'), hashfunc=hashlib.sha256))

    @staticmethod
    def recover_public_key(private_key):
        sk = SigningKey.from_pem(private_key)
        public_key_hex = sk.get_verifying_key()
        print(hexlify(private_key_hex.to_string()).decode('ascii'))