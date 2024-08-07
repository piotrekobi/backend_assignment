from fastapi import APIRouter, HTTPException
from .models import AddBatchRequest, StatsResponse
from .data_store import (
    initialize_symbol,
    add_values,
    get_relevant_data,
    data_store,
    stats_store,
)

router = APIRouter()


@router.post("/add_batch/")
async def add_batch(request: AddBatchRequest):
    symbol = request.symbol
    values = request.values

    if symbol not in data_store:
        initialize_symbol(symbol)

    await add_values(symbol, values)
    return {"message": "Batch data added successfully"}


@router.get("/stats/", response_model=StatsResponse)
async def get_stats(symbol: str, k: int):
    if symbol not in data_store:
        raise HTTPException(status_code=400, detail=f"Symbol {symbol} not found")
    if k < 1 or k > 8:
        raise HTTPException(status_code=400, detail="Invalid k value")

    data_points = int(10**k)
    try:
        relevant_data = await get_relevant_data(symbol, data_points)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    min_val = stats_store[symbol]["min_heap"][0]
    max_val = -stats_store[symbol]["max_heap"][0]
    last_val = relevant_data[-1]
    sum_val = stats_store[symbol]["sum"]
    sum_sq_val = stats_store[symbol]["sum_sq"]
    avg_val = sum_val / data_points
    var_val = (sum_sq_val / data_points) - (avg_val**2)

    return StatsResponse(
        symbol=symbol, min=min_val, max=max_val, last=last_val, avg=avg_val, var=var_val
    )
