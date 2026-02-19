# -*- coding: utf-8 -*-
from pathlib import Path
from typing import List
import json
import re

from providers.model_router import get_model


def _carrega_template() -> str:
    return (Path(__file__).parent / 'prompts' / 'template-exercici.md').read_text(encoding='utf-8')


def _format_exercici(
    tpl: str,
    num: int,
    titol: str,
    objectius: list,
    snapshot: str,
    maquines: list,
    enunciat: str,
    checks: list,
    bonus: str,
) -> str:
    out = tpl
    out = out.replace('{{NUM}}', str(num))
    out = out.replace('{{TITOL}}', titol)
    out = out.replace('{{objectiu1}}', objectius[0] if objectius else '')
    out = out.replace('{{objectiu2}}', objectius[1] if len(objectius) > 1 else '')
    out = out.replace('{{snapshot}}', snapshot)
    out = out.replace('{{maquines}}', ', '.join(maquines))
    out = out.replace('{{enunciat}}', enunciat)
    out = out.replace('{{check1}}', checks[0] if checks else '')
    out = out.replace('{{check2}}', checks[1] if len(checks) > 1 else '')
    out = out.replace('{{bonus}}', bonus)
    return out


def _quotes_from_corpus(corpus: str, n: int = 2, max_len: int = 140) -> list[str]:
    """Extreu n cites curtes del corpus (frases de 30..max_len caràcters)."""
    sents = re.split(r'(?<=[\.\!\?])\s+|\n+', corpus.strip())
    out: list[str] = []
    for s in sents:
        s = s.strip()
        if 30 <= len(s) <= max_len:
            out.append(s)
        if len(out) == n:
            break
    if len(out) < n:
        base = corpus.strip().replace('\n', ' ')
        if base:
            out.append(base[:max_len].strip())
        if len(out) < n and len(base) > max_len:
            out.append(base[max_len:max_len*2].strip())
    return out[:n]


def _fallback_exercici(corpus: str, semestre: str, mes_nom: str, idx: int) -> str:
    """Exercici estable si el model respon amb 'Sense context...' o massa curt."""
    cites = _quotes_from_corpus(corpus, n=2, max_len=140)

    enunciat = """
### Passos
1) A **DEBIANLAB**, crea el projecte:
   - Directori: `~/lab-prog/src`
   - Fitxer: `~/lab-prog/src/hello.c` amb el clàssic *Hello, World!* (tal com apareix als apunts).
2) Compila a Debian:
   - `mkdir -p ~/lab-prog/bin`
   - `gcc -O2 -Wall -o ~/lab-prog/bin/hello ~/lab-prog/src/hello.c`
3) Publica l’artefacte al **SERVERLAB** via SMB:
   - Munta la compartició: `sudo mount -t cifs //serverlab.lab.local/dropbox /mnt -o username=LAB\\manel-admin`
   - Copia: `cp ~/lab-prog/bin/hello /mnt/hello-debian.bin`
4) A **CLIENTLAB (Windows)**, verifica **DNS** i recull l’artefacte:
   - PowerShell: `Resolve-DnsName serverlab.lab.local`
   - Mapa la unitat: `New-PSDrive -Name Z -PSProvider FileSystem -Root \\serverlab.lab.local\\dropbox -Persist`
   - Comprova: `Test-Path Z:\\hello-debian.bin`
5) Evidències:
   - Captures de `gcc` i del fitxer a `Z:\\`
   - Sortida de `Resolve-DnsName`

### Comandes (copiar i enganxar)
```bash
# Debian
mkdir -p ~/lab-prog/src ~/lab-prog/bin
cat > ~/lab-prog/src/hello.c <<'EOF'
#include <stdio.h>
int main(){ printf("Hello, World!\n"); return 0; }
EOF
gcc -O2 -Wall -o ~/lab-prog/bin/hello ~/lab-prog/src/hello.c
sudo mount -t cifs //serverlab.lab.local/dropbox /mnt -o username=LAB\\manel-admin
cp ~/lab-prog/bin/hello /mnt/hello-debian.bin