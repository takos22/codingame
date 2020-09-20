# TODO add more tests
import pytest
import os
import sys
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.abspath("..."))

def test_import():
    import codingame
    assert codingame.__title__ == codingame.__name__ == codingame.__package__ == "codingame"
    assert codingame.__author__ == "takos22"

def test_client():
    import codingame
    client = codingame.Client()

    assert hasattr(client, "get_codingamer")
    assert hasattr(client, "get_clash_of_code")

    codingamer = client.get_codingamer(os.environ.get("CODINGAMER_PUBLIC_HANDLE"))

    assert type(codingamer) == codingame.CodinGamer

    codingamer = client.get_clash_of_code(os.environ.get("CLASHOFCODE_PUBLIC_HANDLE"))

    assert type(codingamer) == codingame.ClashOfCode
