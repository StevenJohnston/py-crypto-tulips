from crypto_tulips.services.genesis_block_service import GenesisBlockService
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
        "_hash":"0e2f076c38116a8ea27c401339fbddc8f0599b8c897a2398c9618b17d74e9f2f",
        "contract_transactions":[

        ],
        "pos_transactions":[
            {
                "_hash":"2ca410f9e510fe13407c39a3e5c47083a46a2cb03ee1280a75b2bf4268035a22",
                "addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----",
                "amount":100,
                "signature":"IXFoNDcjgBmODD4kGk8dIDtOPLGn3lykzF70oR8Yg+3mbljucjJE9wX2geVjqn7oTdQsqm5eDGDaSVvg0UaO05WUVSIl96GFmvo4Z6iyKXAJ/YSIUmiyem5uePal0NeQ9uliMyxAj9XGmyaV1Ls/jlngrBbm8KPsH9cPM9HOhiP6CPd3sA/9C9J18OJ/TseQohUayVs3w0OQHpO+rFD02ohUI4Rvt0B8QMJD9sMQMEroizDX5rl27OJPFwcRpY/WciMc9bKESb/6TGr3lSSUgUWR6p6BZKIS7T7vgS/YAN7msk510f0vp3pE0RAyM3e9DJqbbnwgJCmlvWIUbiv3Fg==",
                "timestamp":1520135639.4713802
            }
        ],
        "signature":"Z0ZCgW/cMILqOweTV+eqn0yox+3L+G/h+zrTMPuaNfmrm8x7tXzTb5VsAAGfyqlV5Ok9cVPQ6EBHYKTCIdlVPsq8s15XZ6SLuSk/Rm0VpRllSPgwwyBAmOonqS2tF6O8JcuEmmUMrlZ2h/Oq+Q4CIFBrwpD7stztiy624jluHNpqA86zbYF9d7QBFQfE2ER8xwRFKEH/8cUVd5M4+JPCGuuY2Sb7XBS2wifTlJBoFOKj9EkmCCGmfe+or+0XHWWP/X0SEPYzfWEmbmesKFpe6Ej5bdZkfGlmP4pqqN7d/Iq2ich79e/B6s3b1736cr1D3nFuFFEQz6lD/ItzyUKUkg==",
        "timestamp":1520135639.4713802,
        "transactions":[
            {
                "_hash":"6daa396d275987c4fe8b5c3e4d62a0fad08ea6b700e306d93881f5a4be1c2b68",
                "amount":1.0,
                "from_addr":"",
                "signature":"B0AktTYZRD7IjLzReIzkiEwJPLFQkzHBmBaoiIln1qALujrWNivwKalhEWluHXhtW+qkiHJ6D4vgblmgDNphRTTKU7HNfoXOzlQdu2jAE8y9z1uVvBjCrvg29Zbyd97LzsHqe7XORZ4/yStpnsJ17XNn5ynKsxRaiF/kSuEFNypl4a/LTUhnSX3Xvs6PL3MJmG3qQ1ZmgH8PCmwF2r0Xoy52aBUAs5ipIdV05ZXuds/xcVLyxcdLHhqvBvJhAit2vQfROC8XFcMObWKQZbJrXsG2j9rdmE7lCyiR3nIo6DX1AdqSEomgT0ADd2t+sy/KYjR2dj0uqByLdbgIErN2vA==",
                "timestamp":1520135639.4713802,
                "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----"
            },
            {
                "_hash":"57f08afd6a94edd6f82e4c099245e8839fa84a31cd5591d865fd3cc4e7a4a65e",
                "amount":10.0,
                "from_addr":"",
                "signature":"Rw5QeuieGX7Flh4BweXOTnZlC23vMuose8jIW7XxZLcG8QyBBckmPzN4timHRmao3qmYzGCws+RFO/yYSFvO+Oy0rrlco+H4oTF2MLUoNbpXC9z4ANU/5FG8gmf7qTdetSYmvVnNFql8nHVqZXNIdYWi0r8wDeCNyDgeWUYGiu0356bjsYO6vihAPmd0YgGXIVV5pPJG0ED0xwIxjjny7c7G6ju0y9A7/ZG7o9VbA0gsp8aVheghRr2ibVLo3LZiI7wIRTrw9C0g5VwiKXQlE8Pg9xBDxmOqGbmYqH4dA23/NZrr5TDTOmJ2PfZ/M31RVJ1Jo/qVHyHcHxeCS7mZ7g==",
                "timestamp":1520135639.4713802,
                "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----"
            },
            {
                "_hash":"7a1a672301a52942b82da4ba54e6fba3a766f44804ea0804f7712678a8555df9",
                "amount":100.0,
                "from_addr":"",
                "signature":"XhW5cUeFY5X+/pwIGomVYj4X5EqNjGQyDt49LLiu9aZvnig7AOW6Q1Eh3S/aUm1I+ZhYdCbVQOID2Uy1ABzbhaHsi8O94Shcx5tEWadLUeG+J6xUck4AVJi9vKouY+/wy77rek+UizDdHTKAaCP4muRVFFJ5gUfwx8L4quM3Cs9HKnlQ6P2hR2CFLe1Z3lIBct+lmMGDwToyAYOyK4DHICQKdFQJR0AUurBvPfdhERJJ9ty5+TgQ9ABLvG/B4J/f2fAnodeUcQ2rlDijzUxkhD1Vbum3meltuU5WFMAtnhgs4A+FgNLOsNiTKAa5r8Wy38sDLLy4uFIqKkD47+ccVQ==",
                "timestamp":1520135639.4713802,
                "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----"
            },
            {
                "_hash":"89c254e3278ce871afc0413a6f89cf95589babc5cbd68964b121be1917ea4340",
                "amount":1000.0,
                "from_addr":"",
                "signature":"GIU7CM/ehpK9e/CRsoUCEq9PLFq3cR5cKufsCpYShjlExYulVYBnkTACxYAk5l+ZcnpCmAY4EQS5aRLd80O28ME3yXM1fTj+d0cob3WHPA6aRgsQBmTzS0rLo65tgnf+mfYuR5wWIn2ansNd8dJ0s0ABIDlFBCG7QjVx+S++oHtSB42diDJ3MYYuDPuXb/WNqBqBfy3+0U7Xm0jwZ36yLeKDSuWrmX0vzognyk8HfI8nrszJr8B8sDZGjy/2K2ULqj4w86W7VPrHdXhOJZukC3UjPPkC2oD6HXGrillfgOxrOCSLl8l7MtaTY0FikGK83ZXDUJWHvejNKEYlnBN/2Q==",
                "timestamp":1520135639.4713802,
                "to_addr":"-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----"
            }
        ]
    }
    actual = block.get_sendable()

    assert actual == expected