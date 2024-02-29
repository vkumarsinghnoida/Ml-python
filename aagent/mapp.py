#!/root/miniconda3/envs/aagent/bin/python3

import ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community import embeddings
from langchain_community.vectorstores.chroma import Chroma

embedding_function = embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text')

# Load the database from the specified directory with the embedding function
vectorstore = Chroma(
    persist_directory="./pytorch",
    embedding_function=embedding_function
)

retriever = vectorstore.as_retriever()

def start_chat():
    # Initialize the chat history with a system message
    global retriever
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'}
    ]

    # Start the chat loop
    while True:
        # Read user input
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        # Add the user input to the messages
        context = retriever.invoke(user_input)
        formatted_prompt = f"Question: {user_input}\n\nContext: {context}"
        messages.append({'role': 'user', 'content': formatted_prompt})

        # Send the user input to the Ollama API with streaming enabled
        response_generator = ollama.chat(model='dolphin-phi', messages=messages, stream=True)

        # Print each part of the response in real-time with a slight delay
        for part in response_generator:
            if 'message' in part:
                print(part['message']['content'], end='', flush=True)
            else:
                print("Unexpected response part:", part)

        print(" ")
        # Add the assistant's response to the messages
        # Note: Since we're streaming, we might not have the full response yet.
        # You might need to handle this differently depending on your application's needs.
        messages.append({'role': 'assistant', 'content': "Assistant's response"})

# Start the chatbot
start_chat()
