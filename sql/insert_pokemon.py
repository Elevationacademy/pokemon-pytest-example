import json
from data import data as pokemons
import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="pokemons",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

for pokemon in pokemons:
    insert_pokemon = "INSERT INTO pokemon values ({},'{}',{},{})".format(
        pokemon["id"],
        pokemon["name"],
        pokemon["height"],
        pokemon.get("weight")
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_pokemon)
            connection.commit()
    except Exception as e:
        print(e)
        print("Error inserting pokemon")

    owners = pokemon["ownedBy"]
    for owner in owners:
        insert_owner = "INSERT INTO trainer values ('{}','{}')".format(
            owner.get("name"),
            owner.get("town")
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(insert_owner)
                connection.commit()
        except Exception as e:
            print(e)
            print("Error inserting trainer")

        insert_pair = "INSERT INTO pokemon_trainer values ('{}',{})".format(
            owner["name"],
            pokemon["id"]
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(insert_pair)
                connection.commit()
        except Exception as e:
            print(e)
            print("Error inserting pair")
