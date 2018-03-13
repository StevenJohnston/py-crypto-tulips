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
        'timestamp': 1520135639,
        'signature': 'KiKFu5/blurP9LdIcSMbhk9xTEK+tb1hTgEVGuTqDAyAvEAzvqMI1VRUTeLG2xu0O/MvbdPIgvJUriv4iKQwWEcbBPtaj39FP6qFUK8ydn/lm96K2R9u+WUhHp+iL3A+YKlw4z4hXIavSZHref41l2qJ4CaLEaUynpEI07ujWm2u0fdsVAT3kLgsn4dKNSE2vFHnb+IcbhRqWsjccWZ44VRgOoBUm8eNOlbxmEuwXPUcyZB9MmlMFtoXoSZWSun2BAn/2LmV/Zk6Tvph97TlnzL/8GNctbvYxFjR9hyR+Io512rFDW1SbVBnMriw4hwiG4MFai8B+Jz44AgM2jjq3g==',
        '_hash': 'f53b4f6826b46e9e21b2d6e594adc856fc8c4f7b1b186f6644861e222b6bec24',
        'contract_transactions': [],
        'transactions': [{
            'signature': 'CnDOs1IZIXXZD85WYWbs5pkxh23FGKLgeA/13qb8br4qUTJSrpxnamBD6xZALD6XucyX/qSfj9jzB4beF2B4BV2OJtyc4BWYlR+dbANHCuLyIlXrKGxZN0sh0tJcV/ODPDd6w8oqCwumIkTrqjMQfjtPpUvZFkVVh2jKEwM4vwvAycRxoyxWbFFfS+C7xk+z7FidiCVYlSYJaTJ6+GQPqRAMx+Ey2ibpU3UIzR9i2cOqEDk9nUg+N43VcYIezbx7W81T9znN+F7RBP3X2Ww5BJ4dFlc71aE4HZrOJ/uJ/G76FjCl7FHvRcDHkLZ8MMG9H41XoS8Idn4/NqFqLKQpdA==',
            'amount': 1.0,
            'to_addr': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
            '_hash': '2cb0c5c1b1a5df13a08e831fdb3d5a9fbe1be556b23681591bdf3a5371133074',
            'timestamp': 1520135639,
            'from_addr': ''
        }, {
            'signature': 'WI7tfdIVczyzqLl+HmEqLm5kQwRN1tLG63kGdlrdoZq0NlMj8mdqXsVytSgGV5JG0jRIPNs3HyCInT7niSxvD0BpACevli8M68754VeGsTbTuRras6r4ud0n0l8SOVBgj6ujlXBwNSdVCbsKSToDD7dc685uLsUw/9ZroC1pVGnnHiz2E6DimdJuBylfNkjOr5pIaOQxmL8g+1bIilPayUhLYTy2SeItSZofbj0ICspJ871sUggyHhxJrrfJUQR7xLWAXGo3qAnHczsolspHf4n3hjqswtC16GpKkqn5ilZzclk2ssG8I0Njy85PFpGwYhlyyfZaa+hNmXRZYU2UfA==',
            'amount': 10.0,
            'to_addr': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
            '_hash': 'a0cb0f7c00771e4eed4547dbce4e0789c5fd556eaac0f611e14c1103354605c1',
            'timestamp': 1520135639,
            'from_addr': ''
        }, {
            'signature': 'URF079sLoTlQ3TjedN1DQy5gyby695GLe4UDvseMb4UDYbJPst/IdUfXomyfH0y8vYf6GmEay1egPRrY/9HlCjRObah6mQpYNRvWjNF3L0tDuJfFiz74o2weyFYfv4wS8IWkDry7GPYpoYDf8uMm9dqCrrfS9EYvIanYQZdq9e72Q9w7Q3xBSGWO8jrK14vCCXD7PYXN9BynoboO1OgfvpI4VIgKgO7wZHiCqqwkzXqwf04MwHcXilOrpmVgO4mivsRTV5uc8nMKGNp2Ozn8I0O8IC8zPv9YzKCKm/O6qMz89jEVekVrHDT2aBAXTQE8xlDdlm308kUuzmpSSw9muA==',
            'amount': 100.0,
            'to_addr': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
            '_hash': '665cb4816b5963dc977bce8ca29f0b535965797a779d0ccf2080f85a8a30ff18',
            'timestamp': 1520135639,
            'from_addr': ''
        }, {
            'signature': 'PMhB1f4SWi/ZdArthq7WstOOku8R6g7GZcDMhBZC8QT0ZRMf1p6ugYJEzvxNjd0qjZoufRLzyxos50mI7esffObSaMB0wQHVcLs7x99B+PNhdA2lwiA/klzr2D1yp1bo8xXrcrL3kafxX6T4odCV6Pb4ZQRxjN9N6iL57MC8B/Nb5iN90FznvefLQb1BqtBGq0zg3+fUgn9QFd7ZP4dmzeDkYvQeU2qQ97MdFdsIe7KT30/anxkURudCxS8tlNTIo1P5tnvHYrrNyFrzmYbDKlb2sYSaqLSY+XFlAQ38wCzG724ABn37lYuMEtJvdNnK2g49foFsbxBBFONkz7dNkQ==',
            'amount': 1000.0,
            'to_addr': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
            '_hash': '92c45afc5e07459c04adb6fa6c2bb28819bd27b6c66e4a998e03b0d0c7d6b82d',
            'timestamp': 1520135639,
            'from_addr': ''
        }],
        'pos_transactions': [{
            'timestamp': 1520135639,
            'signature': 'S+BT1QrOSW55bJiKdxvVKophPX/QXhSC7JfqgzRzTsEWWL301PHWH5lKVKFXXDk3gjAv2V8SR3SSaeMnrxzRuSYwzICTi9yd454ddXkRcFOJzf+BUx+3b3vTsRliFrhnL1N3X2QP0ksN3UzBS/aKaMXDk2QYE1pqabizk+x0q0EQZwXpGHDVJCewm4GG/oUGgnX2BQHhFOuGwMCfRacuoI7r4cKh8bORlTPNlUeJjnsaNd7rJbzbKnp8mN8//7uToWhSY+8Oh/Us3J+X75DkPP1ZPuaK+Lobyg5KnMeUuhyHH2GFaCIfvmDI0JWOMbByHzJcIcFUHnzy5auwg9S4JQ==',
            'amount': 100.0,
            'from_addr': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
            '_hash': '9dd6aa857df1fe049e31c2f3f5b46f70d739f7fd8b39b9eccbb6391f05087f3c'
        }],
        'height': 0,
        'prev_block': 'LAST_BLOCK',
        'owner': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----'
    }
    actual = block.get_sendable()
    print(str(actual))
    assert actual == expected

