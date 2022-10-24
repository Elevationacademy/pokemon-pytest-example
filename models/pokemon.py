import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="pokemons",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def get_id(pokemon_name):
    query = "select id from pokemon where name='{}'".format(pokemon_name)
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone().get("id")

def get(pokemon_name):
    query = "select * from pokemon where name='{}'".format(pokemon_name)
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()



def add(pokemon):
    insert_query = """INSERT INTO pokemon values ({},'{}',{},{})""".format(
        pokemon["id"],
        pokemon["name"],
        pokemon["height"],
        pokemon["weight"]
    )
    with connection.cursor() as cursor:
        cursor.execute(insert_query)
        connection.commit()
    for ptype in pokemon.get("type"):
        add_type(pokemon["id"], ptype)


def get_by_type(pokemon_type):
    query = """select name
    from pokemon join pokemon_type as pt on pokemon.id=pt.pokemon_id
    where type='{}';""".format(pokemon_type)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return [item["name"] for item in result]


def add_type(pokemon_id, ptype):
    insert_query = "INSERT INTO pokemon_type values ({},'{}')".format(
        pokemon_id, ptype)
    with connection.cursor() as cursor:
        cursor.execute(insert_query)
        connection.commit()




