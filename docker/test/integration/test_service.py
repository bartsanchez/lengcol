import requests


def test_app_is_running():
    r = requests.get("http://web")
    assert r.status_code == requests.codes.ok
