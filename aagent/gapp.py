#!/root/miniconda3/envs/aagent/bin/python3
'''
import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

ques = input("Enter question ")

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": str(ques),
        }
    ],
    model="mixtral-8x7b-32768",
)

print(chat_completion.choices[0].message.content)
'''

import gradio as gr
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

def chatbot_response(user_input):
    global retriever
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'}
    ]

    context = retriever.invoke(user_input)
    formatted_prompt = f"Question: {user_input}\n\nContext: {context}"
    messages.append({'role': 'user', 'content': formatted_prompt})

    response_generator = ollama.chat(model='dolphin-phi', messages=messages, stream=True)
    response = ""
    for part in response_generator:
        if 'message' in part:
            response += part['message']['content']
        else:
            response += "Unexpected response part: " + str(part)

    # Add the assistant's response to the messages
    messages.append({'role': 'assistant', 'content': response})

    return response

# Define the Gradio interface
iface = gr.Interface(
    fn=chatbot_response, # The function to call
    inputs=gr.inputs.Textbox(lines=5, placeholder="Type your message here..."), # Input component
    outputs=gr.outputs.Textbox(), # Output component
    title="Chatbot",
    description="A simple chatbot using Gradio and Ollama."
)

# Launch the Gradio app
iface.launch()

