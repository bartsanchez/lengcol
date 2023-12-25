import requests


def insert_definition(definition, value, tags):
    r = requests.get("http://web/definitions/add/", timeout=5)
    csrftoken = r.cookies["csrftoken"]
    data = {
        "csrfmiddlewaretoken": csrftoken,
        "term": definition,
        "value": value,
        "example_set-TOTAL_FORMS": "1",
        "example_set-INITIAL_FORMS": "0",
        "example_set-MIN_NUM_FORMS": "0",
        "example_set-MAX_NUM_FORMS": "5",
        "example_set-0-value": "",
        "example_set-0-id": "",
        "example_set-0-definition": "",
    }
    if tags:
        data["tags"] = tags
    headers = {"Cookie": f"csrftoken={csrftoken}"}
    return requests.post(
        "http://web/definitions/add/",
        data=data,
        headers=headers,
        timeout=5,
    )
