import json
import tkinter as tk

def search_pokemon():
    # Clear the existing results in the Text widget
    result_text.delete('1.0', tk.END)

    # Get the entered ability from the 1st index of the ability list box
    selected_ability = ability_listbox.get(0) if ability_listbox.size() > 0 else ""

    # Get the entered moves from the 1st index of the move list boxes
    selected_moves = [move_listbox.get(0) if move_listbox.size() > 0 else "" for move_listbox in move_listboxes]

    # Debugging: Print entered values to check what's being processed
    #print(f"Entered Ability: {selected_ability}")
    #print(f"Entered Moves: {selected_moves}")

    # Check if both ability and moves are empty, and return early if they are
    if not selected_ability and all(not move for move in selected_moves):
        return

    # Initialize a variable to keep track of matching Pokémon
    matching_pokemon = []

    # Iterate through the Pokémon data
    for pokemon_info in pokemon_data:
        abilities = set(ability.lower() for ability in pokemon_info.get('abilities', []))
        moves = set(move.lower() for move in pokemon_info.get('moves', []))

        if (selected_ability == "" or selected_ability in abilities) and all(move in moves for move in selected_moves if move != ""):
            name = pokemon_info['name']
            id = pokemon_info.get('id', '')
            link = pokemon_info.get('link', '')
            #print(f"Name: {name}, ID: {id}, Link: {link}")
            matching_pokemon.append((name, id, link))

    # Display the matching Pokémon in the Text widget with the ID as a hyperlink
    if matching_pokemon:
        for name, id, link in matching_pokemon:
            result_text.insert(tk.END, f'{name} (ID: ')
            result_text.tag_configure(id, foreground="blue", underline=True)
            result_text.insert(tk.END, id, (id,))
            result_text.tag_bind(id, "<Button-1>", lambda event, link=link: open_link(link))
            result_text.insert(tk.END, f')\n')
    else:
        result_text.insert(tk.END, 'No Pokémon found with the specified ability and moves.')

def open_link(link):
    import webbrowser
    webbrowser.open(link)

# Function to update list boxes with autocomplete options
def update_listbox(event, lb, entry, source):
    # Clear the current list of suggestions
    lb.delete(0, tk.END)
    
    # Get the current text in the Entry
    current_text = entry.get().strip().lower()
    
    # Populate the Listbox with matching suggestions from the source if the text box is not empty
    if current_text:
        for item in source:
            if item.startswith(current_text):
                lb.insert(tk.END, item)

# Load the data from the JSON file
with open('merged_pokemon_data_combined2.json', 'r') as file:
    pokemon_data = json.load(file)

# Create a set of abilities and moves for auto-complete
abilities = set()
moves = set()
for pokemon_info in pokemon_data:
    abilities.update(pokemon_info.get('abilities', []))
    moves.update(pokemon_info.get('moves', []))

# Create the main Tkinter window
root = tk.Tk()
root.title("Pokémon Search")

# Create labels and text boxes for ability and moves
ability_label = tk.Label(root, text="Enter Ability:")
ability_label.grid(row=0, column=0, padx=5, pady=5)
ability_entry = tk.Entry(root)
ability_entry.grid(row=0, column=1, padx=5, pady=5)

# Create an ability Listbox for autocomplete
ability_listbox = tk.Listbox(root, height=1)
ability_listbox.grid(row=0, column=2, padx=20, pady=5)
ability_entry.bind('<KeyRelease>', lambda event, lb=ability_listbox, entry=ability_entry, source=abilities: update_listbox(event, lb, entry, source))

# Label and Entry boxes for moves
move_labels = [tk.Label(root, text=f"Enter Move {i + 1}:") for i in range(4)]
move_entries = [tk.Entry(root) for _ in range(4)]
move_listboxes = [tk.Listbox(root, height=1) for _ in range(4)]

for i, (move_label, move_entry, move_listbox) in enumerate(zip(move_labels, move_entries, move_listboxes)):
    move_label.grid(row=i + 1, column=0, padx=5, pady=5)
    move_entry.grid(row=i + 1, column=1, padx=5, pady=5)
    move_listbox.grid(row=i + 1, column=2, padx=5, pady=5)
    move_entry.bind('<KeyRelease>', lambda event, lb=move_listbox, entry=move_entry, source=moves: update_listbox(event, lb, entry, source))

# Create a button to trigger the search
search_button = tk.Button(root, text="Search Pokémon", command=search_pokemon)
search_button.grid(row=5, column=0, padx=5, pady=5, columnspan=3)

# Create a Text widget to display the search results
result_text = tk.Text(root, height=10, width=40)
result_text.grid(row=6, column=0, padx=5, pady=5, columnspan=3)

# Start the Tkinter main loop
root.mainloop()
