from dotenv import load_dotenv
load_dotenv()
import os
import anthropic

key = os.getenv('ANTHROPIC_API_KEY')
print(f'Key found: {bool(key)}')
print(f'Key preview: {key[:15] if key else "NONE"}')

client = anthropic.Anthropic(api_key=key)
msg = client.messages.create(
    model='claude-haiku-4-5-20251001',
    max_tokens=50,
    messages=[{'role': 'user', 'content': 'Give me ONLY the Paiboon romanization for this Thai word: ภิกษุ. Just the romanization, nothing else.'}]
)
print(f'Response: {msg.content[0].text}')
