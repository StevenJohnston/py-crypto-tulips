from crypto_tulips.services.genesis_block_service import GenesisBlockService
from crypto_tulips.dal.objects.block import Block
from crypto_tulips.hashing.crypt_hashing import Hashing
from crypto_tulips.dal.objects.transaction import Transaction
import pytest
import json

_priv = """-----BEGIN RSA PRIVATE KEY-----
MIIEoQIBAAKCAQBtxQbESKGGw1uYw113TkyhXfMHy2jq/iXJ+17oEzjGk6qzT39e
vE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme7wQEW5bM1lt5/LemQshRtKY9pcg3
xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLjTORn0ssrBlFi+bjG/eF/qyO9H0lj
OPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWidbUoMxnJCOFKK5Dmvgku/Ca3eVXTV
85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8ixWTW+67XNB0A12QFYMhjw4pvQ2m
wosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZAgMBAAECggEACuaB4YQE5kkIE4dz
BKH14iBePevpI0zRm9kmd41RGgcX8G54i4PPoLTGkUa9JHok659buCrGyv83jEj5
5Ql8/NdnYrdlpjmzI84AvrXrBpIV4BFSbJd80P1EPXdTV5I/SJRuBi2gz5Nhq1fk
tc9N4dyE4fqAymj6NAXwX3JerjrDKqjfWt076CLOIqoG2m7pcOcr00DVNTJcb7rj
fd2isAVhv2mJDJkOmO5/aOwX6FjywBkt0Vfs4wvByA2e9rc1D/3UeL0SHT4JliAj
VBQuodlMwLMqwaWbsMOuN3559p7kbd4oFBk8zkQb1KZ66RS/gTI2WLDcCfURaEbd
dxETwQKBgQCnxiMG2ws41v70iafQhmbSAv0DmS5PwCOvu8Y2n1QTboI84GOCDI7I
okxWT3vsfB1mXte26PFkAnkIE9DSQkx3iFtn7RNrAeOtvzIYG33t6tB3axK6fm2+
MqdXpO/r53PZb70+8dAEEobC0Q0POKR/z1nHopfw3idxEOo1oV9B/QKBgQCnfkzm
BggBdvnEoAzfmYXe18SsWH9Q93CZtXkfxeehHZuF01uGY9a6cyvHY/phmrANPUB1
mvapC3M53tcgEbDrO8Ue2VkyXpLlCLCXZxpTC2YFdElh/kvaJbEHhkL09hmDNjMu
wXuyYw4CXLjzRwuA8A+b6P0Z6LiMKn1lWWXFjQKBgA1TyfiDcfLD8WDPhoskAgrw
vdSJWIpxQuR00BwKsA0THDllwcHU6Yq6icHZcoiom1VEd3JKMtK095RSrqXlKlnc
dRZeWMqJTeLBa2NK28gIfSLfWI+D94fCUlS9/2kH68X8AFZ9sv5/0kCrhpQM9dRJ
TmJzYgp6OzvaEiDMftqpAoGAJid2OvvqvPKuSOUwqYreXPoH2j66meYT51/YfK1n
a2NEN0MDWWTK2GQ998jFk5BaRFnMoj2vrKhoEim6FZsSEzPlXnaig//ZNIU7PPIG
pB43mkx4HvN/sezeG9mwzP52p1YkaKU4mVVJLq6SjxCDBVcqJxj29vz1dTCEqh6o
OU0CgYAfixcS5l4bdAOuvv8QvEt+ACfoDuDdBds5j7Se3M+M0kS6VtbE3mnTSPxf
06GC2cu14VtSiXfKv59b95vBz/LRhKIUsJ/Q+TdVE7DJRI4S+tlZio0i9lvO1SHb
wPhY4P/Zsoe8tswOJyFbSBRNmXCPZ7UBOZcn9jVhg5SQBFIW7Q==
-----END RSA PRIVATE KEY-----"""

