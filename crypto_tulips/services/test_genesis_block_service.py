from crypto_tulips.services.genesis_block_service import GenesisBlockService
from crypto_tulips.dal.objects.block import Block
from crypto_tulips.hashing.crypt_hashing_wif import EcdsaHashing
from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.services.block_service import BlockService
from crypto_tulips.services.pos_service import POSService
from crypto_tulips.dal.services.block_service import BlockService as DalBlockService
import pytest
import json
import redis

_priv = """55a1281dfe6cf404816be8f2bb33813e2cf8ef499fb22e21cb090f8f8563a72a"""
_priv_den = """4a7351205a7bfaa9726a67cba6f331f1b03ee1e904250f95f81f82e775bb55c1"""

def test_generate_from_priv():
    expected = True
    block = GenesisBlockService.generate_from_priv(_priv)
    actual = BlockService.verify_transactions(block)
    assert actual == expected

def test_validate_rsa_block():
    genesis_block = {
        "height": 0,
        "prev_block": "",
        "_hash": "036850bec30839508bf16badc1efc5c0a31eb82f8b23c524c7ea8cd3d0c8b81f",
        "terminated_contracts": [],
        "signed_contracts": [],
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
        "signature": "3a3a88935574c820fa70a2408f594585d03988df1980f6c0129b84ee129c322c683de1a7f8be6087d468abbbeb32f2a49eb0ac0c64a9b8de57d43a480ebf4dfc"
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

def test_pos_author():
    expected = 'c8fdd9558e4e36d3549c449986c587aa16be67439ed70b8bf1f7e47e8586572f4c821059e4077a94d3e31f1cfa8bccc5c2acf86e955d30ef93633bcabcdc9f34'
    r = redis.Redis()
    r.flushdb()
    genesis_block = {
        "height": 0,
        "prev_block": "",
        "_hash": "036850bec30839508bf16badc1efc5c0a31eb82f8b23c524c7ea8cd3d0c8b81f",
        "terminated_contracts": [],
        "signed_contracts": [],
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
        "signature": "3a3a88935574c820fa70a2408f594585d03988df1980f6c0129b84ee129c322c683de1a7f8be6087d468abbbeb32f2a49eb0ac0c64a9b8de57d43a480ebf4dfc"
    }
    block = Block.from_dict(genesis_block)
    dal_block_service = DalBlockService()
    dal_block_service.store_block(block)
    actual = POSService.get_next_block_author(block)
    print(actual)
    assert actual == expected

def test_pos_author_two_blocks():
    expected = '23f48768a8e871db2ed721a1e0d250ce41a1fe49765e01e798db0816b781169115e01d3a702934276fa4536bb59527ba0cd7c2fd9eb9e3c13785750c4a9c31d0'
    r = redis.Redis()
    r.flushdb()
    genesis_block = {
        "height": 0,
        "prev_block": "",
        "_hash": "036850bec30839508bf16badc1efc5c0a31eb82f8b23c524c7ea8cd3d0c8b81f",
        "terminated_contracts": [],
        "signed_contracts": [],
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
        "signature": "3a3a88935574c820fa70a2408f594585d03988df1980f6c0129b84ee129c322c683de1a7f8be6087d468abbbeb32f2a49eb0ac0c64a9b8de57d43a480ebf4dfc"
    }

    second_block = {
        '_hash': '1048eb4638a45b140a51e7a6d92e972010878d9f05be6fe5c0d20d17b4c26e7a',
        'height': 1,
        'contract_transactions': [],
        'transactions': [{
            'amount': '1.00000000',
            'to_addr': '23f48768a8e871db2ed721a1e0d250ce41a1fe49765e01e798db0816b781169115e01d3a702934276fa4536bb59527ba0cd7c2fd9eb9e3c13785750c4a9c31d0',
            'timestamp': 1520135639,
            '_hash': '188b1e41db5661c87777d7ea3d96cbe0b8858df2cd9c020abb4a424f91c22087',
            'from_addr': '',
            'signature': 'c3d5bdf941cf4a4a95483174e085da38cc4f7decb59cf07ce3ac80623de7e842f46b1d7f6880c358fe4b0ead324ba5af4176743bfd390daf34f79a6ed5e51de8'
        }, {
            'amount': '10.00000000',
            'to_addr': '23f48768a8e871db2ed721a1e0d250ce41a1fe49765e01e798db0816b781169115e01d3a702934276fa4536bb59527ba0cd7c2fd9eb9e3c13785750c4a9c31d0',
            'timestamp': 1520135639,
            '_hash': '004186e14438ea30c3d6ee69dfdc4b66d589e6d5d85c751bfae1220ecdbe8954',
            'from_addr': '',
            'signature': '8d02e40b4923aa1e9869ab48c8de423a510f966e6edb3def1013cf243fe9b7c6ab9c77fa485a02ff03fc769f9e1c36f9085210058d729ed4d71194d7e6c98335'
        }, {
            'amount': '100.00000000',
            'to_addr': '23f48768a8e871db2ed721a1e0d250ce41a1fe49765e01e798db0816b781169115e01d3a702934276fa4536bb59527ba0cd7c2fd9eb9e3c13785750c4a9c31d0',
            'timestamp': 1520135639,
            '_hash': '9463a74fa3e79a5a7f0dee4c8b0d06cdf5624dc529b2d1915cdffabfcdece8ff',
            'from_addr': '',
            'signature': '26962120d2621f61ce4281169d97a06fc508d0246e9779dc3d50a04382f469389166b040d54fab4f00b45fa4ef9ff69296709b1165afb1e695ff893124325e47'
        }, {
            'amount': '1000.00000000',
            'to_addr': '23f48768a8e871db2ed721a1e0d250ce41a1fe49765e01e798db0816b781169115e01d3a702934276fa4536bb59527ba0cd7c2fd9eb9e3c13785750c4a9c31d0',
            'timestamp': 1520135639,
            '_hash': '79ba95186cf2068aa7868057661e315856e44d43a7b3e1fdebfdd9cf7e9679d1',
            'from_addr': '',
            'signature': '5b8dfb857bbee98edc869948bcd90b361d2a9ac48704981cd4a4697ae090b22bf3389b2a0d17ed198f7c9aaa98baa68db5d869279a5065c6ebb44dcb628d06f7'
        }],
        'timestamp': 1520135642,
        'terminated_contracts': [],
        'signed_contracts': [],
        'contracts': [],
        'prev_block': '036850bec30839508bf16badc1efc5c0a31eb82f8b23c524c7ea8cd3d0c8b81f',
        'signature': '829ac7859ca675ea410a781cf30b39fd7864daeda054c50893001da164d04cfacab103dc57cb9d39e545b8533dbd8d54954c3399c01bc356c06801e48242d531',
        'owner': '23f48768a8e871db2ed721a1e0d250ce41a1fe49765e01e798db0816b781169115e01d3a702934276fa4536bb59527ba0cd7c2fd9eb9e3c13785750c4a9c31d0',
        'pos_transactions': [{
            '_hash': '1d1d4247b7611a28e66b114a14445e894dfb7086accb8d02f6f1ac06ff15e049',
            'amount': '100.00000000',
            'from_addr': '23f48768a8e871db2ed721a1e0d250ce41a1fe49765e01e798db0816b781169115e01d3a702934276fa4536bb59527ba0cd7c2fd9eb9e3c13785750c4a9c31d0',
            'signature': 'b7e348c8ebe6e483279a22d1426d31122f14a4ea46b27b9fa85d2cd91b533abc463cafd85ddf524f3677daabf888a146f91721cac26a17568a768a3c18956a15',
            'timestamp': 1520135639
        }]
    }
    dal_block_service = DalBlockService()

    block = Block.from_dict(genesis_block)
    dal_block_service.store_block(block)

    block = Block.from_dict(second_block)
    dal_block_service.store_block(block)

    actual = POSService.get_next_block_author(block)
    assert actual == expected

@pytest.mark.last
def end_closing():
    r = redis.Redis()
    r.flushdb()