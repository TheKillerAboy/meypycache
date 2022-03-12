import pytest
from pytest import fixture, lazy_fixture
import json
from meypycache.core import uuid

@fixture
def json_seed():
    metadata = {
        "args": [
            'a',
            'HELLO',
            0,
            100
        ],
        "kwargs": {
            "ABC": "DEF",
            33: "KK"
        }
    }
    return json.dumps(metadata)


@pytest.mark.parametrize(
    "seed,final_uuid", 
    [
        (0,"e3e70682-c209-4cac-629f-6fbed82c07cd"),
        (100,"f3a3c571-7476-1899-75a3-adb3254a9493"),
        ("HELLO","674254a7-d4e0-090b-87e0-45c2f62816e6"),
        (lazy_fixture('json_seed'),"dfa2032d-0e7c-dd42-9132-4b085c80fc50")
    ]
)
def test_uuid_from_seed(seed, final_uuid):
    assert str(uuid.uuid_from_seed(seed)) == final_uuid
