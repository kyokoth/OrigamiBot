from os import getenv
from dotenv import load_dotenv
from pathlib import Path

import pytest

load_dotenv()



@pytest.fixture
def token():
    t = getenv('TEST_BOT_TOKEN', None)
    if not t:
        pytest.skip('Token required for this test, yet no token found in ENV (TEST_BOT_TOKEN)')
    return t


@pytest.fixture
def private_cid():
    cid = getenv('TEST_PRIVATE_CID', None)
    if not cid:
        pytest.skip('Private chat id required for this test, yet no found in ENV (TEST_PRIVATE_CID)')
    return cid


@pytest.fixture
def image_file():
    path = Path(__file__).parent / '../imgs/logo.png'
    return open(path, 'rb')