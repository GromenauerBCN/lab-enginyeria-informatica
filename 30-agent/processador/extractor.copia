
from pathlib import Path
from typing import List
from PyPDF2 import PdfReader
from docx import Document

def _pdf_to_text(path: Path) -> str:
    try:
        reader = PdfReader(str(path))
        texts = [page.extract_text() or '' for page in reader.pages]
        return '
'.join(texts)
    except Exception as e:
        return f"[ERROR extreient PDF {path.name}: {e}]"

def _docx_to_text(path: Path) -> str:
    try:
        doc = Document(str(path))
        return '
'.join(p.text for p in doc.paragraphs)
    except Exception as e:
        return f"[ERROR extreient DOCX {path.name}: {e}]"

def _md_to_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore')

def extreu_texts(dir_apunts: Path) -> List[str]:
    texts = []
    for p in sorted(dir_apunts.glob('**/*')):
        if p.is_dir():
            continue
        if p.suffix.lower() == '.pdf':
            texts.append(_pdf_to_text(p))
        elif p.suffix.lower() in ('.md', '.markdown', '.txt'):
            texts.append(_md_to_text(p))
        elif p.suffix.lower() in ('.docx', ):
            texts.append(_docx_to_text(p))
    return texts
