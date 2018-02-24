import requests


def test():
    try:
        return requests.get("http://localhost:8080/geoserver/").status_code
    except Exception:
        return -1

