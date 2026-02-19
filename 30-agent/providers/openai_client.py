import os

from typing import Optional
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # carrega el .env més proper (normalment ../.env)


class OpenAIClient:
    """
    Client generador de text basat en OpenAI (GPT-5.x).
    Manté la interfície .generate(prompt) compatible amb el teu agent.
    """

    def __init__(self):
        # API key (obligatòria)
        self.api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("Falta OPENAI_API_KEY al .env")

        # Model (pots canviar a gpt-5, gpt-5.1, gpt-5.2, o snapshot pin)
        self.model: str = os.getenv("OPENAI_MODEL", "gpt-5.2")

        # Paràmetres opcionals
        self.temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))

        # Client oficial OpenAI
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        """
        Envia un prompt a OpenAI i retorna text pla.
        """
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
            )
            content = resp.choices[0].message.content
            return content.strip() if content else ""
        except Exception as e:
            raise RuntimeError(f"Error generant text amb OpenAI ({self.model}): {e}") from e
