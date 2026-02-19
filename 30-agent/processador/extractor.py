from pathlib import Path
from typing import List
from PyPDF2 import PdfReader
from docx import Document

def _pdf_to_text(path: Path) -> str:
    try:
        reader = PdfReader(str(path))
        # extract_text() pot retornar None; el convertim a cadena buida
        texts = [(page.extract_text() or "") for page in reader.pages]
        return "\n".join(texts)
    except Exception as e:
        return f"[ERROR extreient PDF {path.name}: {e}]"

def _docx_to_text(path: Path) -> str:
    try:
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        return f"[ERROR extreient DOCX {path.name}: {e}]"

def _md_to_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def extreu_texts(dir_apunts: Path) -> List[str]:
    texts: List[str] = []
    for p in sorted(dir_apunts.glob("**/*")):
        if p.is_dir():
            continue
        suffix = p.suffix.lower()
        if suffix == ".pdf":
            texts.append(_pdf_to_text(p))
        elif suffix in (".md", ".markdown", ".txt"):
            texts.append(_md_to_text(p))
        elif suffix in (".docx",):
            texts.append(_docx_to_text(p))
    return texts