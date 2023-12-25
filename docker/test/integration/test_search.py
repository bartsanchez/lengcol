import re

import requests

from . import utils


def test_search_is_improved():
    first_definition = b"The secret messages are calling to me endlessly"
    r = utils.insert_definition(
        definition=first_definition,
        value=b"Electric Light Orchestra",
        tags="80s, Jeff Lynne, ELO",
    )
    assert r.status_code == 200

    second_definition = b"But time keeps flowing like a river to the sea"
    r = utils.insert_definition(
        definition=second_definition,
        value=b"Alan Parsons Project",
        tags="soft rock 80s",
    )
    assert r.status_code == 200

    r = requests.get("http://web/terms/search/?v=mesage", timeout=5)
    assert r.status_code == 200
    # One appearing is in last_definitions, so we have to increment by 1
    assert len(re.findall(first_definition, r.content)) == 2
    assert len(re.findall(second_definition, r.content)) == 1

    r = requests.get("http://web/terms/search/?v=frowing+mike", timeout=5)
    assert r.status_code == 200
    assert len(re.findall(first_definition, r.content)) == 1
    assert len(re.findall(second_definition, r.content)) == 2


def test_search_includes_definition_value():
    first_definition = b"The secret messages are calling to me endlessly"

    r = requests.get("http://web/terms/search/?v=orkestra", timeout=5)
    assert r.status_code == 200
    # One appearing is in last_definitions, so we have to increment by 1
    assert len(re.findall(first_definition, r.content)) == 2


def test_search_includes_tag_name():
    first_definition = b"The secret messages are calling to me endlessly"

    r = requests.get("http://web/terms/search/?v=Lynne", timeout=5)
    assert r.status_code == 200
    # One appearing is in last_definitions, so we have to increment by 1
    assert len(re.findall(first_definition, r.content)) == 2
