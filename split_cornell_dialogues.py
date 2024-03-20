import os

def parse_conversations(movie_lines_file, movie_conversations_file, output_directory):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Read movie lines into a dictionary
    lines_dict = {}
    with open(movie_lines_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parts = line.strip().split(' +++$+++ ')
            lines_dict[parts[0]] = (parts[3], parts[-1])  # Storing speaker name along with the dialog line
    
    # Read movie conversations and write to individual files
    with open(movie_conversations_file, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, start=1):
            parts = line.strip().split(' +++$+++ ')
            conversation = eval(parts[-1])  # Convert string representation of list to actual list
            conversation_text = [f"{lines_dict[utterance_id][0]}: {lines_dict[utterance_id][1]}" for utterance_id in conversation]
            conversation_text[-1] = f'"{conversation_text[-1]}"'  # Wrap last line in quotation marks
            output_file = os.path.join(output_directory, f'dialog_{i}.txt')
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write('\n'.join(conversation_text))

# Paths to input files
movie_lines_file = "cornell movie-dialogs corpus/movie_lines.txt"
movie_conversations_file = "cornell movie-dialogs corpus/movie_conversations.txt"

# Output directory
output_directory = "parsed_cornell_dialogs"

# Parse conversations and write to files
parse_conversations(movie_lines_file, movie_conversations_file, output_directory)
