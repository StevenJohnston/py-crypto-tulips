from crypto_tulips.p2p.p2p_client import P2pClient
from crypto_tulips.p2p import message
from crypto_tulips.hashing.crypt_hashing import Hashing
import json

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

temp = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA2xF6fjvpsKtDsoAvbB2ugJLC+zPGT7GWbgWKc9ln4xu+DgUs
WEi/njuPPngsU7zdgScxOWoCgRWA3oGAvY42mid3LxaSck5L6ux6l1HpPPQrIVZL
lp50iHOaVOoZdoqXDIG9fkXxXyL/G03U8iSwJMuu4HnDXPrLbZ7IQhUaibjGSMvn
qWAWUXeYBibvRjYuN/Ne2aABG3lDQg18vHy4DgNVauYfp3f5bpva/mwZ/9hNW6qv
GCK7kFVhN+lHPOLYVoYlwIy39bTtlCXNBrzrHafkArIWWDJS+mIfcj3orm4KUNZv
uT2rNWqncpmynhxcRi+B5rjKgFaFFJqBI6VhRQIDAQABAoIBAQCpcyKh5CwGCOOr
ffWwlmD1eRAzCMBbwo0Oe2C17bOq+zmOVLgRbewyM/XAJ2p6NzvK/AraU0KuoHh3
JAr2FLvtj5tkI/yRSDj29YZ559UW3fNCrSJ41gZjya/WAOJDTD48YVq3AtkKcuKL
NzABQRmyzI5veiAAmsmh+FEEtJg7b/Ak4uwm6YPwyZ7nGBM7qTEX7aOBAghOkBfH
xGQLtigESxO/TwE/xGl2mb2elj879064gwEgLykCCdb2S3wWKJbe6mE1Wxd7VuEq
36YiYaSJNKLEHBftk73RNPAz03G1QGSZx3JHXoq+CwQe/W2OyVSP9KHfaTAVXR1F
eeOkHAg9AoGBAO/HKjZ9Q89/T1ZEb1gkss5PNBQjgB4YbGvuh05B1Nk6JUvizMuj
7aszGySz11yGikhvXjAG2zrxZOBdHRAHr9LNG7pjWJa1CbuGw5oQ16KjXoHccgkf
U0DdNjui1Px1HEdHdK8b6bLqciRRHFpyuh9mylrj0T5ZiPILgBYLkhRfAoGBAOnj
obeWLrcH0iK3O8M1baK3EQ3n9I+oll3Ay5rd7YGfVjEclJsraWnqoDph+SunYNeZ
ovrENvpTNI1bmdcEX1cgj6cH/5cnJ35rc3R0M9YdsaQUGzJOVzLFyZBuQ8CDOH4M
Mcg3O6DYDx7KzbE69WIUY5AAMocIe1Y7Aa2BtozbAoGAGZa1qI8Bt5ksjFZNU6jG
9EF7m1KWj5+nonUYN3/LCUutQ0X2+RyLdqPDl80hhJxPEZ/g+1sf9lBgpZkKSvWn
C+YbuW50u9CiM0MUiNKXUKICqfUurk6LgfaZnQ+pjy+oTusPRsjBzfg7KikFz5lC
x6semUiKwg6oELytdKzTcB0CgYBp4hBjEU1CtPqvlq4qeHSStje1SO4RXyv7c315
NcEA7oZRo3OvL58AQSSaaaIo3hRcZoQ+7DdLagGfgPmLOsKCqg3+ewN9hU8+zxws
ezLAWx8Bfcy2IHsfVCUlCpYHgCBCB/k9f6ux7D4kHYGzG1LdPQe5uC0nrnJPnlTr
HI7tAwKBgQCCe6y2k7zCx+wq4F4C0EKuXz8US6yx3pHZWJZW/O1R1nPYRPdvS6nH
gYoKHneLvvbSrdUpMC7dVy0P0lQ4AzGCpi6BVgpVkKNmZUepOV9Mx7M4DiFOwEQe
f07U4hWOKP5FLbb+V0ZlU/RnuSLQzCKwqeGDiv2f4NnSys2pnIOY2Q==
-----END RSA PRIVATE KEY-----"""


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

if __name__ == '__main__':
    p2p = P2pClient(silent = False)
    p2p.connect_to('vagrant', 36363)
    p2p.send_msg('wallet')
    #Start getting balance, trans history and pending trans
    denys_public_key = Hashing.get_public_key(denys_private_key)
    william_public_key = Hashing.get_public_key(william_private_key)
    transaction_msg = message.Message('tx_by_public_key', william_public_key)
    transaction_json = transaction_msg.to_json(is_object=False)
    transaction_json = json.dumps(transaction_json, sort_keys=True)
    p2p.send_msg(transaction_json)
    data = p2p.recv_msg()

    #ends

    #Testing user wallet key generation

    #public_key = Hashing.get_public_key(temp)
    # print(public_key)
    # sig = Hashing.str_signature_of_data('message', temp)
    # print(sig)

    #ends user wallet testing

    #start a transaction
    amount = 100
    json_trans_to_sign = {
        "from_addr": william_public_key,
        "to_addr": denys_public_key,
        "amount": amount
    }
    trans_json_str = json.dumps(json_trans_to_sign, sort_keys=True)
    sig = Hashing.str_signature_of_data(trans_json_str, temp)

    json_transaction_req = {
        "from_addr": william_public_key,
        "signature": sig,
        "to_addr": denys_private_key,
        "amount": amount
    }
    one_transaction_msg = message.Message('tx', json_transaction_req)
    one_transaction_json = one_transaction_msg.to_json(is_object=False)
    one_transaction_json = json.dumps(one_transaction_json, sort_keys=True)
    p2p.send_msg(one_transaction_json)


    p2p.send_msg("exit")

    p2p.close_socket()

