# Portal Integration Protocol Notes

## 1. Purpose

The goal is to expose meter information and energy readings through a documented FastAPI service while keeping the legacy Urja Meter Ops portal read-only.

This document records the portal endpoints investigated, observed authentication behavior, current integration status, and the next steps required for live integration.

## 2. Portal Endpoints Investigated

| Resource | Endpoint | Observation |
|---|---|---|
| Login | `POST /login` | Form fields observed: `email` and `password` |
| Meter search | `GET /portal/meters/search?q=&page=1` | Requires a valid session |
| Energy readings | `GET /portal/meters/{meter_id}/energy` | Observed response fields include `timestamp`, `kwh`, `kvah`, and `voltR` |

The meter search response was observed to include meter records and pagination metadata such as `total`, `page`, and `pageSize`.

These findings reflect the endpoints and responses investigated during this assignment; they do not establish that every portal behavior has been exhaustively verified.

## 3. Authentication Findings

An unauthenticated request to the meter search endpoint returned HTTP `401`, indicating that a valid session is required.

A programmatic form submission to `/login` using `httpx` returned HTTP `403` with the message:

`Cross-site POST form submissions are forbidden`

The attempted programmatic login was therefore rejected. No attempt was made to bypass the portal's cross-site request protection.

An approved programmatic authentication flow has not yet been established.

## 4. Current Implementation

The FastAPI service currently uses clearly labeled mock data. It does not represent its returned meter records or energy readings as live portal data.

The portal client detects the rejected programmatic login and raises an error rather than attempting to bypass the portal's protection.

The current API supports meter listing, search and filtering, pagination, energy-reading retrieval, and appropriate handling of unknown meter IDs using the mock dataset.

## 5. Limitations

Live portal integration remains incomplete because an approved programmatic authentication flow has not been established.

The mock dataset contains two meter records and sample energy readings. It is intended to exercise API behavior, response schemas, filtering, pagination, and error handling; it is not a complete representation of the portal's dataset.

## 6. Next Steps

1. Obtain the portal owner's approved API or authentication instructions.
2. Implement the approved read-only authentication flow.
3. Map actual portal responses into the API's documented response models.
4. Add tests for authentication failures, portal errors, timeouts, and malformed responses.
5. Keep credentials outside source control and avoid logging session cookies or tokens.
6. Update `openapi.json` and the README if the API contract changes.

## 7. Data Integrity and Security

The integration must remain read-only. It must not modify or delete portal data, bypass authentication protections, or expose credentials and session tokens in logs.

Credentials should be supplied through environment variables or another approved secrets-management mechanism and must not be committed to source control.

## 8. Related Documentation

- `README.md` — setup instructions, API usage, implementation status, assumptions, and limitations.
- `openapi.json` — machine-readable API contract for the FastAPI service.
- `reflection.md` — reflection on assumptions, challenges, mistakes, limitations, and possible improvements.
