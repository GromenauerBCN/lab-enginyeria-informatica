
import os
import requests

class OllamaProvider:
    def __init__(self):
        self.base = os.getenv('OLLAMA_BASE', 'http://localhost:11434')
        self.model = os.getenv('OLLAMA_MODEL', 'llama3.1')
    def generate(self, prompt: str) -> str:
        url = f"{self.base}/api/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        r = requests.post(url, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data.get('response', '')
