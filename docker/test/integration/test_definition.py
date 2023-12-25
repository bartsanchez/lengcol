import re

import requests

from . import utils


def test_definition_contains_other_definitions():
    definitions = ("first", "second", "third")
    for number in definitions:
        r = utils.insert_definition(
            definition="Water",
            value=f"{number} definition",
            tags=f"definition, {number}",
        )
        assert r.status_code == 200

    r = requests.get("http://web/terms/search/?v=first", timeout=5)

    def_id_regex = b'<a href="/definitions/(.*)/".*\n.*first definition'
    definition_id = str(re.search(def_id_regex, r.content).group(1), encoding="utf-8")

    r = requests.get(f"http://web/definitions/{definition_id}/", timeout=5)
    assert r.status_code == 200

    # one definition is in the HTML meta section
    assert len(re.findall(b"first definition", r.content)) == 2

    assert len(re.findall(b"second definition", r.content)) == 1
    assert len(re.findall(b"third definition", r.content)) == 1

    assert b"Otras definiciones" in r.content


def test_definition_only_one():
    r = utils.insert_definition(
        definition="train",
        value="AVE",
        tags="definition, vehicles",
    )
    assert r.status_code == 200

    r = requests.get("http://web/terms/search/?v=AVE", timeout=5)

    def_id_regex = b'<a href="/definitions/(.*)/".*\n.*AVE'
    definition_id = str(re.search(def_id_regex, r.content).group(1), encoding="utf-8")

    r = requests.get(f"http://web/definitions/{definition_id}/", timeout=5)
    assert r.status_code == 200

    # one definition is in the HTML meta section
    assert len(re.findall(b"AVE", r.content)) == 2

    assert b"Otras definiciones" not in r.content
