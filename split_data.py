import os

def split_lines_into_files(input_file, output_directory):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    with open(input_file, 'r') as f_input:
        line_number = 1
        for line in f_input:
            # Define the filename for the current line
            output_file = os.path.join(output_directory, f"training_{line_number}.txt")
            # Write the current line to the output file
            with open(output_file, 'w') as f_output:
                f_output.write(line)
            # Increment line number for the next file
            line_number += 1

input_file = 'cleaned_data.txt'  
output_directory = 'split_data' 
split_lines_into_files(input_file, output_directory)