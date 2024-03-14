from groq import Groq

client = Groq()
completion = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[
        {
            "role": "user",
            "content": str(input(" Enter quesrion "))
        },
        {
            "role": "assistant",
            "content": "Hello! I'm an assistant designed to help answer your questions and assist you with various tasks. How can I help you today?"
        }
    ],
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
