
import os
import requests

class AzureOpenAIProvider:
    def __init__(self):
        self.endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.key = os.getenv('AZURE_OPENAI_API_KEY')
        self.deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        self.api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-08-01-preview')
    def generate(self, prompt: str) -> str:
        if not (self.endpoint and self.key and self.deployment):
            raise RuntimeError("Variables d'entorn Azure OpenAI no definides")
        url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
        headers = {"api-key": self.key, "Content-Type": "application/json"}
        body = {"messages": [{"role": "system", "content": "Ets un generador d'exercicis en català."},{"role": "user", "content": prompt}],"temperature": 0.4}
        r = requests.post(url, headers=headers, json=body, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data['choices'][0]['message']['content']
