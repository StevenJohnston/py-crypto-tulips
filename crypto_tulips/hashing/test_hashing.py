from . import crypt_hashing


jsonTest = {
    "Temp": "Hello"
}

jsonTestInvalid = {
    "Temp": None
}

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