def test_generate_from_priv():
    block = GenesisBlockService.generate_from_priv(_priv)

    expected = {
        'owner':'-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
        'transactions':[
            {
                'from_addr':'',
                'amount':1.0,
                'timestamp':1520135639,
                'signature':'JLhYlCLqb1hhKamCbKWfGh4Ja6eqYYCzXEUKu0uIxj5y/uyZzfu6VSexLBukUAn9+/7qvRqRmTFIWWB1qhQ4vo8tkPpGGR7TcUMi55fgZeRccBndYjso/5ZWOwdiymSkXCbeW7VppzUbLwSrm9rIDFz52p2v7xZIJcY4UruJFlNPEpbkG0tOZRnFXmice/qu8hZJ4l/l55B834jM8DxeI4sI0myk5CXJOiy6vvupjQS8HAcbpFsKnhKKF/xXIYYSGUU123Mty2u5bjhKjpTVBVL53b4WV1fBDVOfg5mMlI+PY4AssUkYBIirrxeBVuXwl+DHwwc4ZHfXKTUH9G5h0Q==',
                'to_addr':'-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
                '_hash':'5719d7850b6128e5cc783087f48390d86993eda2acaa6905098597e3272a6884'
            },
            {
                'from_addr':'',
                'amount':10.0,
                'timestamp':1520135639,
                'signature':'UG6PAQhWjOSfTIo6g8EAe4fdyh1EcqPTx+1YaOE02+AABrmph4lhnIjL+RYEl6dF8mUZPs8ekV6dx/uVP58KnelYrciukZ6HKnd4k+jOF0K5Le3UlObADs7WJ5N4QzJaPOEvp5VMNOYF0YR/5QU7dxDVoTAdPGaooiYt8YemLl4qEmNTpOznLMZsal3PMiorp/H82JrQN2c2yAvWFXDFs9hyDL1I9Ul4iMtmjT2y9TpGF2MXF+JDwurqLS+2su3L8gx5scbe+TyrdpggeigVw173qgsoEbQkzxdZUGw6Fl6Ek2drCh1oDC7KKX6APmsOnCF+5y2x7rXYzTgca84y3g==',
                'to_addr':'-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
                '_hash':'cc2f9b562d42c97b7708a9d2a5e74d8f11dc3d7840b700a49caaeb1b55072618'
            },
            {
                'from_addr':'',
                'amount':100.0,
                'timestamp':1520135639,
                'signature':'FHXNlrfLsNznUZ1xc6gwgCXVaHZ2Ja0299UX6iDxpkO9ZXKkMvJ2Yl3qmW2MO2U9DzDrM/gohQZ2hCWEPTPEWFFS7pNO3t9PBOCWLusSwD/FBoJDAh3qhcSkQuvD+He8zUOp+7tb6839qqrecgWQ4pPnG5diFt2HfdM6kTUO/VnEcgbcGbHeAiOkjVbhAXnKzQSR/V6rQCQxNaEBSoLbq15LuMiVRMEj6xV97aFAno1gPI2yWehfyg+yUmgcojyLPMxlOVS0wI9SWMip8S9smIEijIjePdmKTT+Dqa1lspHIV9GTJGLd1qfamKPZG3rvsvbXP+k+0Chon0jxsvl9zA==',
                'to_addr':'-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
                '_hash':'50ef5c63eb31de177cb3ff7013b1f27855ca08ee8a82258ae49fd55d9d58d531'
            },
            {
                'from_addr':'',
                'amount':1000.0,
                'timestamp':1520135639,
                'signature':'WXMkix4a6MkAEIzT+RVCu6SAXm5Rt0nPe5jqvHVGvMD5z2p4JX0RglrfRhYgRlCZfsG/VeFKZXQ5xOq4JYoHsSDN6HGFS0P3NDkGzlZy+CzBP1gelrqR/s94/vi0uXKFQqgxj1zZWE8ScHPjtFzv9dIgrnuO6eUUjCLl2sp9iPCn6scqDGss8/Oi/nu8FFa02y5QWWC0bdjuzDSfNrSSFAnSqxWZqhCQlxFxvHW9GJxt9ErcqrEMSrw19HNGsQf2ANIfCs6dQXl/00AAp897fwoCl5y2O85zD5bRFT8Hp7lwLvSAqVwkWa8I+QZZEZRTv3aUTUnAFXiYo/fffrjCqQ==',
                'to_addr':'-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
                '_hash':'85ccd39b76976efe4e201635cec939b16b1aca696249ef0e1ad454c3e7188b47'
            }
        ],
        'timestamp':1520135639,
        '_hash':'1027b1cba972122fbf1b5452c2281e9b20437d5ddd848c06628eb72fc3d74ae0',
        'signature':'Hb5gadPe7aCTgFFWDINo5t+Qs5LuOojog3WkQq86lGPRhvuseDIXblGGsvMLGPnh6Ix6Hc/8PoD2+fW9W1A1ekOw8+xIN/Xx3gvQoOf1mC+f/08Mrm3BzPNHL+h+y2h/f2kOxq8a80TK12HnSF3ClSmfpcGqZkYyrpPkjBN6dmGbf+hrDTItRXrhMZW3KewB9mnGWJnfq5wwpAVdygHVHznVdjU64ALBsszknmSQ+ivhhoGqW0YHvfmy9oC4VVYHTjUQ7nB/+19TdIHPvErtNMkJlnltfsaK9euf+mx+VgmxFR6SH+ioMLxsmIqRF6u2CEKf/wiRdNHhFW+QkJTMeA==',
        'pos_transactions':[
            {
                'from_addr':'-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
                'amount':100.0,
                'timestamp':1520135639,
                '_hash':'6a6e42224a94f3baad484073ce95f92cf59c2ec468ec8acaa3ccc65db48f6057',
                'signature':'PCp46BHA9wIkkRbLdMz4vuuUcFxH/h94lpjrNnSIyVgmpclaiRDwZq8CpRQUXr4tT8aSBymVD110Yfpizoj/POITe+2ji8ggHUcwv6ScIQ7VFmunsl1mRHfOtVtbdOqXCBZ6IsKbpwpjtAck3fGk14D5kIVKoC2/6W2s0wYgi5riVs79BzGbbj0TdKx7SLItiiHLYi8e+t+LFH6GBY03ciiLU8C0GIuPA4nl5bPrOwadkzmv9zb9q/CluNfJaNx/kJ1S9/2YXXFtIMY26kaSlKzdFjWRVgNep7I7Y5XOyGlcSWNl8NTrCf4HPgyW4pgqFB53HB9uTKmLueyjTOqcPA=='
            }
        ],
        'height':0,
        'contract_transactions':[

        ]
    }
    actual = block.get_sendable()
    print(str(actual))
    assert actual == expected

