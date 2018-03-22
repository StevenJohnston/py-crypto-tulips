from crypto_tulips.services.genesis_block_service import GenesisBlockService
from crypto_tulips.dal.objects.block import Block
from crypto_tulips.hashing.crypt_hashing_wif import EcdsaHashing
from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.services.block_service import BlockService
import pytest
import json

_priv = """55a1281dfe6cf404816be8f2bb33813e2cf8ef499fb22e21cb090f8f8563a72a"""

def test_generate_from_priv():
    expected = True
    block = GenesisBlockService.generate_from_priv(_priv)
    actual = BlockService.verify_transactions(block)
    assert actual == expected

def test_validate_rsa_block():
    genesis_block = {
        "height": 0,
        "prev_block": "",
        "_hash": "1a06bafd792615929ab6c65fd9f54ef2a1a2e408f9548f5d4c32e2cfd6b10a0e",
        "contracts": [],
        "pos_transactions": [{
            "from_addr": "c8fdd9558e4e36d3549c449986c587aa16be67439ed70b8bf1f7e47e8586572f4c821059e4077a94d3e31f1cfa8bccc5c2acf86e955d30ef93633bcabcdc9f34",
            "timestamp": 1520135639,
            "_hash": "82b2704e380f4bc55c214d44f4cdd698ec3ed5471882d0ae67d80462f13434f5",
            "amount": "100.00000000",
            "signature": "2b6f4ad89868f8a820f682fb580a20b3383e9889b50736a66c8ed441ac4ebb29b7f32d6efe929b05d66de7ac0e20d0ea471f7a1e482f505f2f0df3221d720ba4"
        }],
        "contract_transactions": [],
        "timestamp": 1520135639,
        "owner": "c8fdd9558e4e36d3549c449986c587aa16be67439ed70b8bf1f7e47e8586572f4c821059e4077a94d3e31f1cfa8bccc5c2acf86e955d30ef93633bcabcdc9f34",
        "transactions": [{
            "to_addr": "c8fdd9558e4e36d3549c449986c587aa16be67439ed70b8bf1f7e47e8586572f4c821059e4077a94d3e31f1cfa8bccc5c2acf86e955d30ef93633bcabcdc9f34",
            "timestamp": 1520135639,
            "_hash": "f54029850ab8ffc3d3f1b210bee0008f1b42aa45e267925f42b80ed9eedb1c20",
            "amount": "1.00000000",
            "from_addr": "",
            "signature": "36a0131c4087dae1d0909baf5ea1b35c9955db7e775646df40d35ad6469469b21439e08263ab7a2fa03f3285fb13ce1b80b399bb6f254694e3f36b9ed5fa6a98"
        }, {
            "to_addr": "c8fdd9558e4e36d3549c449986c587aa16be67439ed70b8bf1f7e47e8586572f4c821059e4077a94d3e31f1cfa8bccc5c2acf86e955d30ef93633bcabcdc9f34",
            "timestamp": 1520135639,
            "_hash": "ac32ce4867f65d575d95109b59e713f180541cd5c76ca93dad7cea210ebfa26c",
            "amount": "10.00000000",
            "from_addr": "",
            "signature": "83abc47ca9ad48e91b63d6d4bba28786abfc7345f29f02dbf1c90b4e66f91413cf9a081314095d4bf30d508b9781d035a5816f13ea0c1f1d6b6dd59665697b15"
        }, {
            "to_addr": "c8fdd9558e4e36d3549c449986c587aa16be67439ed70b8bf1f7e47e8586572f4c821059e4077a94d3e31f1cfa8bccc5c2acf86e955d30ef93633bcabcdc9f34",
            "timestamp": 1520135639,
            "_hash": "e1e65c22699599507d2621b84a39b02ca525e5d3881c583d4d96cffdf3ceced7",
            "amount": "100.00000000",
            "from_addr": "",
            "signature": "998d03e220b28ad99b2b6d7a00cc1a06443ceea8a3a96acc896c6d8953b44d78f58a6cfbf699d5b4ed35f062cb05674d2f10718ecf44d07a300a781c21734220"
        }, {
            "to_addr": "c8fdd9558e4e36d3549c449986c587aa16be67439ed70b8bf1f7e47e8586572f4c821059e4077a94d3e31f1cfa8bccc5c2acf86e955d30ef93633bcabcdc9f34",
            "timestamp": 1520135639,
            "_hash": "b3cf3fba2d1b5e3ca6fee0b5d22a1b81f038ffd9e825119f1a7226e3e10a61ee",
            "amount": "1000.00000000",
            "from_addr": "",
            "signature": "556474088e1f4c75f24cb72db8b0be78134d10d0323c40569207baef1172c43b96596573a446389d2330d781109b76da8725d2ef29876cdd4a198fafc9cbf50f"
        }],
        "signature": "c1baa8f6d1789c2ddb803b1ad34ba742efd30aa4f77aea3ca5c86224a193596bd74299cccedbe9603af15edc7890fb403d79bd3acc72adefdd214244fad6000c"
    }
    block = Block.from_dict(genesis_block)
    block_signable = block.get_signable()
    block_signable_json = json.dumps(block_signable, sort_keys=True, separators=(',', ':'))
    actual = EcdsaHashing.verify_signature_hex(block.owner, block.signature, block_signable_json)
    expected = True
    print(actual)
    assert actual == expected

def test_transaction():
    expected = True
    time_now = 1520135639
    public = EcdsaHashing.recover_public_key_str(_priv)
    firstTransaction = Transaction('', '', '', public, 1, 1, time_now)
    firstTransaction.update_signature(_priv)
    firstTransaction.update_hash()

    trans_signable = firstTransaction.get_signable()
    trans_signable_json = json.dumps(trans_signable, sort_keys=True, separators=(',', ':'))
    actual = EcdsaHashing.verify_signature_hex(firstTransaction.from_addr, firstTransaction.signature, trans_signable_json)
    assert actual == expected