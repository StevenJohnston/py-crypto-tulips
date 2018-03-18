from . import crypt_hashing_wif

def test_signiture_obj():
    public_key_hex, private_key_hex = crypt_hashing_wif.EcdsaHashing.generate_key_pair()
    signature = crypt_hashing_wif.EcdsaHashing.sign_message("message", private_key_hex)
    status = crypt_hashing_wif.EcdsaHashing.verify_signature(public_key_hex, signature, "message")
    assert status == True

def test_signiture_str():
    public_key_hex, private_key_hex = crypt_hashing_wif.EcdsaHashing.generate_key_pair_str()
    signature_hex = crypt_hashing_wif.EcdsaHashing.sign_message_hex("message", private_key_hex)
    status = crypt_hashing_wif.EcdsaHashing.verify_signature_hex(public_key_hex, signature_hex, "message")
    assert status == True

def test_unvalid_signiture_str():
    public_key_hex, private_key_hex = crypt_hashing_wif.EcdsaHashing.generate_key_pair_str()
    signature_hex = crypt_hashing_wif.EcdsaHashing.sign_message_hex("message", private_key_hex)
    status = crypt_hashing_wif.EcdsaHashing.verify_signature_hex(public_key_hex, signature_hex, "1message")
    assert status == False

def test_unvalid_signiture_obj():
    public_key_hex, private_key_hex = crypt_hashing_wif.EcdsaHashing.generate_key_pair()
    signature = crypt_hashing_wif.EcdsaHashing.sign_message("message", private_key_hex)
    status = crypt_hashing_wif.EcdsaHashing.verify_signature(public_key_hex, signature, "sdfmessage")
    assert status == False

def test_recovery_of_public_key():
    private_key = '26ac6d0bf2507a737558a015f6b29c260e294683cbb52ca22e579b7c7eaf483a'
    public_key = '89403913430fd91b97cf830f9562569286c7b80bd85d101c1b65016e2d6c0bccb2e57aec52633f0f85dc08b4ec1ce34bdb5e4889012a9571e5b277a4e0907c34'
    recover_pub_key = crypt_hashing_wif.EcdsaHashing.recover_public_key_str(private_key)
    assert recover_pub_key == public_key