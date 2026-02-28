import requests
try:
    r = requests.get("http://127.0.0.1:4040/api/tunnels")
    print(r.json()["tunnels"][0]["public_url"])
except Exception as e:
    print(f"Could not get URL: {e}")
