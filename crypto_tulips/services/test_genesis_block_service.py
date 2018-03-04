from crypto_tulips.services.genesis_block_service import GenesisBlockService
from crypto_tulips.dal.objects.block import Block
from crypto_tulips.hashing.crypt_hashing import Hashing
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
        "pos_transactions":[  
            {  
                "amount":100,
                "_hash":"2ca410f9e510fe13407c39a3e5c47083a46a2cb03ee1280a75b2bf4268035a22",
                "timestamp":1520135639.4713802,
                "signature":"IXFoNDcjgBmODD4kGk8dIDtOPLGn3lykzF70oR8Yg+3mbljucjJE9wX2geVjqn7oTdQsqm5eDGDaSVvg0UaO05WUVSIl96GFmvo4Z6iyKXAJ/YSIUmiyem5uePal0NeQ9uliMyxAj9XGmyaV1Ls/jlngrBbm8KPsH9cPM9HOhiP6CPd3sA/9C9J18OJ/TseQohUayVs3w0OQHpO+rFD02ohUI4Rvt0B8QMJD9sMQMEroizDX5rl27OJPFwcRpY/WciMc9bKESb/6TGr3lSSUgUWR6p6BZKIS7T7vgS/YAN7msk510f0vp3pE0RAyM3e9DJqbbnwgJCmlvWIUbiv3Fg==",
                "addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----"
            }
        ],
        "timestamp":1520135639,
        "signature":"Ggwyy98QpexFpfwhXGaV+bY+49sIptebTt+gWDKvOa5V2x7gBmVy8n/yTcX9BAtvwwcBKVK0GFVp2eXxdPqYeg5nCg2DJd86D/Q+jaFPjLtsWw56N4lZQKKygOKXanexDmFdc90oIZjakt90039qC0S+7pWfT0jaGtUVzF4zuf2PPRyXDCkHv9VqORAMGELAgTHaU+y4pJY47MPuyPxy1/4VmwQJYtazBoOdZhkAhRig1jgwzXA0B//byvWrW2gI1KJsEMEMui1Td2Fo/irw+fTvvMW1T3iJzN3n4GG0qbqAFtkOAfp/Ffk4mWO/PsDY3LcchLem/kIUNqV9tr57LQ==",
        "contract_transactions":[  

        ],
        "height":0,
        "_hash":"b663cd85dab5964be29084d7fbc9b7f40b597c3b0d3d77e7d0c394e3a7c6e174",
        "transactions":[  
            {  
                "amount":1.0,
                "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----",
                "signature":"JLhYlCLqb1hhKamCbKWfGh4Ja6eqYYCzXEUKu0uIxj5y/uyZzfu6VSexLBukUAn9+/7qvRqRmTFIWWB1qhQ4vo8tkPpGGR7TcUMi55fgZeRccBndYjso/5ZWOwdiymSkXCbeW7VppzUbLwSrm9rIDFz52p2v7xZIJcY4UruJFlNPEpbkG0tOZRnFXmice/qu8hZJ4l/l55B834jM8DxeI4sI0myk5CXJOiy6vvupjQS8HAcbpFsKnhKKF/xXIYYSGUU123Mty2u5bjhKjpTVBVL53b4WV1fBDVOfg5mMlI+PY4AssUkYBIirrxeBVuXwl+DHwwc4ZHfXKTUH9G5h0Q==",
                "_hash":"5719d7850b6128e5cc783087f48390d86993eda2acaa6905098597e3272a6884",
                "timestamp":1520135639,
                "from_addr":""
            },
            {  
                "amount":10.0,
                "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----",
                "signature":"UG6PAQhWjOSfTIo6g8EAe4fdyh1EcqPTx+1YaOE02+AABrmph4lhnIjL+RYEl6dF8mUZPs8ekV6dx/uVP58KnelYrciukZ6HKnd4k+jOF0K5Le3UlObADs7WJ5N4QzJaPOEvp5VMNOYF0YR/5QU7dxDVoTAdPGaooiYt8YemLl4qEmNTpOznLMZsal3PMiorp/H82JrQN2c2yAvWFXDFs9hyDL1I9Ul4iMtmjT2y9TpGF2MXF+JDwurqLS+2su3L8gx5scbe+TyrdpggeigVw173qgsoEbQkzxdZUGw6Fl6Ek2drCh1oDC7KKX6APmsOnCF+5y2x7rXYzTgca84y3g==",
                "_hash":"cc2f9b562d42c97b7708a9d2a5e74d8f11dc3d7840b700a49caaeb1b55072618",
                "timestamp":1520135639,
                "from_addr":""
            },
            {  
                "amount":100.0,
                "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----",
                "signature":"FHXNlrfLsNznUZ1xc6gwgCXVaHZ2Ja0299UX6iDxpkO9ZXKkMvJ2Yl3qmW2MO2U9DzDrM/gohQZ2hCWEPTPEWFFS7pNO3t9PBOCWLusSwD/FBoJDAh3qhcSkQuvD+He8zUOp+7tb6839qqrecgWQ4pPnG5diFt2HfdM6kTUO/VnEcgbcGbHeAiOkjVbhAXnKzQSR/V6rQCQxNaEBSoLbq15LuMiVRMEj6xV97aFAno1gPI2yWehfyg+yUmgcojyLPMxlOVS0wI9SWMip8S9smIEijIjePdmKTT+Dqa1lspHIV9GTJGLd1qfamKPZG3rvsvbXP+k+0Chon0jxsvl9zA==",
                "_hash":"50ef5c63eb31de177cb3ff7013b1f27855ca08ee8a82258ae49fd55d9d58d531",
                "timestamp":1520135639,
                "from_addr":""
            },
            {  
                "amount":1000.0,
                "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----",
                "signature":"WXMkix4a6MkAEIzT+RVCu6SAXm5Rt0nPe5jqvHVGvMD5z2p4JX0RglrfRhYgRlCZfsG/VeFKZXQ5xOq4JYoHsSDN6HGFS0P3NDkGzlZy+CzBP1gelrqR/s94/vi0uXKFQqgxj1zZWE8ScHPjtFzv9dIgrnuO6eUUjCLl2sp9iPCn6scqDGss8/Oi/nu8FFa02y5QWWC0bdjuzDSfNrSSFAnSqxWZqhCQlxFxvHW9GJxt9ErcqrEMSrw19HNGsQf2ANIfCs6dQXl/00AAp897fwoCl5y2O85zD5bRFT8Hp7lwLvSAqVwkWa8I+QZZEZRTv3aUTUnAFXiYo/fffrjCqQ==",
                "_hash":"85ccd39b76976efe4e201635cec939b16b1aca696249ef0e1ad454c3e7188b47",
                "timestamp":1520135639,
                "from_addr":""
            }
        ],
        "owner":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----"
    }
    actual = block.get_sendable()
    assert actual == expected

