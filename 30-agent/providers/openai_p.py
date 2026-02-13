
import os
import requests

class OpenAIProvider:
    def __init__(self):
        self.key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    def generate(self, prompt: str) -> str:
        if not self.key:
            raise RuntimeError('OPENAI_API_KEY no definit')
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        body = {"model": self.model, "messages": [{"role": "system", "content": "Ets un generador d'exercicis en català."},{"role": "user", "content": prompt}],"temperature": 0.4}
        r = requests.post(url, headers=headers, json=body, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data['choices'][0]['message']['content']
