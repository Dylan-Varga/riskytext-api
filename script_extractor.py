import os
import re

def extract_dialogues(script_path):
    with open(script_path, 'r', encoding='utf-8') as f:  
        script_content = f.read()

    # Remove content within parentheses
    script_content = re.sub(r'\([^()]*\)', '', script_content)

    # Extract dialogues based on capitalized words denoting new lines of dialogue
    dialogues = re.findall(r'([A-Z\s]+):(.+?)(?=[A-Z\s]+:|$)', script_content, re.DOTALL)

    return dialogues

def save_dialogues(dialogues, output_path):
    with open(output_path, 'w', encoding='utf-8') as f: 
        for character, dialogue in dialogues:
            f.write(f"{character.strip()}:\n{dialogue.strip()}\n\n")

scripts_folder = 'movies_source'

# Create output directory
output_folder = 'dialogues_output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through each script
for filename in os.listdir(scripts_folder):
    if filename.endswith('.txt'):
        script_path = os.path.join(scripts_folder, filename)
        dialogues = extract_dialogues(script_path)
        output_path = os.path.join(output_folder, filename.replace('.txt', '_dialogues.txt'))
        save_dialogues(dialogues, output_path)

print("Dialogues extracted and saved successfully!")
