from collections import deque
from heapq import heappush, heapify
from typing import Dict, List
import asyncio

MAX_DEQUE_SIZE = 10**8

data_store: Dict[str, deque] = {}
last_data_points: Dict[str, deque] = {}
stats_store: Dict[str, Dict[str, float]] = {}
data_locks: Dict[str, asyncio.Lock] = {}


def initialize_symbol(symbol: str):
    data_store[symbol] = deque()
    last_data_points[symbol] = deque(maxlen=MAX_DEQUE_SIZE)
    stats_store[symbol] = {
        "min_heap": [],
        "max_heap": [],
        "sum": 0.0,
        "sum_sq": 0.0,
        "count": 0,
    }
    data_locks[symbol] = asyncio.Lock()


async def add_values(symbol: str, values: List[float]):
    async with data_locks[symbol]:
        for value in values:
            data_store[symbol].append(value)
            last_data_points[symbol].append(value)
            heappush(stats_store[symbol]["min_heap"], value)
            heappush(stats_store[symbol]["max_heap"], -value)
            stats_store[symbol]["sum"] += value
            stats_store[symbol]["sum_sq"] += value * value
            stats_store[symbol]["count"] += 1

            if len(data_store[symbol]) > MAX_DEQUE_SIZE:
                old_value = data_store[symbol].popleft()
                stats_store[symbol]["sum"] -= old_value
                stats_store[symbol]["sum_sq"] -= old_value * old_value
                stats_store[symbol]["count"] -= 1
                stats_store[symbol]["min_heap"].remove(old_value)
                heapify(stats_store[symbol]["min_heap"])
                stats_store[symbol]["max_heap"].remove(-old_value)
                heapify(stats_store[symbol]["max_heap"])


async def get_relevant_data(symbol: str, data_points: int):
    async with data_locks[symbol]:
        if len(last_data_points[symbol]) < data_points:
            raise ValueError("Not enough data points")
        relevant_data = list(last_data_points[symbol])[-data_points:]
        return relevant_data
