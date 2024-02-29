import gradio as gr
import ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community import embeddings
from langchain_community.vectorstores.chroma import Chroma

# Initialize the embedding function and vector store
embedding_function = embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text')
vectorstore = Chroma(persist_directory="./pytorch", embedding_function=embedding_function)
retriever = vectorstore.as_retriever()

def generate(input, chat_history, top_k, top_p, temp):
    global retriever
    messages = chat_history or [{'role': 'system', 'content': 'You are a helpful assistant.'}]

    # Retrieve context using the retriever
    context = retriever.invoke(input)
    formatted_prompt = f"Question: {input}\n\nContext: {context}"
    messages.append({'role': 'user', 'content': formatted_prompt})

    # Generate response using the Ollama API
    response_generator = ollama.chat(model='dolphin-phi', messages=messages, stream=True)
    response = ""
    for part in response_generator:
        if 'message' in part:
            response += part['message']['content']
        else:
            response += "Unexpected response part: " + str(part)

    # Add the assistant's response to the messages
    messages.append({'role': 'assistant', 'content': response})

    return messages, messages

# Define the Gradio interface
block = gr.Blocks()

with block:
    gr.Markdown("""<h1><center> Jarvis </center></h1>""")
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="Type here")
    state = gr.State()
    with gr.Row():
        top_k = gr.Slider(0.0, 100.0, label="top_k", value=40)
        top_p = gr.Slider(0.0, 1.0, label="top_p", value=0.9)
        temp = gr.Slider(0.0, 2.0, label="temperature", value=0.8)
    submit = gr.Button("SEND")
    submit.click(generate, inputs=[message, state, top_k, top_p, temp], outputs=[chatbot, state])

block.launch(debug=True)
