import sys
import json
import time
import threading
import socket
from .dal.services import redis_service
from .node import bootstrap, node
from .p2p import message
from .hashing.crypt_hashing import Hashing
from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.dal.objects.block import Block
from crypto_tulips.p2p.message import Message

from crypto_tulips.services.transaction_service import TransactionService
from crypto_tulips.services.block_service import BlockService


from crypto_tulips.services.base_transaction_service import BaseTransactionService

denys_private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAzjo14F/L8Yu009jtTR4BYi28UCoBTA/zOoweOI9vK3BBB4lw
7eDywVuZuTesUHKC2Se3sqGjh6Oiju7xszoevR2zf1bpb0znT1HlYlCx+jVo/cBY
rU4eCTekH3EwryTxNjEWdDGgDHaSlS1hywo4koMBgwpgn0G6UKleHKMJyWh4CK37
krENp1Q+1CQHGre3KOJN6YB1r+M+8WYsZ38elGCZPqo0Tguv4Dv7K9iWVQz1nASE
rxXoJga51u6ryuhOBAHvEnmQCrKTgitRw2eIKJ0oSsY+R60kI7nqqy62hGsrz8/u
EYOWj+PPecVYsMCcX8+oCtKTz8Zho+m/jqmg/QIDAQABAoIBACItoI86oTS7iDES
AyYkQmtwlASfKY7fF9sMrNeH4g9Lb+OdYjNydBkaoswBD5RXnhr6S6YVxuHsez0A
Gduv1rdWDFEe6Noy3yUUuBUGtbB3mJpxfeDfEPhLGe7CFiT41Oc71HJWZSWboyiJ
GGuLmpuhjacXmbLbNFM49ql9Vdpko1DwAdyXRduRVDWMnn0Zy5GNHUgACO4T3aFk
h3tr6goU/hFR5pZlvEGmmzWWk/Nu5H1A8H0G3C4K+i15W0zmCn5rq917Zgo5eSPo
0CpL1OVaFw1gYhwqJ7RjYDqpNzvbqwyG/tejJWARkOZ/eYOw8dEZfAN8sG+w+BAs
pHRh3OECgYEA4olgvfEdcIRKpFPv3gp21x4sdc0tQCiLDBtzOjqXV6y/wZmS//bb
eCQ8z3MxioM9l1hIet+aJyIkJ4rQjnc/vVBZwjgASVaq4vn0SvwZyYIoQaF1ASLw
agCdD8cyHsLuSxILL7N43vfQS4ME6i4pKBhSmkMH89WxcMOTd6SWKU0CgYEA6Qyg
58boUuKMB9Gm9GdxKkEFm3ax3aWu6uhIRT9KwgmsdWZfe4NutWXUd1bkLDcvo752
aIl8UJRHodq2VOXLA7vL2kkvaKz+hjQ86saAnWy5OC1g8r7K/V48IQVNr6RJmstR
54Q8ivLI6DENw0wlphSeUcp2PHUg6IF6Dm2D/nECgYEAsFUo5ZC6TqvbAgCIFLjm
eln1V5jm4Srt2PXBApE63rcL6CGnh/BaMzFZ2EydQmkX1yeT+3jzoAR2SgVGg66V
AcJ6q7A1oOCCUf0oR/nmBLF4rmWEEudkZc6mcvKls8YeAHdCF9ZGfqA9FZodiD94
L8qG+aa1mPo8jT7fGeEWNX0CgYEA2W5v3W+GKHa3wT/IrfSo74xUx/RZBHvlk8N+
UiU4AYt2/N2zrhA1RUcpkOJf5iTi7LnxzZyggKmnn4noXZM781LOYe2wLtBgdCPe
xgjHzJi4woIMFs8NopC+Nuy0y2/TQHn8A64rslPMQF4sAg9UfPx1rcfgwo1hU6wh
jb59zPECgYEArEuv93e44y1DOR7oAWmexSQmuckSphezxeQMzOu14ck7WKgSjvDV
M1+eVGQ3zpEQ3t95vVWxnljDga/SnwDl6YMZZLqbuYaJkZCVJi8AZq0oOchbRjQL
y4mnpTZMzqIHBJ2nu0C8thwJ9SqWATT5cENzZhYRrYfBeMwrgBGmTuc=
-----END RSA PRIVATE KEY-----"""

william_private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEApDDm3fScenXUABItek4rBidvh3rsKBJeQ2BQzNqPgcaCArBL
cnMMFq7UXDGG46e0mbkM+zmcEqStABujccCQyq3jggYPqGnPyRMHcQiu8s2Nr3r1
9+j8Yb8qWT2fYI55TAqivj5bWfMGsdx6plXQNjRB6LaDMogAHwipu1RkHe/9FaPs
f9yiFhxTCyddCclaHo3789CCCwsEZ40UcI2q1VoZbI6c0VcoHGuN8tuTtIwmaSop
ik9rrKw7XsiQgvCWzy7nTIJTgucI0j3Uu0T9X+PHQgbb6+kxs65c5luqaGWvAALn
zvQ2mK2li4IJ0BTULxugfSX+TQnBe8hLjBoiJQIDAQABAoIBAEBapnKCiL565mAs
v8R7VOOxm0Y3yM4f/PBdlO3mEG9mNdkF7lxqeWd+mN+Vze/28JN783mYZ/LqtqAf
NR3Fwzqdk1mINKTm7Dk8iyMjqyahqJIKGNRVbm6FdfzKaWh4D1TdqlH0sOt9lLcr
2qrNYbGNI/QpbRzmL136kERLXH5ay9oN8gP0/L/j8pPF5SONG+z8M48jtc+csc7V
hnFWSM/YbOzBOLcuuwcV373kRfMosdBX1AX1PBesJwoyVwgS7rc9jTnphkS/qY44
5hF/nC8RJgMBJDQX/epG2XefdX4MPmeLfAFl2jbAnv+GpoQaaj3dABVtqGSt9YIR
B950lTUCgYEAvYHMQdffc8hfEhQg9D7zEsan3UuKrSBEED6q82HU78C59zy6Lrio
TsH87fFfB/o+aUIzIMloqNud7wG4JQoEXwvhZdNJCrgC73uPNR6desQKLb3aY6LZ
dSfp2lR1SVVW5Yx4DlF96wOOJl1XHGwPa9rFAjgc0SQGl8VHsJGAwmMCgYEA3c0h
OdcwRSrNELtNo15pu5jqqznnuNbcG499xHaryxMtlcrKrbI8mGA7v+jj048vCyB4
ewmKvkNVxK5fv3kF0qos6/ymTVMMidt8eyHGcDHRKFbi1ohiYrLY35bN0k34Xlt+
xm0RuI5eHdHa2+cRA7+cguDjhrFLsc9kc6NC69cCgYEAtigUwVmSZUW99K+6eWwk
0/B2HKXnN8CjDAZg5i8ssgRL/RW3VP+UcJfQ2pq/oPhuk1jZsnNHEcCAT+QUMC4v
w3i1AN6WACKeV7oqDoJOF1pm+k7apBk983oZNA8o6gOI0n8yS3kTkxpIwiHIgP5x
2FdiNV7gfDunxq0P2u4RmUcCgYEA23rH3SeOUXNoFp1x1y5u7D8GQEd9gE/E4NTd
/BH+L2ab3jUc2EKeaZ4Yoe+/ujJet+D6t62aiGmzLnvqrVsBoxPYffC1U6DRsHzr
siCa75ysPwGzV9z/lnEp4B6nLusO0bgyPAHj3j+q7FEkBCSjlpT+OBh3rWo14A68
dR1h9GMCgYBhxLj+WN642MGMjc08CKK1mUUEpJa5yO3Mtpwiht8bD/ZxSnKhTblr
6/CSG4T9b6wh7y05FJ29sfTj6W7GbF6GgQ3oXk9DYDNCEjnOws7eF78ITQ6n2XrU
pHLKS94V6h1Ircz8nbDYBq6Siyl+FFX34iBqBBn7Syz3R+uRDaFjCg==
-----END RSA PRIVATE KEY-----"""

