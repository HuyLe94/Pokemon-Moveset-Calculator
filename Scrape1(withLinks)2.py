from bs4 import BeautifulSoup
import requests
import json
import re

# Send a GET request to the main page URL
main_page_url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number'
response = requests.get(main_page_url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all tables with the class 'roundy'
tables = soup.find_all('table', class_='roundy')

# Initialize a list to store ID, name, and link data
pokemon_data = []

# Create a regular expression pattern for a case-insensitive " form"
pattern = re.compile(r' form', re.IGNORECASE)

# Iterate through the tables
for table in tables:
    # Find all <tr> elements in the <tbody> of the table
    rows = table.find('tbody').find_all('tr')

    # Start from the 2nd <tr> (skip the header row)
    for row in rows[1:]:
        # Extract data based on the positions of <td> elements
        columns = row.find_all('td')
        if len(columns) > 2:
            id_cell = columns[0]  # The ID is in the first column
            link_cell = columns[2]  # The link is in the third column
            id_text = id_cell.text.lstrip('#').strip()
            if id_text:
                id = int(id_text)
                link = 'https://bulbapedia.bulbagarden.net' + link_cell.find('a')['href']
                name = link_cell.text.strip()

                # Remove the " form" substring in a case-insensitive manner
                name = re.sub(pattern, '', name)

                pokemon_data.append({
                    "id": id,
                    "name": name,
                    "link": link
                })

# Save the collected data to a JSON file
output_file = 'pokemon_data_scrape.json'

with open(output_file, 'w') as file:
    json.dump(pokemon_data, file, indent=4)

print(f'Pokemon data has been saved to {output_file}')
