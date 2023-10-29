import json

# Load the data from the JSON file
with open('pokemon_data.json', 'r') as file:
    pokemon_data = json.load(file)

# Define the list of target move names and abilities you want to search for
target_moves = [
    'yawn',
    'surf',
    
]  # Replace with your list of moves

target_abilities = [
    'unaware'
    
]  # Replace with your list of abilities

# Create a list to store Pokémon IDs and names that have all the specified moves and abilities
pokemon_with_moves_and_abilities = []

# Iterate through the Pokémon data
for pokemon_info in pokemon_data:
    moves = set(pokemon_info.get('moves', []))
    abilities = set(pokemon_info.get('abilities', []))
    if set(target_moves).issubset(moves) and set(target_abilities).issubset(abilities):
        pokemon_id = pokemon_info['id']
        pokemon_name = pokemon_info['name']
        pokemon_with_moves_and_abilities.append({'id': pokemon_id, 'name': pokemon_name})

# Print the Pokémon IDs and names that have all the specified moves and abilities
if pokemon_with_moves_and_abilities:
    print(f'Pokémon with all the specified moves and abilities:')
    for pokemon_info in pokemon_with_moves_and_abilities:
        print(f'ID: {pokemon_info["id"]}, Name: {pokemon_info["name"]}')
else:
    print('No Pokémon found with all the specified moves and abilities.')
