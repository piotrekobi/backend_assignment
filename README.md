# High-Performance Trading Data Service

This project implements a high-performance RESTful service capable of handling the rigorous demands of high-frequency trading systems. The service provides API endpoints for adding batch trading data and retrieving statistical analyses of recent trading data.

## Features

- POST /add_batch/: Allows the bulk addition of consecutive trading data points for a specific symbol.
- GET /stats/: Provides rapid statistical analyses of recent trading data for specified symbols.

## Requirements

- Python 3.9+
- pip (Python package installer)

## Setup

1. Clone the repository:

   `git clone https://github.com/piotrekobi/backend_assignment.git`

   `cd backend_assignment`

2. Create a virtual environment:

   `python3 -m venv venv`

   `source venv/bin/activate`  (On Windows use `venv\Scripts\activate`)

3. Install dependencies:

   `pip install -r requirements.txt`

## Running the Service

1. Start the FastAPI server:

   `python -m app.main`

   The server will be running at <http://0.0.0.0:8000>.

## API Endpoints

### POST /add_batch/

Purpose: Allows the bulk addition of consecutive trading data points for a specific symbol.

Input:

- symbol: String identifier for the financial instrument.
- values: Array of floating-point numbers representing sequential trading prices.

Response:

- Confirmation of the batch data addition.

Example Request:

```sh
curl -X POST "http://0.0.0.0:8000/add_batch/" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{"symbol": "AAPL", "values": [150.0, 151.0, 152.0]}'
```

### GET /stats/

Purpose: Provides rapid statistical analyses of recent trading data for specified symbols.

Input:

- symbol: The financial instrument's identifier.
- k: An integer from 1 to 8, specifying the number of last 1e{k} data points to analyze.

Response:

- min: Minimum price in the last 1e{k} points.
- max: Maximum price in the last 1e{k} points.
- last: Most recent trading price.
- avg: Average price over the last 1e{k} points.
- var: Variance of prices over the last 1e{k} points.

Example Request:

```sh
curl -X GET "http://0.0.0.0:8000/stats/?symbol=AAPL&k=1" \
-H "accept: application/json"

```

## Running Tests

1. Install testing dependencies:

   `pip install -r requirements.txt`

2. Run the tests:

   `PYTHONPATH=$(pwd) pytest tests/test_app.py` (On Windows use `set PYTHONPATH=%cd% && pytest tests\test_app.py`)
