import os
import json

# Load the JSON data
with open('git_data_1.json', 'r') as f:
    data = json.load(f)

# Extract conversations
conversations = data.values()

# Iterate through each conversation
for idx, conv in enumerate(conversations):
    # Extract messages and agents
    messages = [item['message'] for item in conv['content']]
    agents = [item['agent'] for item in conv['content']]

    # Splice messages and agents every 4 messages
    spliced_messages = [messages[i:i+4] for i in range(0, len(messages), 4)]
    spliced_agents = [agents[i:i+4] for i in range(0, len(agents), 4)]

    # Create "git_convo" directory
    if not os.path.exists('git_convo'):
        os.makedirs('git_convo')

    # Write spliced messages and agents to separate txt files in "git_convo" directory
    for i, (msg_chunk, agent_chunk) in enumerate(zip(spliced_messages, spliced_agents)):
        filename = f"git_convo/git_convo_{idx+1}_{i+1}.txt"
        with open(filename, 'w') as f:
            for msg, agent in zip(msg_chunk, agent_chunk):
                f.write(f"{agent}: {msg}\n")
        if msg_chunk:
            with open(filename, 'a') as f:
                f.write(f'"{msg_chunk[-1]}"')