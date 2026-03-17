import requests
import json

BASE_URL = "http://127.0.0.1:5002"

def test_og_route():
    print("Testing /runOG endpoint...")
    payload = {
        "casename": "CLEWS.Demo",
        "sc_name": "test_verification_run",
        "og_spec": {
            "start_year": 2026,
            "end_year": 2030, # Small range for fast test
            "omega": [0.1] * 5 # Dummy demographics
        }
    }
    try:
        # Note: This might still trigger a long run if not careful with OG-Core specs
        # For verification, we just want to see if the route is found and doesn't 500 immediately
        response = requests.post(f"{BASE_URL}/runOG", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_og_route()