def test_validate_rsa_block():
    genesis_block = {
        'timestamp': 1520135639,
        'signature': 'KiKFu5/blurP9LdIcSMbhk9xTEK+tb1hTgEVGuTqDAyAvEAzvqMI1VRUTeLG2xu0O/MvbdPIgvJUriv4iKQwWEcbBPtaj39FP6qFUK8ydn/lm96K2R9u+WUhHp+iL3A+YKlw4z4hXIavSZHref41l2qJ4CaLEaUynpEI07ujWm2u0fdsVAT3kLgsn4dKNSE2vFHnb+IcbhRqWsjccWZ44VRgOoBUm8eNOlbxmEuwXPUcyZB9MmlMFtoXoSZWSun2BAn/2LmV/Zk6Tvph97TlnzL/8GNctbvYxFjR9hyR+Io512rFDW1SbVBnMriw4hwiG4MFai8B+Jz44AgM2jjq3g==',
        '_hash': 'f53b4f6826b46e9e21b2d6e594adc856fc8c4f7b1b186f6644861e222b6bec24',
        'contract_transactions': [],
        'transactions': [{
            'signature': 'CnDOs1IZIXXZD85WYWbs5pkxh23FGKLgeA/13qb8br4qUTJSrpxnamBD6xZALD6XucyX/qSfj9jzB4beF2B4BV2OJtyc4BWYlR+dbANHCuLyIlXrKGxZN0sh0tJcV/ODPDd6w8oqCwumIkTrqjMQfjtPpUvZFkVVh2jKEwM4vwvAycRxoyxWbFFfS+C7xk+z7FidiCVYlSYJaTJ6+GQPqRAMx+Ey2ibpU3UIzR9i2cOqEDk9nUg+N43VcYIezbx7W81T9znN+F7RBP3X2Ww5BJ4dFlc71aE4HZrOJ/uJ/G76FjCl7FHvRcDHkLZ8MMG9H41XoS8Idn4/NqFqLKQpdA==',
            'amount': 1.0,
            'to_addr': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
            '_hash': '2cb0c5c1b1a5df13a08e831fdb3d5a9fbe1be556b23681591bdf3a5371133074',
            'timestamp': 1520135639,
            'from_addr': ''
        }, {
            'signature': 'WI7tfdIVczyzqLl+HmEqLm5kQwRN1tLG63kGdlrdoZq0NlMj8mdqXsVytSgGV5JG0jRIPNs3HyCInT7niSxvD0BpACevli8M68754VeGsTbTuRras6r4ud0n0l8SOVBgj6ujlXBwNSdVCbsKSToDD7dc685uLsUw/9ZroC1pVGnnHiz2E6DimdJuBylfNkjOr5pIaOQxmL8g+1bIilPayUhLYTy2SeItSZofbj0ICspJ871sUggyHhxJrrfJUQR7xLWAXGo3qAnHczsolspHf4n3hjqswtC16GpKkqn5ilZzclk2ssG8I0Njy85PFpGwYhlyyfZaa+hNmXRZYU2UfA==',
            'amount': 10.0,
            'to_addr': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
            '_hash': 'a0cb0f7c00771e4eed4547dbce4e0789c5fd556eaac0f611e14c1103354605c1',
            'timestamp': 1520135639,
            'from_addr': ''
        }, {
            'signature': 'URF079sLoTlQ3TjedN1DQy5gyby695GLe4UDvseMb4UDYbJPst/IdUfXomyfH0y8vYf6GmEay1egPRrY/9HlCjRObah6mQpYNRvWjNF3L0tDuJfFiz74o2weyFYfv4wS8IWkDry7GPYpoYDf8uMm9dqCrrfS9EYvIanYQZdq9e72Q9w7Q3xBSGWO8jrK14vCCXD7PYXN9BynoboO1OgfvpI4VIgKgO7wZHiCqqwkzXqwf04MwHcXilOrpmVgO4mivsRTV5uc8nMKGNp2Ozn8I0O8IC8zPv9YzKCKm/O6qMz89jEVekVrHDT2aBAXTQE8xlDdlm308kUuzmpSSw9muA==',
            'amount': 100.0,
            'to_addr': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
            '_hash': '665cb4816b5963dc977bce8ca29f0b535965797a779d0ccf2080f85a8a30ff18',
            'timestamp': 1520135639,
            'from_addr': ''
        }, {
            'signature': 'PMhB1f4SWi/ZdArthq7WstOOku8R6g7GZcDMhBZC8QT0ZRMf1p6ugYJEzvxNjd0qjZoufRLzyxos50mI7esffObSaMB0wQHVcLs7x99B+PNhdA2lwiA/klzr2D1yp1bo8xXrcrL3kafxX6T4odCV6Pb4ZQRxjN9N6iL57MC8B/Nb5iN90FznvefLQb1BqtBGq0zg3+fUgn9QFd7ZP4dmzeDkYvQeU2qQ97MdFdsIe7KT30/anxkURudCxS8tlNTIo1P5tnvHYrrNyFrzmYbDKlb2sYSaqLSY+XFlAQ38wCzG724ABn37lYuMEtJvdNnK2g49foFsbxBBFONkz7dNkQ==',
            'amount': 1000.0,
            'to_addr': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
            '_hash': '92c45afc5e07459c04adb6fa6c2bb28819bd27b6c66e4a998e03b0d0c7d6b82d',
            'timestamp': 1520135639,
            'from_addr': ''
        }],
        'pos_transactions': [{
            'timestamp': 1520135639,
            'signature': 'S+BT1QrOSW55bJiKdxvVKophPX/QXhSC7JfqgzRzTsEWWL301PHWH5lKVKFXXDk3gjAv2V8SR3SSaeMnrxzRuSYwzICTi9yd454ddXkRcFOJzf+BUx+3b3vTsRliFrhnL1N3X2QP0ksN3UzBS/aKaMXDk2QYE1pqabizk+x0q0EQZwXpGHDVJCewm4GG/oUGgnX2BQHhFOuGwMCfRacuoI7r4cKh8bORlTPNlUeJjnsaNd7rJbzbKnp8mN8//7uToWhSY+8Oh/Us3J+X75DkPP1ZPuaK+Lobyg5KnMeUuhyHH2GFaCIfvmDI0JWOMbByHzJcIcFUHnzy5auwg9S4JQ==',
            'amount': 100.0,
            'from_addr': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
            '_hash': '9dd6aa857df1fe049e31c2f3f5b46f70d739f7fd8b39b9eccbb6391f05087f3c'
        }],
        'height': 0,
        'prev_block': 'LAST_BLOCK',
        'owner': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----'
    }
    block = Block.from_dict(genesis_block)
    block_signable = block.get_signable()
    block_signature_bytes = Hashing.reverse_str_signature_of_data(block.signature)
    actual = Hashing.validate_signature(block_signable, block.owner, block_signature_bytes)
    expected = True
    print(actual)
    assert actual == expected

