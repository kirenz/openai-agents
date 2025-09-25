from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

MODEL = "gpt-5-nano"

response = client.responses.create(
    model=MODEL,
    tools=[{"type": "web_search"}],
    input="What was a positive news story from today in Stuttgart?"
)

print(response.output_text)