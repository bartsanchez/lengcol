import re

import requests


def insert_definition(definition, value):
    r = requests.get("http://web/definitions/add/")
    csrftoken = r.cookies['csrftoken']
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
    headers = {'Cookie': "csrftoken={}".format(csrftoken)}
    return requests.post(
        "http://web/definitions/add/",
        data=data,
        headers=headers,
    )


def test_search_is_improved():
    first_definition = b"The secret messages are calling to me endlessly"
    r = insert_definition(
        definition=first_definition,
        value=b"Electrick Light Orchestra",
    )
    assert r.status_code == 200

    second_definition = b"But time keeps flowing like a river to the sea"
    r = insert_definition(
        definition=second_definition,
        value=b"Alan Parsons Project",
    )
    assert r.status_code == 200

    r = requests.get("http://web/terms/search/?v=mesage")
    assert r.status_code == 200
    # One appearing is in last_definitions, so we have to increment by 1
    assert len(re.findall(first_definition, r.content)) == 2
    assert len(re.findall(second_definition, r.content)) == 1

    r = requests.get("http://web/terms/search/?v=frowing+mike")
    assert r.status_code == 200
    assert len(re.findall(first_definition, r.content)) == 1
    assert len(re.findall(second_definition, r.content)) == 2
