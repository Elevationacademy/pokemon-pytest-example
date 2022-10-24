from pymysql import IntegrityError
import pokemon_api
from models import owner as Owner
from models import pokemon as pokemodel
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse


router = APIRouter()


@router.put('/evolve/{owner}/{pokemon_name}')
def evolve(owner, pokemon_name):
    evolves_to = pokemon_api.get_next_in_evolution_chain(pokemon_name)
    if not evolves_to:
        return JSONResponse({"Error": "pokemon {} can not evolve".format(pokemon_name)},
                            status_code=status.HTTP_400_BAD_REQUEST)

    pokemon_id = pokemodel.get_id(pokemon_name)
    try:
        Owner.evolove_pokemon(pokemon_id, owner, evolves_to)
        return JSONResponse({"success": "pokemon {} evolved into {}".format(pokemon_name, evolves_to)})
    except IntegrityError:
        raise HTTPException(status_code=409,
                            detail=f"pokemon {pokemon_name} aleady exists")

    except Owner.ElementNotExistError:
        message = "trainer {} does not have a {} pokemon".format(
            owner, pokemon_name)
        return JSONResponse({"Error": message},
                            status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse({"DB Error": str(e)},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
