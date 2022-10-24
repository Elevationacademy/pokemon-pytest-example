import pymysql
from . import pokemon

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="pokemons",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def delete_pokemon(owner, pokemon_id, should_commit=True):
    query = "delete from pokemon_trainer where pokemon_id={} and trainer='{}'".format(
        pokemon_id, owner)

    with connection.cursor() as cursor:
        cursor.execute(query)
        if cursor.rowcount > 0:
            if should_commit:
                connection.commit()
            return True
        else:
            raise ElementNotExistError()


def add_pokemon(owner, pokemon_id):
    query = "insert into pokemon_trainer values ('{}',{})".format(
        owner, pokemon_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except Exception as e:
        print(e)
    

def add(owner_data):
    query = "insert into trainer values ('{}','{}')".format(
        owner_data.get("name"), owner_data.get("town"))

    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()



def get_pokemons(owner):
    query = """
                select name
                from pokemon join pokemon_trainer as pt on pokemon.id=pt.pokemon_id
                where trainer="{}";
    """.format(owner)

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return [item["name"] for item in result]


def evolove_pokemon(pokemon_id, owner, evolves_to):
    delete_query = "delete from pokemon_trainer where pokemon_id={} and trainer='{}'".format(
        pokemon_id, owner)
    add_query = "insert into pokemon_trainer values ('{}',{})".format(
        owner, pokemon.get_id(evolves_to))
    with connection.cursor() as cursor:
        cursor.execute(delete_query)
        if cursor.rowcount < 1:
            raise ElementNotExistError()
    with connection.cursor() as cursor:
        cursor.execute(add_query)
    connection.commit()


def get_owners(pokemon_name):
    pokemon_id = pokemon.get_id(pokemon_name)
    get_owners = "select trainer from pokemon_trainer where pokemon_id='{}';".format(
        pokemon_id)
    with connection.cursor() as cursor:
        cursor.execute(get_owners)
        return cursor.fetchall()


class ElementNotExistError(Exception):
    pass
