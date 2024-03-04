import streamlit as st
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

# Streamlit app
st.title("Chatbot")

# Sidebar for conversation selection
st.sidebar.title("Conversations")
saved_conversations = list_saved_conversations()
if saved_conversations:
    selected_conversation = st.sidebar.selectbox("Select a conversation", ["New Conversation"] + saved_conversations)
    if selected_conversation != "New Conversation":
        conversation_history = load_conversation(selected_conversation)
    else:
        conversation_history = []
else:
    conversation_history = []

# Main chat interface
st.write("Conversation:")
for message in conversation_history:
    st.write(f"{message['role'].capitalize()}: {message['content']}")

user_input = st.text_input("Type your message here:")
if st.button("Send"):
    context = retriever.invoke(user_input)
    formatted_prompt = f"Question: {user_input}\n\nContext: {context}"

    conversation_history.append({"role": "user", "content": formatted_prompt})

    response = client.chat.completions.create(
        messages=conversation_history,
        model="mixtral-8x7b-32768" # Replace with your model ID
    )

    assistant_response = response.choices[0].message.content

    conversation_history.append({"role": "assistant", "content": assistant_response})

    st.write(f"Assistant: {assistant_response}")

# Option to save the chat
save_chat = st.checkbox("Do you want to save this chat?")
if save_chat:
    file_name = st.text_input("Enter a name for the conversation file:")
    if st.button("Save"):
        save_conversation(conversation_history, file_name)
        st.success("Chat saved successfully.")

