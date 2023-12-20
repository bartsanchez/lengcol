import requests


def test_robots_txt_view():
    r = requests.get("http://web/robots.txt", timeout=5)
    assert r.status_code == 200
    assert b"User-agent: *\nAllow: /" in r.content
    assert b"Sitemap: https://www.lenguajecoloquial.com/sitemap.xml" in r.content
