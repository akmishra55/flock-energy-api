
import os
import httpx

BASE_URL = "https://urja-ops.flockenergy.tech"


def create_portal_client():
    username = os.environ.get("FLOCK_USERNAME")
    password = os.environ.get("FLOCK_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "Set FLOCK_USERNAME and FLOCK_PASSWORD first."
        )

    client = httpx.Client(
        base_url=BASE_URL,
        follow_redirects=True,
        timeout=20.0,
    )

    try:
        response = client.post(
            "/login",
            data={
                "email": username,
                "password": password,
            },
        )

        print("Login HTTP status:", response.status_code)

        if response.status_code == 403:
            raise RuntimeError(
                "Portal rejected programmatic login. "
                "An approved authentication flow is required."
            )

        if response.status_code >= 400:
            raise RuntimeError(
                f"Portal login failed with HTTP "
                f"{response.status_code}."
            )

        # Verify access with a read-only meter-list request.
        meter_response = client.get(
            "/portal/meters/search",
            params={"q": "", "page": 1},
        )

        print("Meter endpoint status:", meter_response.status_code)

        if meter_response.status_code == 401:
            raise RuntimeError(
                "No valid session was established. "
                "Check the portal's approved login flow."
            )

        meter_response.raise_for_status()
        data = meter_response.json()

        print("Total meters:", data.get("total"))
        print(
            "Meters returned:",
            len(data.get("data", [])),
        )

        return client

    except Exception:
        client.close()
        raise


if __name__ == "__main__":
    client = create_portal_client()
    client.close()
