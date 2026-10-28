# Project Reflection — Flock Energy API

## 1. What I built

I developed a REST API using FastAPI to expose smart-meter information and energy readings through documented endpoints.

The current implementation includes:
- A root endpoint and health check.
- Meter listing with search, installation-status filtering, and pagination.
- Energy-reading retrieval for known meter IDs.
- Pydantic response models and automatically generated API documentation.
- HTTP 404 handling for unknown meter IDs.
- Automated endpoint tests using pytest and FastAPI's TestClient.

**Important limitation:** The API currently uses explicitly labeled mock data. Live integration with the Urja Meter Ops portal is not complete.

## 2. What assumptions did I make?

I assumed that meter records could be represented using fields such as meter ID, serial number, manufacturer, phase type, installation status, and distribution-transformer code.

I also assumed that the API should provide predictable JSON responses, support filtering and pagination, and return an appropriate HTTP 404 response for an unknown meter ID.

The sample dataset is deliberately small and is not intended to represent the complete portal dataset. I treated the portal as read-only and did not attempt to bypass its authentication protections.

## 3. What was the most difficult part, and how did I get unstuck?

The most difficult part was investigating authentication for the legacy portal. An unauthenticated meter-search request returned HTTP 401. A programmatic form submission to the login endpoint using `httpx` returned HTTP 403 with the message `Cross-site POST form submissions are forbidden`.

I documented the observed behavior and stopped short of bypassing the portal's protection. To continue making progress, I developed the API endpoints against explicitly labeled mock data and added automated tests. Live integration remains unresolved and requires an approved authentication method.

## 4. What mistake did I make?

One design issue was that the initial energy endpoint returned the same sample readings for every recognized meter ID. This could incorrectly associate readings with a meter.

I changed the implementation to maintain energy data by meter ID and return an empty list for a known meter when no sample readings are available. I added a regression test for this behavior.

Another limitation is that the initial implementation focused on API behavior before completing the upstream portal integration. As a result, the API interface works against mock data, but the main live-data requirement is not yet fulfilled.

## 5. What would I improve with another day?

I would prioritize:
1. Obtaining and implementing an approved authentication method for the portal.
2. Connecting the meter-list and energy endpoints to real portal responses.
3. Adding tests for authentication failures, timeouts, upstream HTTP errors, and malformed responses.
4. Reviewing and completing the OpenAPI specification.
5. Improving configuration management, structured logging, and error responses.
6. Expanding tests and verifying the documented behavior against authorized portal responses.

## 6. What would I criticize if reviewing my own submission?

The main criticism is that the current API is not yet backed by live portal data, which is central to the assignment. The mock implementation demonstrates endpoint design, response modeling, filtering, pagination, and basic error handling, but it does not prove that the API can retrieve live portal records.

I would also review whether all documented response fields and error cases match the upstream portal, whether the OpenAPI specification accurately describes the implementation, and whether the tests cover upstream integration failures.

I would consider the submission a useful foundation, but I would not describe the live integration as complete until it had been implemented and tested through an approved authentication flow.