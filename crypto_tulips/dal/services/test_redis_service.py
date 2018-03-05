import pytest
import time

from crypto_tulips.dal.services.redis_service import RedisService
from crypto_tulips.dal.objects.transaction import Transaction


def test_get_attributes():
    service = RedisService()
    t = Transaction('hash', '', 'to address', 'from address', 50.123, 0)
    attr_dict = service._get_attributes(t)

    assert attr_dict == t.__dict__


# Store/Get Specific Object Tests

def test_store_get_transaction_by_hash():
    service = RedisService()
    t = Transaction("test_hash", '', "test to", "test from", 50.123, 0)
    success = service.store_object(t)
    assert success

    new_t = service.get_object_by_hash("test_hash", Transaction)

    assert t.to_string() == new_t.to_string()


def test_get_field():
    service = RedisService()
    t = Transaction("test_hash_get", '', "test to_get", "test from_get", 501, 0)

    stored = service.store_object(t)

    assert stored

    result = service.get_field("transaction", "test_hash_get", "to_addr")

    assert result == ["test to_get"]

