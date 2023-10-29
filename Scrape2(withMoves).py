from bs4 import BeautifulSoup
import requests
import json

# Function to extract move names from a table under a specific span ID
def extract_moves_from_table(soup, span_id):
    move_names = []
    target_span = soup.find('span', {'id': span_id})
    if target_span:
        table = target_span.find_next('table')
        if table:
            for link in table.find_all('a', {'title': lambda x: x and '(move)' in x}):
                move_name = link.text.strip()
                move_names.append(move_name)
    return move_names

# Function to navigate to a "Generation VIII learnset" link and extract moves
def extract_moves_from_gen8_learnset(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Define the span IDs to look for
    span_ids = ['By_leveling_up', 'By_TM', 'By_TM.2FHM.2FTR', 'By_TM.2FHM', 'By_TM.2FTR', 'By_HM.2FTR', 'By_breeding']
    
    # Extract moves from tables under the specified span IDs
    move_list = []
    for span_id in span_ids:
        move_list.extend(extract_moves_from_table(soup, span_id))
    
    return move_list

# Load the existing JSON data
with open('pokemon_data_scrape.json', 'r') as file:
    pokemon_data = json.load(file)

# Iterate through the links
for idx, pokemon in enumerate(pokemon_data, 1):
    link = pokemon['link']
    
    # Send a GET request to the link
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Define the span IDs to look for
    span_ids = ['By_leveling_up', 'By_TM', 'By_TM.2FHM.2FTR', 'By_TM.2FHM', 'By_TM.2FTR', 'By_HM.2FTR', 'By_breeding']
    
    # Extract moves from tables under the specified span IDs
    move_list = []
    for span_id in span_ids:
        move_list.extend(extract_moves_from_table(soup, span_id))
    
    # If the move list is empty, look for a "Generation VIII learnset" link
    if not move_list:
        gen8_learnset_link = soup.find('a', {'title': lambda x: x and 'Generation VIII learnset' in x})
        if gen8_learnset_link:
            gen8_learnset_link = 'https://bulbapedia.bulbagarden.net' + gen8_learnset_link['href']
            move_list = extract_moves_from_gen8_learnset(gen8_learnset_link)
    
    # Add the move list to the existing data
    pokemon['moves'] = move_list
    
    # Print the progress
    print(f'Processed {idx}/{len(pokemon_data)} Pokemon.')

# Save the updated JSON data
output_file = 'pokemon_data_scrape_withmoves.json'
with open(output_file, 'w') as file:
    json.dump(pokemon_data, file, indent=4)

print(f'Pokemon data with moves has been saved to {output_file}')