def test_validate_rsa_block():
    genesis_block = {
        'owner':'-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
        'transactions':[
            {
                'from_addr':'',
                'amount':1.0,
                'timestamp':1520135639,
                'signature':'JLhYlCLqb1hhKamCbKWfGh4Ja6eqYYCzXEUKu0uIxj5y/uyZzfu6VSexLBukUAn9+/7qvRqRmTFIWWB1qhQ4vo8tkPpGGR7TcUMi55fgZeRccBndYjso/5ZWOwdiymSkXCbeW7VppzUbLwSrm9rIDFz52p2v7xZIJcY4UruJFlNPEpbkG0tOZRnFXmice/qu8hZJ4l/l55B834jM8DxeI4sI0myk5CXJOiy6vvupjQS8HAcbpFsKnhKKF/xXIYYSGUU123Mty2u5bjhKjpTVBVL53b4WV1fBDVOfg5mMlI+PY4AssUkYBIirrxeBVuXwl+DHwwc4ZHfXKTUH9G5h0Q==',
                'to_addr':'-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
                '_hash':'5719d7850b6128e5cc783087f48390d86993eda2acaa6905098597e3272a6884'
            },
            {
                'from_addr':'',
                'amount':10.0,
                'timestamp':1520135639,
                'signature':'UG6PAQhWjOSfTIo6g8EAe4fdyh1EcqPTx+1YaOE02+AABrmph4lhnIjL+RYEl6dF8mUZPs8ekV6dx/uVP58KnelYrciukZ6HKnd4k+jOF0K5Le3UlObADs7WJ5N4QzJaPOEvp5VMNOYF0YR/5QU7dxDVoTAdPGaooiYt8YemLl4qEmNTpOznLMZsal3PMiorp/H82JrQN2c2yAvWFXDFs9hyDL1I9Ul4iMtmjT2y9TpGF2MXF+JDwurqLS+2su3L8gx5scbe+TyrdpggeigVw173qgsoEbQkzxdZUGw6Fl6Ek2drCh1oDC7KKX6APmsOnCF+5y2x7rXYzTgca84y3g==',
                'to_addr':'-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
                '_hash':'cc2f9b562d42c97b7708a9d2a5e74d8f11dc3d7840b700a49caaeb1b55072618'
            },
            {
                'from_addr':'',
                'amount':100.0,
                'timestamp':1520135639,
                'signature':'FHXNlrfLsNznUZ1xc6gwgCXVaHZ2Ja0299UX6iDxpkO9ZXKkMvJ2Yl3qmW2MO2U9DzDrM/gohQZ2hCWEPTPEWFFS7pNO3t9PBOCWLusSwD/FBoJDAh3qhcSkQuvD+He8zUOp+7tb6839qqrecgWQ4pPnG5diFt2HfdM6kTUO/VnEcgbcGbHeAiOkjVbhAXnKzQSR/V6rQCQxNaEBSoLbq15LuMiVRMEj6xV97aFAno1gPI2yWehfyg+yUmgcojyLPMxlOVS0wI9SWMip8S9smIEijIjePdmKTT+Dqa1lspHIV9GTJGLd1qfamKPZG3rvsvbXP+k+0Chon0jxsvl9zA==',
                'to_addr':'-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
                '_hash':'50ef5c63eb31de177cb3ff7013b1f27855ca08ee8a82258ae49fd55d9d58d531'
            },
            {
                'from_addr':'',
                'amount':1000.0,
                'timestamp':1520135639,
                'signature':'WXMkix4a6MkAEIzT+RVCu6SAXm5Rt0nPe5jqvHVGvMD5z2p4JX0RglrfRhYgRlCZfsG/VeFKZXQ5xOq4JYoHsSDN6HGFS0P3NDkGzlZy+CzBP1gelrqR/s94/vi0uXKFQqgxj1zZWE8ScHPjtFzv9dIgrnuO6eUUjCLl2sp9iPCn6scqDGss8/Oi/nu8FFa02y5QWWC0bdjuzDSfNrSSFAnSqxWZqhCQlxFxvHW9GJxt9ErcqrEMSrw19HNGsQf2ANIfCs6dQXl/00AAp897fwoCl5y2O85zD5bRFT8Hp7lwLvSAqVwkWa8I+QZZEZRTv3aUTUnAFXiYo/fffrjCqQ==',
                'to_addr':'-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
                '_hash':'85ccd39b76976efe4e201635cec939b16b1aca696249ef0e1ad454c3e7188b47'
            }
        ],
        'timestamp':1520135639,
        '_hash':'1027b1cba972122fbf1b5452c2281e9b20437d5ddd848c06628eb72fc3d74ae0',
        'signature':'Hb5gadPe7aCTgFFWDINo5t+Qs5LuOojog3WkQq86lGPRhvuseDIXblGGsvMLGPnh6Ix6Hc/8PoD2+fW9W1A1ekOw8+xIN/Xx3gvQoOf1mC+f/08Mrm3BzPNHL+h+y2h/f2kOxq8a80TK12HnSF3ClSmfpcGqZkYyrpPkjBN6dmGbf+hrDTItRXrhMZW3KewB9mnGWJnfq5wwpAVdygHVHznVdjU64ALBsszknmSQ+ivhhoGqW0YHvfmy9oC4VVYHTjUQ7nB/+19TdIHPvErtNMkJlnltfsaK9euf+mx+VgmxFR6SH+ioMLxsmIqRF6u2CEKf/wiRdNHhFW+QkJTMeA==',
        'pos_transactions':[
            {
                'from_addr':'-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
                'amount':100.0,
                'timestamp':1520135639,
                '_hash':'6a6e42224a94f3baad484073ce95f92cf59c2ec468ec8acaa3ccc65db48f6057',
                'signature':'PCp46BHA9wIkkRbLdMz4vuuUcFxH/h94lpjrNnSIyVgmpclaiRDwZq8CpRQUXr4tT8aSBymVD110Yfpizoj/POITe+2ji8ggHUcwv6ScIQ7VFmunsl1mRHfOtVtbdOqXCBZ6IsKbpwpjtAck3fGk14D5kIVKoC2/6W2s0wYgi5riVs79BzGbbj0TdKx7SLItiiHLYi8e+t+LFH6GBY03ciiLU8C0GIuPA4nl5bPrOwadkzmv9zb9q/CluNfJaNx/kJ1S9/2YXXFtIMY26kaSlKzdFjWRVgNep7I7Y5XOyGlcSWNl8NTrCf4HPgyW4pgqFB53HB9uTKmLueyjTOqcPA=='
            }
        ],
        'height':0,
        'contract_transactions':[

        ]
    }
    block = Block.from_dict(genesis_block)
    block_signable = block.get_signable()
    block_signature_bytes = Hashing.reverse_str_signature_of_data(block.signature)
    actual = Hashing.validate_signature(block_signable, block.owner, block_signature_bytes)
    expected = True
    assert actual == expected