matt_private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAuEeT+FJAeLUyBNgQMB7oU8E8QS2IsAmFDJWGTbV6QnWCpXAe
e1d624nER1aGCE7C/y3WT0Vvq5OPteDwwKIQr9m4Thy269vUP8OS5mrgmFDvLSr+
n2OGj7/gRPZBLaKYGEQpmYOXAojsjTQHikqheUQmqo0EbJMQc/M9mMLcmGZ0DtkU
v4vaVWCKD2S1Y6uz8r9TUlr/Ajun+HkQjRZiL0958gQ8+dB1aXbbwk7hYUk2Mp01
HZBgAK8uPNCypniCqh+ZPiU+Y36QPe7fWsZoXFu9ZoTWinMpF3pE83RYq//id5D3
6V1v0Eln3dCuvZ5eTHoKnrTGrFIzPR4pXop6zwIDAQABAoIBADuoqKXu8wJhHuVk
kbESgIKE/53WQPdEzbcqPUWxJ/iWFIq8xpGF27dxXYL+5vuPjB+S1lvpjeKNLixi
u26RyTc1FC7tquamz4spJMjF9xo4sYX88lvlm620H8YTtzwv9G9+ub0CVgQzEeoQ
2xQRXz9kKeRzLOh9oAj5yYpII6SOkOumRmTSkSg+Kd/YCzYyny2PapqaEJCc5H5d
i4H77vRhD7sjwq3ngHbXlqBqWnSzvC3DxB9UpeO7R3eS94WVRBZsmrXU1RDeCz4H
TriOEHTtzSOS2WfnjR9ekr739OpZ/wyT3dEy9T4mv8MmJuULhew34HoWtvuuISCB
NR242ckCgYEAv5NZ9I5WlAHzTDLqqC9z7THT4eThKGinWYBwYnznVEAPN7zDdeTW
kTD1GajvMOxhV77UKitjBqqiXfl5x5MDCNPLiHQ3QfxDV938+gbd3xrvrHYoFKQK
zSYzUfvV+loPs+bYAkSOOfA+zyP9iVMzRAVTAP4Eh1g0mbdwEyjm4KUCgYEA9kAe
UkOb4eqn0dYI3JaFGf5KjkbYYkPxXmSCz7uDRkECNwhcwqt+qLha/DIlJcim8cBk
SFwX7fVBlkChrUGc9Y0ziNmrQFNC2C91ORP/mAACpYAjdQs7pJqKMLzTWcqrbRht
cnCE2w352a1i0CTzVoN1sr4HuTl8LHnW5dnFP2MCgYAOq984vmnc/eU/Eass5C1x
nd5HL3sa2CDw1shEkqI4ros7zoX9kl/oUKKEq45d5cxypteivx3fVdQHdGKiKR0T
YPz2X0gYEpSptwN3tmzpeCugvo/FPObi3SkS/0Fc4ebP9T7XtZ5ay45T2MLC8I89
h1ba/ZklMFke6JB5tykvTQKBgF5ugDIz0xdzkR+a4JMW9bveFGEzMc+dFnaIPNHE
qrbKPzszbb8JXOz+pYWJBU3UAJE8ojhNeK+8GYaxCk8Slkpj95tHPbDRPRUCPgXB
cYasmlc1KGO+BwU8bjn6b2JDojGX6IC2PXxzg5jCMN55DQfkKcJ9tSCGtuOnZY2H
UWjZAoGAcmQlDeVmOleFSVQYy2fnP0jsEWbrO8SnkvqDvO583+wHEO0ednRGyHmU
dgMfTbcqL8dIoA+eNFf/w/RiYV3Wk5AKhIHY+BxVA2X2WzY6+Kkd9LWuc3mibPgt
Zkoqjm1jGXbp5IKFS/L9LIONbMfSSJIQIa9cE9ogmRKUqT+oiR4=
-----END RSA PRIVATE KEY-----"""

steven_private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAlna+RN5cJIoWJHtF82QBhg4/cghZNqMxtpI9PnWp2WV8zQ4t
+5TzKHe/wXpPKwoN3iKAsn6vrsGBug6LUmpFBnADfx8kg+WTBIZM+3qfMOlR6Bud
Y8l/wngJ59G8s5Bhuj8yrjURU3qLdQEAe+q2gRPCV0EKSZWW0wOAUjPuinoRBelR
68p85d5m+KoSaXCmt00jy+gGkmpPBga1+zzgA/pOSUexwQ2cDZSfIwnOmXbmfPLk
l2VsqonFijDrXtT/6MV8cOVT80swZMqqLAtqDlnbxJpsIdZzJVnZe+2lLJee2X56
OuZLbJ4b/ZY5pOXSnETrMLEjz9H2m3o6eZ/7FQIDAQABAoIBACJ/+aKq5a/PJcKZ
rXFgZeUKEUwhU+tuQfDd2UMgEaDyX0pZTPvZrGOECajgVZTFymY7vQywdbH5VriF
qzZrfYY7WuHkDyhbFHm+HZqwBB5f8VLqOg1uX2gExCiuc7ksiuv8n69IJb/hYmai
oyzGpbA1CqOdGzHCJgIeVGcE11ZSyt/PXt8IrpQiv0PMmvJr9v/O6mb1AC7aPA7Q
hhJiF0fPLFRJX4Vp3RXbsQUruCFolq4K+r6NDXcGPe3g5oF9bHsN0u3p10zI80ds
P60mF3HrboBRvmImT78g6bADXpMBQfuBVFo+fZSAppCyiIwqDw4oqfva3FfxpAOb
LCMM24ECgYEAwdOThRvUwmbmKNOfDaFANuuDwgLlJON9uxauG6dileOBVe5NBKQe
YSiZXXVoVnIclkYEw1juThGBVQ0it+wClnsxOhHxPkh/S9DtrQ3HkkJl6Vwd4H9o
7NtbdOtj1lSOvXPmqqbzBQr7SFgnsMC2P3EpURhbs1meutyf9IRucnUCgYEAxrpd
C7grDssQYD3Qy0A+UFn4d0UPgLvhpGzKEIZg8qYPprYGUKmLCGeMl78Y2j6uCzU/
2u1pVk3gB+KpPTQYuEvthzfGSclji9kFOeD9jzBmN5zVfteekq8KQMXx+R7w/wbI
R9v/izlXiyKTmdSNse6D+qVyEs0VgZsf/S0bEiECgYA/lKHdliWSp6J0Xgbct7qS
yWrtJ3n3QdCqoGP4mk3SkVCJ2aPWE+gLQwAcEjlpsgEConFJi1CQt1lPhwGOh5LJ
vhuFywDxx2JKgnyUueJvbex0Qk1iqSjIGaTEk7qqQg6Ywv41mJI7Y0DOmGxcpLqj
0QEWowDhslJJRboKwa5hSQKBgHiMlmLEjkIEBmQLO3v/9YzydtmK6BOUZRVD9PM/
QNIQ0A+1/XCy2Cb6AXwPrPi+6v7bh2e7epmi1dKSuUzqLFCnpmfO+pbJ9nvf4t6w
T7+rgWYc2hl+nK+oRNTz/ou7LD/Xkmic2JBQ8XzyNY0sNeQIpsDF2cPz6ibbvfTr
hq9hAoGAPeYlKFStjh0BCzfhtvUf6+f9PF4/+ro9EUnlNkHifeQ6e/HSGZUl29F1
YYDz7xYsEi1F+YRFpHlMSwwn+NoOa9gSkQ1UC1CS41upbkj0u3KxIBQNjU/i4ntI
x/wG0mBolBH5eZ8KZXilFHYhKqOdTcfrn/WKLF3HQZVoli5hmZY=
-----END RSA PRIVATE KEY-----"""

