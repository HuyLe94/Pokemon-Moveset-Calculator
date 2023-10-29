import requests
import json

# Determine the total number of Pokémon in the Pokedex (you can get this from the API)
total_pokemon = 1017  # Example, update with the actual total

# Create a list to store data for all Pokémon
all_pokemon_data = []

# Define a function to print the progress
def print_progress(progress, total):
    print(f'Processed {progress}/{total} Pokemon.')

# Iterate through all Pokémon and retrieve data
for pokemon_id in range(1, total_pokemon + 1):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/'
    pokemon_data = requests.get(url).json()
    all_pokemon_data.append(pokemon_data)
    
    # Print the progress
    print_progress(pokemon_id, total_pokemon)

# Ensure the final progress message stays on the console
print()

# Process the data as needed
output_file = 'pokemon_data_api2.json'

# Create a list of dictionaries, each containing data for a Pokémon
pokemon_list = []

for pokemon_data in all_pokemon_data:
    # Extract the ID from the 'id' field in the response
    pokemon_id = pokemon_data['id']
    pokemon_name = pokemon_data['name'].replace('-', ' ')  # Replace hyphens "-" with spaces " "
    
    # Replace hyphens "-" with spaces " " in abilities
    abilities = [ability['ability']['name'].replace('-', ' ') for ability in pokemon_data['abilities']]
    
    # Replace hyphens "-" with spaces " " in move names
    moves = [move['move']['name'].replace('-', ' ') for move in pokemon_data['moves']]
    
    pokemon_info = {
        'id': pokemon_id,
        'name': pokemon_name,
        'abilities': abilities,
        'moves': moves
    }
    pokemon_list.append(pokemon_info)

# Write the list of Pokémon data to a JSON file
with open(output_file, 'w') as file:
    json.dump(pokemon_list, file, indent=4)

print(f'Pokemon data has been saved to {output_file}')
