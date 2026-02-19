import os

def get_model():
    """
    Retorna el client del model segons MODEL_PROVIDER.
      1) MODEL_PROVIDER=openai -> OpenAIClient
      2) MODEL_PROVIDER=ollama -> Ollama
      3) Per defecte -> OpenAIClient (fallback segur)
    """
    provider = os.getenv("MODEL_PROVIDER", "openai").lower().strip()

    if provider == "openai":
        from providers.openai_client import OpenAIClient  # import mandrós
        return OpenAIClient()

    if provider == "ollama":
        try:
            from providers.ollama import Ollama  # només si cal
        except Exception as e:
            raise RuntimeError(
                "MODEL_PROVIDER=ollama però no s'ha pogut importar providers.ollama: %s" % e
            )
        return Ollama()

    # Fallback segur: OpenAI
    from providers.openai_client import OpenAIClient
    return OpenAIClient()
