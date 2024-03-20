import os
import re

def split_dialogue(text):
    # Remove anything inside parentheses and surrounding spaces
    text = re.sub(r'\s*\([^)]*\)\s*', ' ', text)
    # Replace multiple consecutive spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

def split_into_files(sentences, movie_name):
    if not os.path.exists("cleaned_scripts"):
        os.makedirs("cleaned_scripts")
    count = 1
    for i in range(0, len(sentences), 10):
        filename = f"cleaned_scripts/{movie_name}_{count}.txt"
        with open(filename, "w", encoding='utf-8') as file:
            file.write("\n\n".join(sentences[i:i+10]))
        count += 1

def clean_script(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    movie_name = os.path.splitext(os.path.basename(file_path))[0]
    sentences = split_dialogue(text)
    split_into_files(sentences, movie_name)

if __name__ == "__main__":
    # Iterate through directory
    for filename in os.listdir("movies_source"):
        if filename.endswith(".txt"):
            file_path = os.path.join("movies_source", filename)
            clean_script(file_path)