def test_validate_rsa_block():

    genesis_block = {  
        "pos_transactions":[  
            {  
                "amount":100,
                "_hash":"2ca410f9e510fe13407c39a3e5c47083a46a2cb03ee1280a75b2bf4268035a22",
                "timestamp":1520135639.4713802,
                "signature":"IXFoNDcjgBmODD4kGk8dIDtOPLGn3lykzF70oR8Yg+3mbljucjJE9wX2geVjqn7oTdQsqm5eDGDaSVvg0UaO05WUVSIl96GFmvo4Z6iyKXAJ/YSIUmiyem5uePal0NeQ9uliMyxAj9XGmyaV1Ls/jlngrBbm8KPsH9cPM9HOhiP6CPd3sA/9C9J18OJ/TseQohUayVs3w0OQHpO+rFD02ohUI4Rvt0B8QMJD9sMQMEroizDX5rl27OJPFwcRpY/WciMc9bKESb/6TGr3lSSUgUWR6p6BZKIS7T7vgS/YAN7msk510f0vp3pE0RAyM3e9DJqbbnwgJCmlvWIUbiv3Fg==",
                "addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----"
            }
        ],
        "timestamp":1520135639,
        "signature":"Ggwyy98QpexFpfwhXGaV+bY+49sIptebTt+gWDKvOa5V2x7gBmVy8n/yTcX9BAtvwwcBKVK0GFVp2eXxdPqYeg5nCg2DJd86D/Q+jaFPjLtsWw56N4lZQKKygOKXanexDmFdc90oIZjakt90039qC0S+7pWfT0jaGtUVzF4zuf2PPRyXDCkHv9VqORAMGELAgTHaU+y4pJY47MPuyPxy1/4VmwQJYtazBoOdZhkAhRig1jgwzXA0B//byvWrW2gI1KJsEMEMui1Td2Fo/irw+fTvvMW1T3iJzN3n4GG0qbqAFtkOAfp/Ffk4mWO/PsDY3LcchLem/kIUNqV9tr57LQ==",
        "contract_transactions":[  

        ],
        "height":0,
        "_hash":"b663cd85dab5964be29084d7fbc9b7f40b597c3b0d3d77e7d0c394e3a7c6e174",
        "transactions":[  
            {  
                "amount":1.0,
                "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----",
                "signature":"JLhYlCLqb1hhKamCbKWfGh4Ja6eqYYCzXEUKu0uIxj5y/uyZzfu6VSexLBukUAn9+/7qvRqRmTFIWWB1qhQ4vo8tkPpGGR7TcUMi55fgZeRccBndYjso/5ZWOwdiymSkXCbeW7VppzUbLwSrm9rIDFz52p2v7xZIJcY4UruJFlNPEpbkG0tOZRnFXmice/qu8hZJ4l/l55B834jM8DxeI4sI0myk5CXJOiy6vvupjQS8HAcbpFsKnhKKF/xXIYYSGUU123Mty2u5bjhKjpTVBVL53b4WV1fBDVOfg5mMlI+PY4AssUkYBIirrxeBVuXwl+DHwwc4ZHfXKTUH9G5h0Q==",
                "_hash":"5719d7850b6128e5cc783087f48390d86993eda2acaa6905098597e3272a6884",
                "timestamp":1520135639,
                "from_addr":""
            },
            {  
                "amount":10.0,
                "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----",
                "signature":"UG6PAQhWjOSfTIo6g8EAe4fdyh1EcqPTx+1YaOE02+AABrmph4lhnIjL+RYEl6dF8mUZPs8ekV6dx/uVP58KnelYrciukZ6HKnd4k+jOF0K5Le3UlObADs7WJ5N4QzJaPOEvp5VMNOYF0YR/5QU7dxDVoTAdPGaooiYt8YemLl4qEmNTpOznLMZsal3PMiorp/H82JrQN2c2yAvWFXDFs9hyDL1I9Ul4iMtmjT2y9TpGF2MXF+JDwurqLS+2su3L8gx5scbe+TyrdpggeigVw173qgsoEbQkzxdZUGw6Fl6Ek2drCh1oDC7KKX6APmsOnCF+5y2x7rXYzTgca84y3g==",
                "_hash":"cc2f9b562d42c97b7708a9d2a5e74d8f11dc3d7840b700a49caaeb1b55072618",
                "timestamp":1520135639,
                "from_addr":""
            },
            {  
                "amount":100.0,
                "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----",
                "signature":"FHXNlrfLsNznUZ1xc6gwgCXVaHZ2Ja0299UX6iDxpkO9ZXKkMvJ2Yl3qmW2MO2U9DzDrM/gohQZ2hCWEPTPEWFFS7pNO3t9PBOCWLusSwD/FBoJDAh3qhcSkQuvD+He8zUOp+7tb6839qqrecgWQ4pPnG5diFt2HfdM6kTUO/VnEcgbcGbHeAiOkjVbhAXnKzQSR/V6rQCQxNaEBSoLbq15LuMiVRMEj6xV97aFAno1gPI2yWehfyg+yUmgcojyLPMxlOVS0wI9SWMip8S9smIEijIjePdmKTT+Dqa1lspHIV9GTJGLd1qfamKPZG3rvsvbXP+k+0Chon0jxsvl9zA==",
                "_hash":"50ef5c63eb31de177cb3ff7013b1f27855ca08ee8a82258ae49fd55d9d58d531",
                "timestamp":1520135639,
                "from_addr":""
            },
            {  
                "amount":1000.0,
                "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----",
                "signature":"WXMkix4a6MkAEIzT+RVCu6SAXm5Rt0nPe5jqvHVGvMD5z2p4JX0RglrfRhYgRlCZfsG/VeFKZXQ5xOq4JYoHsSDN6HGFS0P3NDkGzlZy+CzBP1gelrqR/s94/vi0uXKFQqgxj1zZWE8ScHPjtFzv9dIgrnuO6eUUjCLl2sp9iPCn6scqDGss8/Oi/nu8FFa02y5QWWC0bdjuzDSfNrSSFAnSqxWZqhCQlxFxvHW9GJxt9ErcqrEMSrw19HNGsQf2ANIfCs6dQXl/00AAp897fwoCl5y2O85zD5bRFT8Hp7lwLvSAqVwkWa8I+QZZEZRTv3aUTUnAFXiYo/fffrjCqQ==",
                "_hash":"85ccd39b76976efe4e201635cec939b16b1aca696249ef0e1ad454c3e7188b47",
                "timestamp":1520135639,
                "from_addr":""
            }
        ],
        "owner":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----"
    }
    block = Block.from_dict(genesis_block)
    block_signable = block.get_signable()
    block_signature_bytes = Hashing.reverse_str_signature_of_data(block.signature)
    actual = Hashing.validate_signature(block_signable, block.owner, block_signature_bytes)
    expected = True
    assert actual == expected