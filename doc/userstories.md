As a user I want to see all available pokemon
`SELECT * FROM Pokemon;`

As a user I want to see a specific pokemon based on id
`SELECT * FROM Pokemon WHERE id = given_id`

As an administrator I want to be able to add new pokemon
`INSERT INTO pokemon (date_created, date_modified, name, poke_type, description, custom) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, name, poke_type, description, custom)`

As a user I want to be able to search for pokemon
`SELECT * FROM Pokemon WHERE Pokemon.name LIKE name`

# TODO
