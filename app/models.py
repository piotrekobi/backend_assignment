from pydantic import BaseModel
from typing import List


class AddBatchRequest(BaseModel):
    symbol: str
    values: List[float]


class StatsResponse(BaseModel):
    symbol: str
    min: float
    max: float
    last: float
    avg: float
    var: float
