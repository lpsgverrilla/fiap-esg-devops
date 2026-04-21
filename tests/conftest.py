import pytest
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from src.db import mongo
from src.main import app


@pytest.fixture
def mock_mongo():
    """Swap the Motor client for mongomock-motor so tests run without a real MongoDB."""
    client = AsyncMongoMockClient()
    mongo.set_client(client)
    yield client
    mongo.set_client(None)


@pytest.fixture
async def client(mock_mongo):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c