def test_transaction():
    firstTransaction = {
        "amount":1.0,
        "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----",
        "signature":"JLhYlCLqb1hhKamCbKWfGh4Ja6eqYYCzXEUKu0uIxj5y/uyZzfu6VSexLBukUAn9+/7qvRqRmTFIWWB1qhQ4vo8tkPpGGR7TcUMi55fgZeRccBndYjso/5ZWOwdiymSkXCbeW7VppzUbLwSrm9rIDFz52p2v7xZIJcY4UruJFlNPEpbkG0tOZRnFXmice/qu8hZJ4l/l55B834jM8DxeI4sI0myk5CXJOiy6vvupjQS8HAcbpFsKnhKKF/xXIYYSGUU123Mty2u5bjhKjpTVBVL53b4WV1fBDVOfg5mMlI+PY4AssUkYBIirrxeBVuXwl+DHwwc4ZHfXKTUH9G5h0Q==",
        "_hash":"5719d7850b6128e5cc783087f48390d86993eda2acaa6905098597e3272a6884",
        "timestamp":1520135639,
        "from_addr":""
    }

    trans = Transaction.from_dict(firstTransaction)
    trans_signable = trans.get_signable()
    block_signature_bytes = Hashing.reverse_str_signature_of_data(trans.signature)
    actual = Hashing.validate_signature(trans_signable, trans.to_addr, block_signature_bytes)
    expected = True
    assert actual == expected