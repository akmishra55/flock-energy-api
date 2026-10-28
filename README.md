# Flock Energy API

A documented REST API built with FastAPI to expose smart-meter information and energy readings.

**Implementation status:** The current API uses mock data. Live integration with the Urja Meter Ops portal is incomplete because programmatic login was rejected and an approved authentication flow has not yet been established.

## Features

- Health-check endpoint.
- Meter listing with pagination.
- Case-insensitive search by meter ID or serial number.
- Installation-status filtering.
- Energy-reading endpoint for known meters.
- Pydantic response models.
- HTTP 404 responses for unknown meter IDs.
- Interactive Swagger documentation.
- Automated tests using pytest.

## Technology stack

- Python 3.12+
- FastAPI
- Pydantic
- Uvicorn
- HTTPX
- Pytest

## Project structure

```text
NewProject/
├── main.py
├── portal_client.py
├── test_main.py
├── requirements.txt
├── openapi.json
├── PROTOCOL.md
├── reflection.md
└── README.md
```

## Setup

Open a terminal in the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the API

```bash
python -m uvicorn main:app --reload
```

The API runs locally at `http://127.0.0.1:8000`.

- Interactive Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON served by FastAPI: http://127.0.0.1:8000/openapi.json

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Basic service message |
| GET | `/health` | Health check |
| GET | `/meters` | List meters, with optional filtering and pagination |
| GET | `/meters/{meter_id}/energy` | Return sample energy readings for a known meter |

### 1. Health check

Request:

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "Flock Energy API"
}
```

### 2. List meters

Request:

```http
GET /meters?page=1&page_size=20
```

Optional query parameters:

- `page`: Page number; minimum 1; default 1.
- `page_size`: Number of records per page; 1–100; default 20.
- `search`: Case-insensitive partial match against meter ID or serial number.
- `status`: Case-insensitive exact match against installation status.

Example:

```http
GET /meters?search=J100001&status=Installed&page=1&page_size=1
```

Example response:

```json
{
  "source": "mock",
  "data": [
    {
      "meterId": "J100001",
      "serialNo": "GE84132",
      "make": "L&T",
      "phaseType": "single",
      "installStatus": "Installed",
      "dtCode": "DT-002"
    }
  ],
  "total": 1,
  "page": 1,
  "pageSize": 1
}
```

### 3. Get energy readings

Request:

```http
GET /meters/J100001/energy
```

The current mock dataset contains three sample readings for `J100001`. The known meter `J100002` returns an empty list because no sample readings are configured for it.

Unknown meter IDs return HTTP `404 Not Found`.

**Data provenance:** The readings are sample data, not verified live portal readings. Responses use `"source": "mock"` to make this explicit.

## Run tests

```bash
python -m pytest -v
```

The current test suite contains six tests covering:

1. Health check.
2. Meter listing.
3. Meter search.
4. Energy readings for a known meter.
5. Empty sample readings for a second known meter.
6. HTTP 404 for an unknown meter.

The latest recorded run passed all six tests. These tests verify the current mock API behavior; they do not establish that live portal integration works.

## Protocol and API documentation

- [Portal protocol notes](PROTOCOL.md): Observed endpoints, authentication behavior, and integration limitations.
- [OpenAPI specification](openapi.json): API specification file.
- [Development reflection](reflection.md): Assumptions, technical challenges, mistakes, and planned improvements.

FastAPI also generates interactive API documentation at `/docs` when the service is running.

## Assumptions and design decisions

- Meter records are represented using meter ID, serial number, manufacturer, phase type, installation status, and distribution-transformer code.
- The API returns JSON responses and uses HTTP 404 for unknown meter IDs.
- Filtering is performed before pagination.
- Mock data is explicitly identified rather than presented as live portal data.
- Portal access must remain read-only and use an approved authentication method.

## Known limitations and intentionally incomplete work

- Live portal data is not integrated.
- Programmatic login was rejected with HTTP 403.
- The mock dataset contains only two meter records.
- Only `J100001` has configured sample energy readings.
- Upstream timeouts, malformed responses, and other portal failures are not yet covered by integration tests.

## Future improvements

1. Implement the portal client after obtaining an approved authentication method.
2. Connect the API endpoints to actual portal responses.
3. Add tests for authentication failures, upstream errors, timeouts, and malformed data.
4. Validate and maintain the OpenAPI specification against the implementation.
5. Improve configuration, logging, error handling, and test coverage.

## Security and data integrity

The current API uses mock data and does not require portal credentials. Credentials, session cookies, and access tokens must not be committed to source control or exposed in logs.

Any future live integration should use authorized, read-only access and must not bypass portal security protections.