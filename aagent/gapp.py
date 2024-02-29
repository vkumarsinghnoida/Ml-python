#!/root/miniconda3/envs/aagent/bin/python3

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
