from unittest.mock import patch as mock_patch

from pymysql import IntegrityError
from fastapi.testclient import TestClient
from server import app

from models import owner as Owner


client = TestClient(app)


@mock_patch('models.owner.evolove_pokemon')
@mock_patch('pokemon_api.get_next_in_evolution_chain')
def test_evolve(next_in_evolution_chain, evolove_pokemon):
    next_in_evolution_chain.return_value = "charmeleon"
    evolove_pokemon.return_value = None

    response = client.put("/evolve/Whitney/charmander")
    response_message = response.json()
    assert response.status_code == 200
    assert "success" in response_message


@mock_patch('models.owner.evolove_pokemon')
def test_evolve_to_exsiting_pokemon(evolove_pokemon):
    evolove_pokemon.side_effect = IntegrityError

    response = client.put("/evolve/Whitney/charmander")
    response_message = response.json()
    assert response.status_code == 409
    assert "detail" in response_message


@mock_patch('pokemon_api.get_next_in_evolution_chain')
def test_evolve_of_non_evolving_pokemon(next_in_evolution_chain):
    next_in_evolution_chain.return_value = None
    response = client.put("/evolve/Whitney/pinsir")
    response_message = response.json()
    assert response.status_code == 400
    assert "Error" in response_message


@mock_patch('models.owner.evolove_pokemon')
@mock_patch('pokemon_api.get_next_in_evolution_chain')
def test_evolve_with_non_existing_pokemon(next_in_evolution_chain, evolove_pokemon):
    next_in_evolution_chain.return_value = "fearow"
    evolove_pokemon.side_effect = Owner.ElementNotExistError

    response = client.put("/evolve/Archie/spearow")

    response_message = response.json()
    assert response.status_code == 404
    assert "Error" in response_message
