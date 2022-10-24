from fastapi import FastAPI
import uvicorn
from routers import pokemons as pokemons_API
from routers import owners as owners_API
from routers import operations as operations_API


app = FastAPI()

app.include_router(pokemons_API.router)
app.include_router(owners_API.router)
app.include_router(operations_API.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
