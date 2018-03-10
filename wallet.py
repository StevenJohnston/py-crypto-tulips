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

if __name__ == '__main__':
    p2p = P2pClient(silent = False)
    p2p.connect_to('vagrant', 36363)
    p2p.send_msg('wallet')
    public_key = Hashing.get_public_key(william_private_key)
    transaction_msg = message.Message('tx_by_public_key', public_key)
    transaction_json = transaction_msg.to_json(is_object=False)
    transaction_json = json.dumps(transaction_json, sort_keys=True)
    data = p2p.send_msg(transaction_json)
<<<<<<< HEAD
    print(json.loads(data))
=======
>>>>>>> f9a696c5af1fcf1875f78c2bea7c0546e925b49e
    p2p.close_socket()