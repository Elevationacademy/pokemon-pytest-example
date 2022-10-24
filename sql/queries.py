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

def get_heviest():
    query = """select name 
            from pokemon
            where weight=(select max(weight) from pokemon);"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result["name"]
    except Exception as e:
        print(e)


def get_pokemon_by_type(type):
    query = "select name from pokemon where type='{}';".format(type)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)


def find_owners(name):
    get_id = "select id from pokemon where name='{}';".format(name)
    get_owners = "select trainer from pokemon_trainer where pokemon_id='{}';"
    try:
        id = None
        with connection.cursor() as cursor:
            cursor.execute(get_id)
            result = cursor.fetchone()
            id = result["id"]
            print(id)
        with connection.cursor() as cursor:
            cursor.execute(get_owners.format(id))
            result = cursor.fetchall()
            return [item["trainer"] for item in result]  
        
    except Exception as e:
        print(e)


    

def find_pokemons(trainer):
    query = """
                select name 
                from pokemon join pokemon_trainer as pt on pokemon.id=pt.pokemon_id
                where trainer="{}";
    """.format(trainer)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return [item["name"] for item in result]
    except Exception as e:
        print(e)


def get_most_owned():
    create_view = """
    create or replace VIEW powners AS
    select pokemon.name, pokemon.id, count(pokemon.id) as owners
    from pokemon join pokemon_trainer as pt on pokemon.id=pt.pokemon_id 
    group by pokemon.id;"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_view)
    except Exception as e:
        print(e)
        return 

    most_owned_query = """
    select name, owners from powners
    where owners=(select max(owners) from powners);
    """   
    try:
        with connection.cursor() as cursor:
            cursor.execute(most_owned_query)
            result = cursor.fetchall()
            return [item["name"] for item in result]
    except Exception as e:
        print(e) 


def main():
    print("heviest", get_heviest())
    print("pokemon_by_type", get_pokemon_by_type("grass"))
    print("owners of gengar", find_owners("gengar"))
    print("pokemons og loga", find_pokemons("Loga"))
    print("most owned", get_most_owned())


if __name__ == "__main__":
    main()