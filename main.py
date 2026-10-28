
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel


class Meter(BaseModel):
    meterId: str
    serialNo: str
    make: str
    phaseType: str
    installStatus: str
    dtCode: str


class MeterListResponse(BaseModel):
    source: str
    data: list[Meter]
    total: int
    page: int
    pageSize: int


class EnergyReading(BaseModel):
    timestamp: str
    kwh: str
    kvah: str
    voltR: str


class EnergyResponse(BaseModel):
    meter_id: str
    source: str
    data: list[EnergyReading]


app = FastAPI(
    title="Flock Energy API",
    description="API for accessing smart meter information",
    version="0.1.0",
)


@app.get("/")
def home():
    return {"message": "Flock Energy API is running"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Flock Energy API",
    }


# Sample meter records; not fetched from the live portal.
MOCK_METERS = [
    {
        "meterId": "J100001",
        "serialNo": "GE84132",
        "make": "L&T",
        "phaseType": "single",
        "installStatus": "Installed",
        "dtCode": "DT-002",
    },
    {
        "meterId": "J100002",
        "serialNo": "AL28136",
        "make": "L&T",
        "phaseType": "single",
        "installStatus": "Installed",
        "dtCode": "DT-003",
    },
]


@app.get("/meters", response_model=MeterListResponse)
def list_meters(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str | None = None,
    status: str | None = None,
):
    filtered_meters = MOCK_METERS

    # Search by meter ID or serial number.
    if search:
        search_text = search.strip().lower()
        filtered_meters = [
            meter for meter in filtered_meters
            if search_text in meter["meterId"].lower()
            or search_text in meter["serialNo"].lower()
        ]

    # Filter by installation status.
    if status:
        filtered_meters = [
            meter for meter in filtered_meters
            if meter["installStatus"].lower() == status.strip().lower()
        ]

    total = len(filtered_meters)

    # Apply pagination after filtering.
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "source": "mock",
        "data": filtered_meters[start:end],
        "total": total,
        "page": page,
        "pageSize": page_size,
    }






# Sample energy readings. These are mock values, not live portal data.
MOCK_ENERGY_READINGS = {
    "J100001": [
        {
            "timestamp": "23/06/2026 23:30",
            "kwh": "42594.05",
            "kvah": "46001.58",
            "voltR": "231",
        },
        {
            "timestamp": "24/06/2026 00:00",
            "kwh": "42594.47",
            "kvah": "46002.02",
            "voltR": "230",
        },
        {
            "timestamp": "24/06/2026 00:30",
            "kwh": "42594.88",
            "kvah": "46002.47",
            "voltR": "225",
        },
    ],
    "J100002": [],
}


@app.get(
    "/meters/{meter_id}/energy",
    response_model=EnergyResponse,
    responses={
        404: {
            "description": "Meter not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Meter 'J999999' was not found"
                    }
                }
            },
        }
    },
)
def get_meter_energy(meter_id: str):
    known_meter_ids = {
        meter["meterId"] for meter in MOCK_METERS
    }

    if meter_id not in known_meter_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Meter '{meter_id}' was not found",
        )

    return {
        "meter_id": meter_id,
        "source": "mock",
        "data": MOCK_ENERGY_READINGS.get(meter_id, []),
    }

def get_meter_energy(meter_id: str):
    known_meter_ids = {
        meter["meterId"] for meter in MOCK_METERS
    }

    if meter_id not in known_meter_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Meter '{meter_id}' was not found",
        )

    return {
        "meter_id": meter_id,
        "source": "mock",
        "data": [
            {
                "timestamp": "23/06/2026 23:30",
                "kwh": "42594.05",
                "kvah": "46001.58",
                "voltR": "231",
            },
            {
                "timestamp": "24/06/2026 00:00",
                "kwh": "42594.47",
                "kvah": "46002.02",
                "voltR": "230",
            },
            {
                "timestamp": "24/06/2026 00:30",
                "kwh": "42594.88",
                "kvah": "46002.47",
                "voltR": "225",
            },
        ],
    }
