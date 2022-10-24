import pytest
import json
from models import owner as ownerModel

@pytest.mark.skip
def test_delete_pokemon():
    ownerModel.delete_pokemon("no such owner", "charmander")

    assert 1 == 1

