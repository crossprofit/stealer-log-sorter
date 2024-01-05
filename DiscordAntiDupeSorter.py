import os
import re

# Define the base folder path
base_folder = "base"

# Define the regular expression pattern to match the token
token_pattern = r"Token: (.+)"

# Function to extract and return the tokens from a given text file
def extract_tokens(file_path):
    with open(file_path, "r", encoding="utf8") as file:
        content = file.read()
        tokens = re.findall(token_pattern, content)
    return tokens

# Get the Discord Tokens.txt files recursively from the base folder
text_files = []
for root, dirs, files in os.walk(base_folder):
    for file in files:
        if file == "Discord Tokens.txt" and "Discord" in root:
            text_files.append(os.path.join(root, file))

# Create a global set to store all tokens
all_tokens = set()

# Extract tokens from each text file and add them to the global set
for file_path in text_files:
    tokens = extract_tokens(file_path)
    all_tokens.update(tokens)

# Create an output file in the current folder
output_file = os.path.join(os.getcwd(), "sorted_tokens.txt")

# Write the unique tokens to the output file
with open(output_file, "w") as file:
    for token in all_tokens:
        file.write(token + "\n")
