import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Send a simple query
# response = client.chat.completions.create(
#     model="gpt-4o-mini",  # cheaper + fast, you can use gpt-4o or gpt-3.5-turbo
#     messages=[
#         {"role": "system", "content": "You are a helpful customer support assistant."},
#         {"role": "user", "content": "What is your return policy?"}
#     ],
#     max_tokens=10  
# )

# print(response.choices[0].message.content)

response = client.responses.create(
  model="gpt-5-nano",
  input="write a haiku about ai",
  store=True,
  max_output_tokens=16
)

print(response.output_text);
