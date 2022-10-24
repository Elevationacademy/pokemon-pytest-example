use pokemons;

drop table IF EXISTS pokemon_type;
drop table IF EXISTS pokemon_trainer;
drop table IF EXISTS trainer;
drop table IF EXISTS pokemon;


CREATE TABLE IF NOT EXISTS pokemon(
    id INT PRIMARY KEY,
    name VARCHAR(20),
    height INT,
    weight INT
); 

CREATE TABLE IF NOT EXISTS pokemon_type(
    pokemon_id INT,
    type VARCHAR(30),
    PRIMARY KEY (type, pokemon_id),
    FOREIGN KEY (pokemon_id)
        REFERENCES pokemon(id)
        ON DELETE CASCADE
); 

CREATE TABLE IF NOT EXISTS trainer(
    name VARCHAR(20) PRIMARY KEY,
    town VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS pokemon_trainer(
    trainer VARCHAR(20),
    pokemon_id INT,
    PRIMARY KEY (trainer, pokemon_id),
    FOREIGN KEY (pokemon_id) 
		REFERENCES pokemon(id) 
  			ON DELETE CASCADE
  			ON UPDATE RESTRICT,
    FOREIGN KEY (trainer) 
		REFERENCES trainer(name) 
  			ON DELETE CASCADE
  			ON UPDATE CASCADE
);

