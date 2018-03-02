from dal.objects.transaction import Transaction
from dal.services.hash_service import HashService
from services.transaction_service.transaction_service import TransactionService

hs = HashService()

t1 = Transaction('testing_hash1', 'matt', 'william', 7000)
t2 = Transaction('testing_hash2', 'steven', 'william', 7000)
t3 = Transaction('testing_hash3', 'shaine', 'william', 605)
t4 = Transaction('testing_hash4', 'william', 'naween', 14605)

hs.store_hash(t1)
hs.store_hash(t2)
hs.store_hash(t3)
hs.store_hash(t4)

ts = TransactionService()

matt_t = ts.get_transactions_by_public_key('matt')

print("\nNumber of transactions that Matt was a part of: " + str(len(matt_t)))
for t in matt_t:
    print(t.to_string() + "\n")

will_t = ts.get_transactions_by_public_key('william')

print("\nNumber of transactions that William was a part of: " + str(len(will_t)))
for t in will_t:
    print(t.to_string() + "\n")