def test_transaction():
    firstTransaction = {
        'from_addr': '',
        '_hash': '2cb0c5c1b1a5df13a08e831fdb3d5a9fbe1be556b23681591bdf3a5371133074',
        'to_addr': '-----BEGIN PUBLIC KEY-----\nMIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBtxQbESKGGw1uYw113Tkyh\nXfMHy2jq/iXJ+17oEzjGk6qzT39evE7Zn60o9gZrmIWnvZMZRfo/fTBxTxKlWFme\n7wQEW5bM1lt5/LemQshRtKY9pcg3xneZzsyn3qy4oMLncWQEPBDiHK+L8OWiENLj\nTORn0ssrBlFi+bjG/eF/qyO9H0ljOPExcQYpjgp1bqcXhAlpSUKMIpdAwje+LWid\nbUoMxnJCOFKK5Dmvgku/Ca3eVXTV85/5VgafFRrvsG96wsRl4A+K88YU5RpbFPo8\nixWTW+67XNB0A12QFYMhjw4pvQ2mwosrgfipELs0TlCZFkr00IwRV7Qenw8tEAlZ\nAgMBAAE=\n-----END PUBLIC KEY-----',
        'timestamp': 1520135639,
        'amount': 1.0,
        'signature': 'CnDOs1IZIXXZD85WYWbs5pkxh23FGKLgeA/13qb8br4qUTJSrpxnamBD6xZALD6XucyX/qSfj9jzB4beF2B4BV2OJtyc4BWYlR+dbANHCuLyIlXrKGxZN0sh0tJcV/ODPDd6w8oqCwumIkTrqjMQfjtPpUvZFkVVh2jKEwM4vwvAycRxoyxWbFFfS+C7xk+z7FidiCVYlSYJaTJ6+GQPqRAMx+Ey2ibpU3UIzR9i2cOqEDk9nUg+N43VcYIezbx7W81T9znN+F7RBP3X2Ww5BJ4dFlc71aE4HZrOJ/uJ/G76FjCl7FHvRcDHkLZ8MMG9H41XoS8Idn4/NqFqLKQpdA=='
    }

    trans = Transaction.from_dict(firstTransaction)
    trans_signable = trans.get_signable()
    block_signature_bytes = Hashing.reverse_str_signature_of_data(trans.signature)
    actual = Hashing.validate_signature(trans_signable, trans.to_addr, block_signature_bytes)
    expected = True
    assert actual == expected