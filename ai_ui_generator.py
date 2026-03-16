from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="Generate tkinter UI layout for chat app"
)

print(response.output_text)