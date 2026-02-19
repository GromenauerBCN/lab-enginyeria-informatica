# -*- coding: utf-8 -*-
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
        body = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Ets un generador d'exercicis en català. "
                        "NO inventis contingut que no aparegui als apunts proporcionats. "
                        "Si falta context, digues-ho explícitament."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1800,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0
            # "seed": 42  # Descomenta per estabilitat entre execucions
        }
        r = requests.post(url, headers=headers, json=body, timeout=150)
        r.raise_for_status()
        data = r.json()
        return data['choices'][0]['message']['content']
