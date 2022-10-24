from fastapi.testclient import TestClient
from server import app


client = TestClient(app)


def test_pokemon_type():
    response = client.get("/pokemons/type/bug")
    bug_pokemons = response.json()
    assert response.status_code == 200
    assert "pinsir" in bug_pokemons


def test_get_pokemon_by_owner():
    expected_pokemons = ["wartortle", "caterpie", "beedrill", "arbok",
                         "clefairy", "wigglytuff", "persian",
                         "growlithe", "machamp", "golem", "dodrio",
                         "hypno", "cubone", "eevee", "kabutops"]
    response = client.get("/pokemons/owner/Drasna")
    owner_pokemons = response.json()
    assert response.status_code == 200
    assert owner_pokemons == expected_pokemons

