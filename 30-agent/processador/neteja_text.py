
import re

def neteja(text: str) -> str:
    t = re.sub(r"
?", "
", text)
    t = re.sub(r"
{3,}", "

", t)
    t = re.sub(r"[	 ]{2,}", " ", t)
    return t.strip()
