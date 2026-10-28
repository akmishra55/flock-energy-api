# Portal Integration Protocol Notes

## 1. Purpose

The goal is to expose meter information and energy readings through a documented FastAPI service while keeping the legacy Urja Meter Ops portal read-only.

## 2. Portal endpoints investigated

| Resource | Endpoint | Observation |
|---|---|---|
| Login | `POST /login` | Form fields observed: `email` and `password` |
| Meter search | `GET /portal/meters/search?q=&page=1` | Requires a valid session |
| Energy readings | `GET /portal/meters/{meter_id}/energy` | Response fields observed include `timestamp`, `kwh`, `kvah`, and `voltR` |

The meter search response was observed to include meter records and pagination metadata such as `total`, `page`, and `pageSize`.

## 3. Authentication findings

An unauthenticated request to the meter search endpoint returned HTTP 401, indicating that a valid session is required.

A programmatic form POST to `/login` using `httpx` returned HTTP 403 with the message:

`Cross-site POST form submissions are forbidden`

The portal therefore rejected the attempted programmatic login. No attempt was made to bypass the portal's cross-site request protection.

## 4. Current implementation

The FastAPI service currently uses clearly labeled mock data. It does not claim that the returned meter records or energy readings are live portal data.

The portal client fails safely when programmatic authentication is rejected.

## 5. Limitations

Live integration is incomplete because an approved programmatic authentication flow has not been established.

The current mock dataset contains two meter records and sample energy readings. It is intended to exercise API behavior, response schemas, filtering, pagination, and error handling.

## 6. Next steps

1. Obtain the portal owner's approved API or authentication instructions.
2. Implement the approved read-only authentication flow.
3. Map real portal responses into the API's documented response models.
4. Add tests for authentication failures, portal errors, and malformed responses.
5. Keep credentials outside source control and avoid logging session cookies or tokens.

## 7. Data integrity and security

The integration should remain read-only. It should not modify or delete portal data, bypass authentication protections, or expose credentials and session tokens in logs.
