from pymysql import IntegrityError
from models import owner as Owner
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse


router = APIRouter()

@router.post('/owners')
async def add_owner(request: Request):
    owner = await request.json()
    try:
        Owner.add(owner)
        return JSONResponse({"status": "Success. Added Owner"},
                            status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        return JSONResponse({"Error": f"owner {owner.get('name')} aleady exists"},
                            status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        return JSONResponse({"DB Error": str(e)},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/owners')
def get_owner(pokemon_name=None):
    try:
        owners = Owner.get_owners(pokemon_name)
        return [item["trainer"] for item in owners]
    except Exception as e:
        return JSONResponse({"Error": e}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
