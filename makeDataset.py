import os
import numpy as np
import pandas as pd
from PIL import Image

steps = 512

# Load the image
image_path = "SV1-01_20220115_L2A0001315114_60321001423890001_01-FUS_SV.png"
image = Image.open(image_path)

# Get the image dimensions
width, height = image.size

# Calculate the number of tiles in each dimension
num_tiles_x = (width + steps - 1) // steps
num_tiles_y = (height + steps - 1) // steps

# Create an empty DataFrame with the correct dimensions
df = pd.DataFrame(index=range(0, num_tiles_y * steps, steps), columns=range(0, num_tiles_x * steps, steps))

# Create the directory for tiles if it does not exist
tiles_dir = "tiles"
os.makedirs(tiles_dir, exist_ok=True)
x_max = -97.70275
x_min = -97.75669
y_min = 30.27655
y_max = 30.29507

import numpy as np
import pandas as pd
from random import choice, shuffle

# Placeholder for a list of words from a big dictionary
# Ideally, this should be replaced with a real dictionary load
word_list = ["large", "apple", "wonderful", "fly", "mysterious", "car", "fast", "light", "dark", "smooth",
             "Ancient", "mysterious", "enigmatic", "silent", "vast", "distant", "glistening", "forgotten", "hidden", "sacred",
             "luminous", "fleeting", "eternal", "melodic", "thunderous", "whispering", "crimson", "azure", "golden", "silver",
             "mythic", "legendary", "celestial", "cosmic", "terrestrial", "maritime", "solar", "lunar", "stellar", "nebulous",
             "arid", "lush", "barren", "fertile", "pristine", "corrupted", "serene", "chaotic", "ancient", "modern",
             "exotic", "native", "rural", "urban", "natural", "synthetic", "authentic", "fabricated", "transparent", "opaque",]

# Example list of fun facts
quirky_fun_facts = [
    "Cats sleep 70% of their lives.",
    "Octopuses have three hearts.",
    "Bananas are berries, but strawberries aren't.",
    "A group of flamingos is called a flamboyance.",
    "Honey never spoils.",
    "The Eiffel Tower can be 15 cm taller during the summer when the iron heats up and expands.",
    "Venus rotates on its axis so slowly that its day is longer than its year.",
    "You can hear a blue whale's heartbeat from more than 2 miles away.",
    "A day on Venus is longer than a year on Venus.",
    "Banana plants are actually giant herbs, and the banana itself is a berry.",
    "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
    "Cleopatra lived closer in time to the moon landing than to the construction of the Great Pyramid of Giza.",
    "There are more stars in the universe than grains of sand on all of Earth's beaches.",
    "A bolt of lightning contains enough energy to toast 100,000 slices of bread."
]

fun_facts_df = pd.DataFrame(index=range(0, num_tiles_y * steps, steps), columns=range(0, num_tiles_x * steps, steps))
# A set to keep track of unique fun facts
unique_facts = set()

# Function to create a unique scrambled fact
def create_unique_fact():
    while True:
        fact = choice(quirky_fun_facts)  # Choose a random base fact
        words = fact.split()
        potential_replacements = [w for w in word_list if len(w) > 4]  # Choose longer words for replacement
        shuffle(potential_replacements)
        num_replacements = np.random.randint(1, len(words) // 2 + 1)  # Ensure at least one replacement
        replacement_indices = np.random.choice(range(len(words)), num_replacements, replace=False)
        for idx in replacement_indices:
            words[idx] = choice(potential_replacements)
        new_fact = ' '.join(words)
        if new_fact not in unique_facts:
            unique_facts.add(new_fact)
            return new_fact
        

# Split the image into tiles
for y in range(0, height, steps):
    if y>7168: break
    for x in range(0, width, steps):
        # Crop the tile
        tile = image.crop((x, y, x + steps, y + steps))

        if x>8192: break

        # Save the tile with coordinates as the filename
        tile_filename = f"{x}_{y}.png"
        tile_path = os.path.join(tiles_dir, tile_filename)
        tile.save(tile_path)

        # Mark the presence of the tile in the DataFrame
        # Calculate approximate coordinates based off min and max values
        tile_x = x_min + ((x_max - x_min) * (x / width))
        tile_y = y_max - ((y_max - y_min) * (y / height))
        df.at[y, x] = f"({tile_x}, {tile_y})"
        prompt_ext = f"({tile_x}, {tile_y}),"
        prompt_ext += create_unique_fact()
        prompt_filename = f"{x}_{y}.txt"
        prompt_path = os.path.join(tiles_dir, prompt_filename)
        with open(prompt_path, "w") as f:
            f.write(prompt_ext)


# Replace NaNs with empty strings if no tile exists at a position
df.fillna('', inplace=True)


# Save the DataFrame as a CSV file
df.to_csv("coordinates_grid.csv")



# Generate a unique fact for each tile
for y in range(0, height, steps):
    if y > 7168: break
    for x in range(0, width, steps):
        if x > 8192: break
        fun_facts_df.at[y, x] = create_unique_fact()

# Fill NaNs with empty strings if no tile exists at a position
fun_facts_df.fillna('', inplace=True)

# Save the DataFrame as a CSV file
fun_facts_df.to_csv("fun_facts_grid.csv")

