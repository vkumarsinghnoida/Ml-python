import gradio as gr
import os
from groq import Groq

def fetch_response(user_input):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "you are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
        model="mixtral-8x7b-32768",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False
    )
    return chat_completion.choices[0].message.content

def list_saved_conversations():
    chats_dir = "chats"
    if not os.path.exists(chats_dir):
        os.makedirs(chats_dir)
    return [f for f in os.listdir(chats_dir) if f.endswith('.txt')]

def load_conversation(file_name):
    chats_dir = "chats"
    file_path = os.path.join(chats_dir, file_name)
    with open(file_path, 'r') as file:
        conversation_history = [line.strip() for line in file.readlines()]
    return conversation_history

def save_conversation(conversation_history, file_name):
    chats_dir = "chats"
    if not os.path.exists(chats_dir):
        os.makedirs(chats_dir)
    file_path = os.path.join(chats_dir, f"{file_name}.txt")
    with open(file_path, 'w') as file:
        for message in conversation_history:
            file.write(f"{message}\n")

# Create a Gradio chat interface
iface = gr.Interface(fn=fetch_response, inputs="text", outputs="text", title="Groq Chatbot", description="Ask a question and get a response.")
iface.launch()

# After the chat session, you can implement the conversation history selector and saving functionality
# This part is not directly integrated into the Gradio interface and would require additional user input or UI elements outside of Gradio
