from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

answer = client.responses.create(
    model="gpt-5",
    input="Who is the current president of France?",
    tools=[{"type": "web_search_preview"}]
)

print(answer.output_text)