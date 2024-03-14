#!/root/miniconda2/envs/aagent/bin/python

import os
from groq import Groq
import ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.chroma import Chroma
import re

# Initialize the Groq client with your API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Initialize the OllamaEmbeddings and Chroma vector store
embedding_function = OllamaEmbeddings(model='nomic-embed-text')
vectorstore = Chroma(persist_directory="./hacker", embedding_function=embedding_function)
retriever = vectorstore.as_retriever()

def list_saved_conversations():
    # List all files in the chats directory that end with .txt
    chats_dir = "chats"
    if not os.path.exists(chats_dir):
        os.makedirs(chats_dir)
    return [f for f in os.listdir(chats_dir) if f.endswith('.txt')]

def load_conversation_from_file(file_name):
    # Load a conversation from a file in the chats directory
    chats_dir = "chats"
    file_path = os.path.join(chats_dir, file_name)
    with open(file_path, 'r') as file:
        conversation_history = [line.strip() for line in file.readlines()]
    return conversation_history

def load_conversation(file_path):
    # Initialize an empty list to hold the conversation history
    conversation_history = []

    # Open the file and read its content
    chats_dir = "chats"
    file_path = os.path.join(chats_dir, file_path)
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize variables to hold the current message and its role
    current_message = ""
    current_role = ""

    # Iterate over each line in the file
    for line in lines:
        # Check if the line starts with "user:" or "assistant:"
        if line.startswith("user:") or line.startswith("assistant:"):
            # If there's a current message, append it to the conversation history
            if current_message:
                conversation_history.append({"role": current_role, "content": current_message})

            # Update the current role and message
            current_role = line.split(":")[0] # "user" or "assistant"
            current_message = line.split(":", 1)[1].strip() # The rest of the line
        else:
            # If the line doesn't start with "user:" or "assistant:", it's part of the current message
            current_message += "\n" + line.strip()

    # Append the last message to the conversation history
    if current_message:
        conversation_history.append({"role": current_role, "content": current_message})

    return conversation_history

def save_conversation(conversation_history, file_name):
    # Save the conversation to a file in the chats directory
    chats_dir = "chats"
    if not os.path.exists(chats_dir):
        os.makedirs(chats_dir)
    file_path = os.path.join(chats_dir, f"{file_name}.txt")
    with open(file_path, 'w') as file:
        for message in conversation_history:
            file.write(f"{message['role']}: {message['content']}\n")

# The rest of your chat_with_bot function remains the same
from interpreter import interpreter

def extract_shell_command(response):
    # Regular expression to find text within triple quotes
    pattern = r"```bash(.*?)```"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return response

def handle_groq_response(response):
    # Extract the shell command from the Groq API response
    shell_command = extract_shell_command(response)
    if shell_command:
        # Ask the user for confirmation before executing the command
        confirmation = input(f"Do you want to execute the following command?\n{shell_command}\n(yes/no): ")
        if confirmation.lower() == 'yes':
            # Execute the command with Open Interpreter
            #interpreter.computer.run("bash", "shell_command")
            bash_command_generator = interpreter.computer.run("bash", str(shell_command))
            for output in bash_command_generator:
                if output['type'] == 'console' and output['format'] == 'output':
                    print(output['content'])
        else:
            print("Command execution cancelled.")
    else:
        print("No shell command found in the response.")



def chat_with_bot():
    # Initialize the conversation history
    conversation_history = [{
            "role": "system",
            "content": "Provide only bash shell commands for ubuntu linux without any description. If there is a lack of details, provide most logical solution.Ensure the output is a valid shell command.If multiple steps required try to combine them together using &&.Provide only plain text without Markdown formatting.Do not provide markdown formatting such as ```. remember your last commands and give updates if asked for something similar"
        }]

    # Check if there are any saved conversations
    saved_conversations = list_saved_conversations()
    if saved_conversations:
        print("Saved conversations:")
        for i, conversation in enumerate(saved_conversations):
            print(f"{i+1}. {conversation}")

        # Ask the user if they want to load a saved conversation or start a new one
        load_or_start_new = input("Do you want to load a saved conversation or start a new one? (load/new): ")
        if load_or_start_new.lower() == 'load':
            selected_conversation_index = int(input("Enter the number of the conversation you want to load: ")) - 1
            selected_conversation = saved_conversations[selected_conversation_index]
            conversation_history = load_conversation(selected_conversation)
        elif load_or_start_new.lower() == 'new':
            print("Starting a new conversation.")
        else:
            print("Invalid option. Starting a new conversation.")

    while True:
        input_string = ""
        while True:
            line = input("> ")
            if line == ",,,":
                break
            elif line == "quit":
                input_string += line
                break
            else:
                input_string += line + "\n"
        if input_string.lower() == 'quit':
            break

        context = retriever.invoke(input_string)
        formatted_prompt = f"Question: {input_string}\n\nContext: {context}"

        conversation_history.append({"role": "user", "content": formatted_prompt})

        response = client.chat.completions.create(
            messages=conversation_history,
            model="mixtral-8x7b-32768" # Replace with your model ID
        )

        assistant_response = response.choices[0].message.content

        conversation_history.append({"role": "assistant", "content": assistant_response})

        print(f"Assistant: {assistant_response}")
        handle_groq_response(assistant_response)

    # After the chat ends, ask the user if they want to save the chat
    save_chat = input("Do you want to save this chat? (yes/no): ")
    if save_chat.lower() == 'yes':
        # Ask the user to name the conversation file
        file_name = input("Enter a name for the conversation file: ")
        if file_name:
            if file_name.endswith(".txt"):
                 file_name = file_name.replace(".txt", "")
            save_conversation(conversation_history, file_name)
        elif load_or_start_new:
            if selected_conversation.endswith(".txt"):
                 selected_conversation = selected_conversation.replace(".txt", "")
            save_conversation(conversation_history, selected_conversation)
        else:
            pass

# Run the chatbot
chat_with_bot()
