import re

def neteja(text: str) -> str:
    # Normalitza finals de línia
    t = text.replace("\r\n", "\n").replace("\r", "\n")

    # Substitueix opcional CR/LF estranys per un sol salt de línia
    t = re.sub(r"\n+", "\n", t)

    # Converteix múltiples espais en un
    t = re.sub(r"[ ]{2,}", " ", t)

    return t.strip()