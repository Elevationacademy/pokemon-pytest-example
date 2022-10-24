import requests
import random

pokemon_base_url = "https://pokeapi.co/api/v2/"

def get_pokemon(pokemon_id):
    pokemon_res = requests.get(url=pokemon_base_url+"pokemon/{}".format(pokemon_id))
    payload = pokemon_res.json()
    types = [t["type"].get("name") for t in payload.get("types")]
    pokemon_data = {
        'id': pokemon_id,
        'name': payload.get('name'),
        'height': payload.get('height'),
        'weight': payload.get('weight'),
        'type': types,
    }
    return pokemon_data

def get_next_in_evolution_chain(pokemon_name):
    pokemon_res = requests.get(url=pokemon_base_url+"pokemon/{}".format(pokemon_name))
    pokemon_res = pokemon_res.json()
    species_url = pokemon_res.get("species").get("url")
    species_res = requests.get(url=species_url)
    evolution_chain_url = species_res.json().get("evolution_chain").get("url")
    evolution_res = requests.get(url=evolution_chain_url).json().get("chain")
    evolves_to = get_evolves_to_from_chain(evolution_res, pokemon_name)
    return evolves_to
   


def get_evolves_to_from_chain(chain, pokemon_name):
    species = chain.get("species").get("name")
    if species == pokemon_name:
        if chain.get("evolves_to"):
            return chain.get("evolves_to")[0].get("species").get("name")
        else: 
            return None
    else: 
        return get_evolves_to_from_chain(chain.get("evolves_to")[0], pokemon_name)

def get_pokemon_types(pokemon):
    res = requests.get(url=pokemon_base_url+"pokemon/{}".format(pokemon))
    types = [t.get("type").get("name") for t in res.json().get("types")]
    return types


def get_random_pokemon_move(pokemon_name):
    pokemon_data = requests.get(url=pokemon_base_url+"pokemon/{}".format(pokemon_name))
    moves = pokemon_data.json().get("moves")
    random_index = random.randint(0, len(moves))
    move_item = moves[random_index].get("move")
    move_url = move_item.get("url")
    response = requests.get(url=move_url)
    move_data = response.json()
    return {key:move_data.get(key) for key in ["name", "power", "accuracy"]}
