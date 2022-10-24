import json
from unittest.mock import Mock
from unittest.mock import patch as mock_patch

from fastapi.testclient import TestClient
from pymysql import IntegrityError

from server import app
from models import owner as Owner


client = TestClient(app)

class TestAddOwner():
    def test_add_owner(self):
        Owner.add = Mock(side_effect = lambda name: None)
        mock_owner = json.dumps({"name": "Mina", "town": "Zedon"})
        response = client.post("/owners", data=mock_owner)
        result = response.json()
        assert response.status_code == 201
        assert result == {"status": "Success. Added Owner"}

    def test_add_existing_owner(self):
        mock_owner = json.dumps({"name": "Limy", "town": "Zedon"})
        Owner.add = Mock(side_effect = [None, IntegrityError])

        client.post("/owners", data=mock_owner)
        response = client.post("/owners", data=mock_owner)
        result = response.json()

        assert response.status_code == 409
        assert "Error" in result

class TestGetPokemons(object):
    @mock_patch('models.owner.get_pokemons')
    def test_chamander_owners(self, get_pokemons):
        mock_trainers = ["Giovanni", "Jasmine"]
        get_pokemons.return_value = mock_trainers

        response = client.get("/owners?pokemon_name=charmander")
        result = response.json()

        assert response.status_code == 200
        for trainer in mock_trainers:
            assert trainer in result

        Owner.get_pokemons.reset_mock()
        print(Owner.get_pokemons)
        print(Owner.get_pokemons.return_value)
