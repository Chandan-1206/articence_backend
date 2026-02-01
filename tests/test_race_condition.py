import asyncio
import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_concurrent_packet_ingestion():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        payload1 = {
            "sequence": 1,
            "data": "a",
            "timestamp": 1.0
        }
        payload2 = {
            "sequence": 2,
            "data": "b",
            "timestamp": 1.1
        }

        responses = await asyncio.gather(
            client.post("/v1/call/stream/race_test", json=payload1),
            client.post("/v1/call/stream/race_test", json=payload2),
        )

        assert responses[0].status_code == 202
        assert responses[1].status_code == 202
