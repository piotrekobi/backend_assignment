import pytest
from fastapi.testclient import TestClient
from app.main import server
from app.models import AddBatchRequest, StatsResponse
from app.data_store import initialize_symbol

client = TestClient(server)


@pytest.mark.asyncio
async def test_add_batch():
    initialize_symbol("AAPL")
    request_data = AddBatchRequest(symbol="AAPL", values=[150.0, 151.0, 152.0]).dict()
    response = client.post("/add_batch/", json=request_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Batch data added successfully"}


@pytest.mark.asyncio
async def test_get_stats():
    initialize_symbol("AAPL")
    request_data = AddBatchRequest(
        symbol="AAPL",
        values=[150.0, 151.0, 152.0, 153.0, 154.0, 155.0, 156.0, 157.0, 158.0, 159.0],
    ).dict()
    response = client.post("/add_batch/", json=request_data)
    assert response.status_code == 200, f"Add batch failed: {response.json()}"

    response = client.get("/stats/", params={"symbol": "AAPL", "k": 1})
    assert response.status_code == 200, f"Get stats failed: {response.json()}"

    stats_response = StatsResponse(
        symbol="AAPL", min=150.0, max=159.0, last=159.0, avg=154.5, var=8.25
    )

    response_data = response.json()
    assert response_data["symbol"] == stats_response.symbol
    assert response_data["min"] == stats_response.min
    assert response_data["max"] == stats_response.max
    assert response_data["last"] == stats_response.last
    assert response_data["avg"] == pytest.approx(stats_response.avg, rel=1e-2)
    assert response_data["var"] == pytest.approx(stats_response.var, rel=1e-2)


@pytest.mark.asyncio
async def test_get_stats_insufficient_data():
    initialize_symbol("GOOGL")
    request_data = AddBatchRequest(symbol="GOOGL", values=[1200.0]).dict()
    response = client.post("/add_batch/", json=request_data)
    assert response.status_code == 200, f"Add batch failed: {response.json()}"

    response = client.get("/stats/", params={"symbol": "GOOGL", "k": 1})
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough data points"


@pytest.mark.asyncio
async def test_get_stats_invalid_k():
    initialize_symbol("AAPL")
    response = client.get("/stats/", params={"symbol": "AAPL", "k": 9})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid k value"


@pytest.mark.asyncio
async def test_add_batch_empty_values():
    initialize_symbol("MSFT")
    request_data = AddBatchRequest(symbol="MSFT", values=[]).dict()
    response = client.post("/add_batch/", json=request_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Batch data added successfully"}


@pytest.mark.asyncio
async def test_get_stats_no_data():
    initialize_symbol("TSLA")
    response = client.get("/stats/", params={"symbol": "TSLA", "k": 1})
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough data points"


@pytest.mark.asyncio
async def test_get_stats_nonexistent_symbol():
    response = client.get("/stats/", params={"symbol": "NONEXISTENT", "k": 1})
    assert response.status_code == 400
    assert response.json()["detail"] == "Symbol NONEXISTENT not found"


@pytest.mark.asyncio
async def test_add_batch_and_get_stats_large_k():
    initialize_symbol("NFLX")
    request_data = AddBatchRequest(symbol="NFLX", values=list(range(1, 101))).dict()
    response = client.post("/add_batch/", json=request_data)
    assert response.status_code == 200

    response = client.get("/stats/", params={"symbol": "NFLX", "k": 2})
    assert response.status_code == 200
    stats_response = StatsResponse(
        symbol="NFLX", min=1.0, max=100.0, last=100.0, avg=50.5, var=833.25
    )

    response_data = response.json()
    assert response_data["symbol"] == stats_response.symbol
    assert response_data["min"] == stats_response.min
    assert response_data["max"] == stats_response.max
    assert response_data["last"] == stats_response.last
    assert response_data["avg"] == pytest.approx(stats_response.avg, rel=1e-2)
    assert response_data["var"] == pytest.approx(stats_response.var, rel=1e-2)
