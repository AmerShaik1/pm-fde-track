# pip install openai>=1.3.0
# pip install azure-ai-projects azure-identity openai

import os
from openai import OpenAI

client = OpenAI(
    base_url=f"{os.environ['AZURE_OPENAI_ENDPOINT']}/openai/v1/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"]
)

response = client.responses.create(
    model=os.environ["grok-4.6"],          # e.g., "gpt-4o-mini"
    input=[{"role": "system", "content": "You're a helpful assistant."},
           {"role": "user", "content": "Summarize the key points from our release notes in 3 bullets."}],
    max_output_tokens=300,
    temperature=0.2
)

print(response.output_text)