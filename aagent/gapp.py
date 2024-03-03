#!/root/miniconda3/envs/aagent/bin/python
'''
import os
from groq import Groq

# Initialize the Groq client with your API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function to handle user input and generate responses
def chat_with_bot():
    # Initialize the conversation history
    conversation_history = []

    while True:
        # Get user input
        user_input = input("You: ")

        # Break the loop if the user types 'quit'
        if user_input.lower() == 'quit':
            break

        # Add user message to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Generate a response using the Groq API
        response = client.chat.completions.create(
            messages=conversation_history,
            model="mixtral-8x7b-32768" # Replace with your model ID
        )

        # Extract the assistant's response
        assistant_response = response.choices[0].message.content

        # Add assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_response})

        # Print the assistant's response
        print(f"Assistant: {assistant_response}")

# Run the chatbot
chat_with_bot()



import os
from groq import Groq
import ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.chroma import Chroma

# Initialize the Groq client with your API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Initialize the OllamaEmbeddings and Chroma vector store
embedding_function = OllamaEmbeddings(model='nomic-embed-text')
vectorstore = Chroma(persist_directory="./pytorch", embedding_function=embedding_function)
retriever = vectorstore.as_retriever()

def chat_with_bot():
    # Initialize the conversation history
    conversation_history = []

    while True:
        # Get user input
        # user_input = input("You: ")

        input_string = ""
        while True:
            line = input("> ")
            if line == "end":
                break
            input_string += line + "\n"

        # Remove the last newline character if the user didn't end with an empty line                                   
        if input_string[-1] == "\n":
            user_input = input_string[:-1]

        # Break the loop if the user types 'quit'
        if user_input.lower() == 'quit':
            break

        # Embed the user input and retrieve context using ChromaDB
        context = retriever.invoke(user_input)
        formatted_prompt = f"Question: {user_input}\n\nContext: {context}"

        # Add user message to the conversation history
        conversation_history.append({"role": "user", "content": formatted_prompt})

        # Generate a response using the Groq API
        response = client.chat.completions.create(
            messages=conversation_history,
            model="mixtral-8x7b-32768" # Replace with your model ID
        )

        # Extract the assistant's response
        assistant_response = response.choices[0].message.content

        # Add assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_response})

        # Print the assistant's response
        print(f"Assistant: {assistant_response}")

# Run the chatbot
chat_with_bot()



import os
from groq import Groq
import ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.chroma import Chroma

# Initialize the Groq client with your API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Initialize the OllamaEmbeddings and Chroma vector store
embedding_function = OllamaEmbeddings(model='nomic-embed-text')
vectorstore = Chroma(persist_directory="./pytorch", embedding_function=embedding_function)
retriever = vectorstore.as_retriever()
'''



import os
from groq import Groq
import ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.chroma import Chroma

# Initialize the Groq client with your API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Initialize the OllamaEmbeddings and Chroma vector store
embedding_function = OllamaEmbeddings(model='nomic-embed-text')
vectorstore = Chroma(persist_directory="./pytorch", embedding_function=embedding_function)
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



def chat_with_bot():
    # Initialize the conversation history
    conversation_history = []

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

    # After the chat ends, ask the user if they want to save the chat
    save_chat = input("Do you want to save this chat? (yes/no): ")
    if save_chat.lower() == 'yes':
        # Ask the user to name the conversation file
        file_name = input("Enter a name for the conversation file: ")
        save_conversation(conversation_history, file_name)

# Run the chatbot
chat_with_bot()

