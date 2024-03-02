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

