import json

# Clean the data and format into JSON
def clean_data_and_format_to_json(input_file, output_file):
    data = []
    with open(input_file, 'r') as f_input:
        for line in f_input:
            parts = line.strip().split('\t')
            cleaned_line = '\t'.join(parts[4:])
            
            # Construct JSON object and append to obj list
            json_obj = {
                "language": "en-us",
                "intent": parts[0],
                "text": parts[1],
                "entities": None
            }
            
            data.append(json_obj)
    
    # Write data to output file
    with open(output_file, 'w') as f_output:
        json.dump(data, f_output, indent=4)

input_file = 'cleaned_data.txt'  
output_file = 'formatted_data.json'  
clean_data_and_format_to_json(input_file, output_file)

