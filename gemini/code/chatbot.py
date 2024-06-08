'''
import os
import json

import google.generativeai as genai

# Configure API key (replace with your own)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Model and generation settings
model_name = "gemini-1.5-flash"  # Choose a suitable Gemini model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name=model_name, generation_config=generation_config
)

# Chat history file
chat_history_file = "chat_history.json"

# Load existing chat history if it exists
try:
    with open(chat_history_file, "r") as f:
        chat_history = json.load(f)
except FileNotFoundError:
    chat_history = []

# Start the chat session
chat_session = model.start_chat(history=chat_history)

# Main chat loop
while True:
    # Get user input
    user_input = ""
    while True:
        line = input("You: ")
        if line == "END":
            break
        user_input += line + "\n"

    # Add user input to chat history
    chat_history.append(
        {"role": "user", "parts": [user_input.strip()]}
    )  # Strip newline from user_input

    # Send message to the model
    response = chat_session.send_message(user_input)

    # Add model response to chat history
    chat_history.append(
        {"role": "model", "parts": [response.text]}
    )

    # Print model response and context length
    print(f"Gemini: {response.text}")

    # Save updated chat history to file
    with open(chat_history_file, "w") as f:
        json.dump(chat_history, f)
'''
import os
import json

import google.generativeai as genai

# Configure API key (replace with your own)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Model and generation settings
model_name = "gemini-1.5-flash"  # Choose a suitable Gemini model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name=model_name, generation_config=generation_config
)

# Chat history file
chat_history_file = "chat_history.json"
demo_file = "demo.txt"

# Load existing chat history if it exists
try:
    with open(chat_history_file, "r") as f:
        chat_history = json.load(f)
except FileNotFoundError:
    chat_history = []

# Load content from demo.txt
try:
    with open(demo_file, "r") as f:
        demo_content = f.read()
        chat_history.append(
            {"role": "user", "parts": [demo_content]}
        )
except FileNotFoundError:
    print(f"Warning: File '{demo_file}' not found. Proceeding without demo content.")

# Start the chat session
chat_session = model.start_chat(history=chat_history)

# Main chat loop
while True:
    # Get user input
    user_input = ""
    while True:
        line = input("You: ")
        if line == "END":
            break
        user_input += line + "\n"

    # Add user input to chat history
    chat_history.append(
        {"role": "user", "parts": [user_input.strip()]}
    )  # Strip newline from user_input

    # Send message to the model
    response = chat_session.send_message(user_input)

    # Add model response to chat history
    chat_history.append(
        {"role": "model", "parts": [response.text]}
    )

    # Print model response and context length
    print(f"Gemini: {response.text}")

    # Save updated chat history to file
    with open(chat_history_file, "w") as f:
        json.dump(chat_history, f)
