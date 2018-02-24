import pytest
import time

from dal.services import hash_service
from dal.objects import transaction


def test_get_attributes():
    service = hash_service.HashService()
    t = transaction.Transaction('hash', 'to address', 'from address', '50.123')
    attr_dict = service._get_attributes(t)

    # remove prefix as it is remove in the method
    attr_dict.pop('prefix')
    assert attr_dict == t.__dict__


# Store/Get Specific Object Tests

def test_store_get_transaction_by_hash():
    service = hash_service.HashService()
    t = transaction.Transaction("test_hash", "test to", "test from", 50.123)
    success = service.store_hash(t)
    assert success

    result = service.get_object_by_hash("test_hash", transaction.Transaction)
    new_t = transaction.Transaction.from_dict(result)
    assert t == new_t


def test_get_field():
    service = hash_service.HashService()
    t = transaction.Transaction("test_hash_get", "test to_get", "test from_get", 501)

    stored = service.store_hash(t)

    assert stored

    result = service.get_field("transaction", "test_hash_get", "to_addr")

    assert result == ["test to_get"]

