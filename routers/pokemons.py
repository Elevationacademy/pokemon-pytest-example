from pymysql import IntegrityError
import pokemon_api
from models import owner as Owner
from models import pokemon as pokemodel
from fastapi import status, APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/pokemons"
)


# option 1 - parameterized
@router.get('/type/{ptype}')
def get_pokemons_by_type(ptype):
    try:
        pokemons = pokemodel.get_by_type(ptype)
        return pokemons
    except Exception as e:
        return JSONResponse({"Error": e},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/owner/{owner}')
def get_pokemons_by_owner(owner):
    try:
        pokemons = Owner.get_pokemons(owner)
        return pokemons
    except Exception as e:
        return JSONResponse({"Error": e},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# option 2 - query param
@router.get('/')
def get_pokemons(ptype=None, owner=None):
    try:
        pokemons = []
        if ptype:
            pokemons = pokemodel.get_by_type(ptype)
        elif owner:
            pokemons = Owner.get_pokemons(owner)
        return pokemons
    except Exception as e:
        return JSONResponse({"Error": str(e)},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{pokemon}')
def get_pokemon(pokemon):
    pokemon_id = pokemodel.get_id(pokemon)
    if not pokemon_id:
        pokemon = pokemon_api.get_pokemon(pokemon)
        pokemodel.add(pokemon)

    types = pokemon_api.get_pokemon_types(pokemon)
    for p_type in types:
        try:
            pokemodel.add_type(pokemon_id, p_type)
        except IntegrityError:
            continue
        except Exception as e:
            return JSONResponse({"Error": e},
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    pokemon_item = pokemodel.get(pokemon)
    pokemon_item["types"] = types
    return pokemon_item


# I think the payload should be in the body
@router.delete('/{pokemon_name}/{owner}')
def delete(pokemon_name, owner):
    try:
        pokemon_id = pokemodel.get_id(pokemon_name)
        Owner.delete_pokemon(owner, pokemon_id)
        return JSONResponse({"deleted": "true"})
    except Owner.ElementNotExistError as e:
        return JSONResponse({"Error": "Pokemon does not exist"},
                            status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse({"Error": e}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
