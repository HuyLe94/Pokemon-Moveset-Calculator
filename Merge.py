import json

# Load data from code1 file
with open('pokemon_data_scrape_withmoves.json', 'r') as file1:
    data_code1 = json.load(file1)

# Load data from code2 file
with open('pokemon_data_api.json', 'r') as file2:
    data_code2 = json.load(file2)

# Create a list to store merged data
merged_data = []

def print_progress(progress, total):
    print(f'Processed {progress}/{total} Pokemon.')

# Merge data from code1 into the list
for item1 in data_code1:
    item = {
        'id': item1['id'],
        'name': item1['name'],
        'abilities': item1.get('abilities', []),
        'moves': item1.get('moves', []),
        'link': item1.get('link', ''),
    }
    merged_data.append(item)
    
# Merge data from code2 into the list
for item2 in data_code2:
    # Find the corresponding entry in the merged list or add a new entry
    matching_item = next((x for x in merged_data if x['id'] == item2['id']))
    if matching_item:
        # Merge abilities data
        matching_item['abilities'] = list(set(matching_item['abilities']) | set(item2.get('abilities', [])))
        matching_item['moves'] = list(set(matching_item['moves']) | set(item2.get('moves', [])))
    else:
        # If not found, add a new entry to the merged list
        item = {
            'id': item2['id'],
            'name': item2['name'],
            'abilities': item2.get('abilities', []),
            'moves': item2.get('moves', []),
            'link': item2.get('link', ''),
        }
        merged_data.append(item)

# Write the merged data to a new JSON file
output_file = 'merged_pokemon_data_combined2.json'
with open(output_file, 'w') as output_file:
    json.dump(merged_data, output_file, indent=4)

print(f'Merged and ordered Pokemon data has been saved to {output_file}')
