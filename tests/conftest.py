import pytest

from starlette import testclient

from app import app


@pytest.fixture(scope='module')
def TestClient():
    return testclient.TestClient(app)