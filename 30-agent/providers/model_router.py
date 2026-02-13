
import os
from providers.ollama import OllamaProvider
from providers.openai_p import OpenAIProvider
from providers.azure_openai_p import AzureOpenAIProvider

def get_model():
    order = [s.strip() for s in os.getenv('PROVIDER_ORDER', 'ollama,openai,azure').split(',')]
    for p in order:
        if p == 'ollama':
            return OllamaProvider()
        if p == 'openai':
            return OpenAIProvider()
        if p == 'azure':
            return AzureOpenAIProvider()
    return OllamaProvider()