naween_private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAnADHyQmj0UJ7R4rbWhGfahNEqftZkG1vMDK0d2Z3WBlSoF91
nMzIJ2SqC+k+e17mIYI1b0F9m/3dkUhGBAMgbbTEuzX0oTNOWDXSHJ9fEjOeJQ1r
nuHWcpzOdZQ8dPd24sbAhYeeaYn1oOCj8Q0Homy8uJ2wru8BSqJjrE2NHDKhjBNh
7RsALMubclHzNCS/vjGor60xkqVHDpq4OTXrE7ifiPAg+009AkTarjXSTedxdRgx
TsLnoWAYISZhD5jnG1gH2v1t3Vod7zFti3pRzUgCYksqYZrunq4QKioJpVLEFsxW
Id6mqxj27DJLS6iKpTQciLYMOZqljRS3b6QmuQIDAQABAoIBACuArjW6GfQbUWxw
ZN3XhzhZ2i56mI3FbpmmshuPt90Z5qgxJoeMtY4CrMa4isN1gcA7YrI9NY1f/D7s
xBWPV6YwICJCmA6x03mWvJpduPHG8iVL+kRqntYEMzCnnzpQ3da8bOhvmrW8koID
0sPACe552yCyXJhTru0Enr3oPF7tsa8VAGIJ3vmlHFs+mhM/Db/n1BMOPdmzgYTf
BRnP1S0VexA8UOAJKDogTUyXOryoKiF/2GS1NZHGEvAlBMYveI/s6GIzZHwApQOk
y93oKqeCfz6GQ4zwfX+qyYmqknqngNv1D+hXrz0JdO9F790gRj4OEaABDcBqmduZ
/VF7C9cCgYEAt1hGTRTj1v3eGla7IOwoBJEscTGce9AAQ9iTkC/fbGqOISuA3nfF
3AqBTt3kbvMwkO+NjHHkTC4yd82+zzKUVn8hTFo0YXhfHMuPiGZtyB9yEHPqxxbM
oB86u4MkvphrJzamYcdx7BOrn7BJDom2Zu8nRg1oVcoLllvDPTVbqW8CgYEA2dLF
90fP7+CIITK+olk6o4f+O/EJfYNBEhUCzq7Txh91ukJof97BG7y4cGGEADOZUQXw
CLzhmdw6V6g6xFLcuuwbm+SUiZkNgjBx+WPjOlYU4rmxZqwYvr2HeJcUBwEVFslG
SyBDUEh0jFWfznAm+MsmCQ5OYaWWzUTcf82ejlcCgYB+ID/cbu59y46q19dLQqoU
2jmUdOiNU/2arrZ0jjpIvtSfhOnWINcAFEn4EzU+DhXu3pylbQP8VBtrxyHoL4dU
KYiimbtHAiOMD4zh7HTBIsC5CMUNyGVkEZe5vvHcG8Y656F1ylpYaP+7ju3zDlFo
ZkTCMB8CRUfLW7znsnkoCQKBgB0tsd0lHoKoljO0Q3sl7sf3MKRA7p+ElJPigqTD
IJU6o5+Ww77VTRL1HdPYDEGmp9QFspjJDIN6z8nsPCsOWokjlbM1VHx2JywYZzwc
GFU5MMUKUOxLA2mRo/MQcdtaVsPdpG/t23aGri4aTjTuKxpKxEaURwWnk+LdZZgt
KB8zAoGAC10au00GY8gDwfE/jkOIKTazwWVcnDR4klO5L0Soug62bzJeNbOyTOgK
Y8guc2tJ/Ypm4LbCJbW2Iax8HPTMkzXMnL11UxvfK+4S10Y5GQFceBbQAjbH/Bly
CpjNK8bI1U/5SIte6XlQt7blePAEF7KTm2YqkJT+IM3wZxPwP4U=
-----END RSA PRIVATE KEY-----"""


def regular_node_callback(data):
    json_dic = json.loads(data)
    new_msg = message.Message.from_dict(json_dic)
    if new_msg.action == 'transaction':
        new_msg.data = Transaction.from_dict(new_msg.data)
        new_transaction = new_msg.data
        print('\nTransaction : {}'.format(new_transaction._hash))
        rs = redis_service.RedisService()
        rs.store_object(new_transaction)
    elif new_msg.action == 'block':
        block_service = BlockService()
        new_block = Block.from_dict(new_msg.data)
        block_service.add_block_to_chain(new_block)
        print('\nBlock : {}'.format(new_block._hash))

def run_miner(a_node):
    block_service = BlockService()
    steven_pub = Hashing.get_public_key(steven_private_key)
    #print('Creating new block')
    time_now = int(time.time())
    height = int(BlockService.get_max_height()) + 1
    ten_transactions = TransactionService.get_10_transactions_from_mem_pool()
    block = Block('', '', steven_pub, height, ten_transactions, [], [], time_now)
    block.update_signature(steven_private_key)
    block.update_hash()
    block_service.add_block_to_chain(block)
    # TODO Test if worked block was added. Might fail due to same hash
    for trabs in ten_transactions:
        BaseTransactionService.remove_from_mem_pool(trabs)
    print('\nCreated Block hash: ' + block._hash)
    block_msg = message.Message('block', block)
    sendable_block = block_msg.to_json()
    block_json = json.dumps(sendable_block, sort_keys=True, separators=(',', ':'))
    a_node.connection_manager.send_msg(msg=block_json)
    #print('Broadcasting block')

a_node = None

def wallet_callback(wallet_sock):
    pending = []
    transaction = []
    data = a_node.connection_manager.server.recv_msg(client_socket=wallet_sock)
    json_dic = json.loads(data)
    new_msg = message.Message.from_dict(json_dic)
    if new_msg.action == 'tx_by_public_key':
        user_trans_history, user_balance = TransactionService.get_transactions_by_public_key(new_msg.data, True)
        for trans in user_trans_history:
            if(trans.is_mempool == 1):
                pending.append(trans.get_sendable())
            else:
                transaction.append(trans.get_sendable())
        user_info = {
            "pending" : pending,
            "transaction": transaction,
            "amount": user_balance
        }
        string_json_user_info = json.dumps(user_info, sort_keys=True, separators=(',', ':'))
        a_node.connection_manager.server.send_msg(data=string_json_user_info, client_socket=wallet_sock)
        a_node.connection_manager.server.close_client(client_socket=wallet_sock)
    elif new_msg.action == 'tx':
        print(new_msg.data)
        pass
    else:
        pass

def start_as_regular(bootstrap_host, peer_timeout=0, recv_data_size=2048, \
        socket_timeout=1):
    print('\t\tStarting as a regular node')
    global a_node
    a_node = node.Node()
    a_node.join_network(bootstrap_host, peer_timeout=peer_timeout, recv_data_size=recv_data_size, \
            socket_timeout=socket_timeout, read_callback=regular_node_callback, wallet_callback=wallet_callback, \
            start_bootstrap=True, start_gossiping=True)
    a_node.make_silent(True)
    while True:
        user_input = input('\t\t\tEnter a command: ')
        if user_input == 'quit' or user_input == 'q':
            break
        elif user_input == 'miner' or user_input == 'm':
            run_miner(a_node)
        elif user_input == 'trans' or user_input == 'transaction' or user_input == 't':
            secret = input('\t\t\tFrom : ')
            if secret == 'denys' or secret == 'd':
                private_key = denys_private_key
            elif secret == 'william' or secret == 'will' or secret == 'w':
                private_key = william_private_key
            elif secret == 'matt' or secret == 'm':
                private_key = matt_private_key
            elif secret == 'steven' or secret == 's':
                private_key = steven_private_key
            elif secret == 'naween' or secret == 'n':
                private_key = naween_private_key
            else:
                continue
            public_key = Hashing.get_public_key(private_key)
            to_addr = input('\t\t\tTo addr: ')
            if to_addr == 'denys' or to_addr == 'd':
                to_addr = Hashing.get_public_key(denys_private_key)
            elif to_addr == 'william' or to_addr == 'w' or to_addr == 'will':
                to_addr = Hashing.get_public_key(william_private_key)
            elif to_addr == 'matt' or to_addr == 'm':
                to_addr = Hashing.get_public_key(matt_private_key)
            elif to_addr == 'steven' or to_addr == 's':
                to_addr = Hashing.get_public_key(steven_private_key)
            elif to_addr == 'naween' or to_addr == 'n':
                to_addr = Hashing.get_public_key(naween_private_key)
            else:
                continue
            from_addr = public_key
            amount = input('\t\t\tAmount: ')
            new_transaction = Transaction('', '', to_addr, from_addr, amount, 1)
            new_transaction.update_signature(private_key)
            new_transaction.update_hash()
            transaction_msg = message.Message('transaction', new_transaction)
            transaction_json = transaction_msg.to_json()
            transaction_json = json.dumps(transaction_json, sort_keys=True, separators=(',', ':'))
            a_node.connection_manager.send_msg(msg=transaction_json)
            print('\nTransaction hash : {}'.format(new_transaction._hash))
            rs = redis_service.RedisService()
            rs.store_object(new_transaction)
    a_node.close()

if __name__ == '__main__':
    arguments = sys.argv[1:]
    print('\tCommand line arguments are {}'.format(arguments))
    if arguments:
        print('\tGot arguments')
        port_node = int(arguments[0])
        if len(arguments) == 1:

            host = socket.gethostbyname(socket.getfqdn())
        else:
            host = arguments[1]
        start_as_regular(host, port_node)
    else:
        host = arguments[0]
    start_as_regular(host)
