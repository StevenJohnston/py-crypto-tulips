from . import crypt_hashing


jsonTest = {
    "Temp": "Hello"
}

jsonTestInvalid = {
    "Temp": None
}
b_message = b'To be signed'
b_different_message = b'change message'
message = "asdfasdf"
invalid = "asdf"


def test_hashing_string():
    hash = hashing_string("test")
    assert hash == "4d967a30111bf29f0eba01c448b375c1629b2fed01cdfcc3aed91f1b57d5dd5e"

def test_hashing_json():
    hash = hashing_string(jsonTest)
    assert hash == "08f04b54179fffeea74ebcef9c799562f478150d40b5abba1a8cd36ae53f2b0a"

def test_hashing_invalid_json():
    hash = hashing_string(jsonTestInvalid)
    assert hash == "d1908ea7bb037ceb78352064cff27baa70db25c69beeaf9918155d9ce95c0958"

def hashing_string(string_to_hash):
    return crypt_hashing.Hashing.hashing_block(string_to_hash)


def test_valid_signature():
    public_key, private_key = crypt_hashing.Hashing.generate_rsa_key("asdfasdf")
    signature = crypt_hashing.Hashing.signature_of_data(b_message, private_key)
    status = crypt_hashing.Hashing.validate_signature(b_message, public_key, signature)
    assert status == True

def test_invalid_signature():
    public_key, private_key = crypt_hashing.Hashing.generate_rsa_key("asdfasdf")
    signature = crypt_hashing.Hashing.signature_of_data(b_message, private_key)
    status = crypt_hashing.Hashing.validate_signature(b_different_message, public_key, signature)
    assert status == False

def test_normal_string_signature():
    public_key, private_key = crypt_hashing.Hashing.generate_rsa_key(message)
    signature = crypt_hashing.Hashing.encode_signature_of_data(message, private_key)
    status = crypt_hashing.Hashing.encode_validate_signature(message, public_key, signature)
    assert status == True


def test_invalid_string_signature():
    public_key, private_key = crypt_hashing.Hashing.generate_rsa_key(message)
    signature = crypt_hashing.Hashing.encode_signature_of_data(message, private_key)
    status = crypt_hashing.Hashing.encode_validate_signature(invalid, public_key, signature)
    assert status == False

def test_recover_public_key():
    public_key, private_key = crypt_hashing.Hashing.generate_rsa_key(message)
    recover_public_key = crypt_hashing.Hashing.get_public_key(private_key)
    assert public_key == recover_public_key

def test_recover_public_key_full_usecase():
    public_key, private_key = crypt_hashing.Hashing.generate_rsa_key(message)
    recover_public_key = crypt_hashing.Hashing.get_public_key(private_key)
    signature = crypt_hashing.Hashing.encode_signature_of_data(message, private_key)
    status = crypt_hashing.Hashing.encode_validate_signature(message, recover_public_key, signature)
    assert status == True

def test_invalid_recover_public_key_full_usecase():
    public_key, private_key = crypt_hashing.Hashing.generate_rsa_key(message)
    recover_public_key = crypt_hashing.Hashing.get_public_key(private_key)
    signature = crypt_hashing.Hashing.encode_signature_of_data(message, private_key)
    status = crypt_hashing.Hashing.encode_validate_signature(invalid, recover_public_key, signature)
    assert status == False