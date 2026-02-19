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

    lines = [
        "### Passos",
        "1) A **DEBIANLAB**, crea el projecte:",
        "   - Directori: `~/lab-prog/src`",
        "   - Fitxer: `~/lab-prog/src/hello.c` amb el clàssic *Hello, World!* (tal com apareix als apunts).",
        "2) Compila a Debian:",
        "   - `mkdir -p ~/lab-prog/bin`",
        "   - `gcc -O2 -Wall -o ~/lab-prog/bin/hello ~/lab-prog/src/hello.c`",
        "3) Publica l’artefacte al **SERVERLAB** via SMB:",
        "   - Munta la compartició: `sudo mount -t cifs //serverlab.lab.local/dropbox /mnt -o username=LAB\\\\manel-admin`",
        "   - Copia: `cp ~/lab-prog/bin/hello /mnt/hello-debian.bin`",
        "4) A **CLIENTLAB (Windows)**, verifica **DNS** i recull l’artefacte:",
        "   - PowerShell: `Resolve-DnsName serverlab.lab.local`",
        "   - Mapa la unitat: `New-PSDrive -Name Z -PSProvider FileSystem -Root \\\\serverlab.lab.local\\dropbox -Persist`",
        "   - Comprova: `Test-Path Z:\\\\hello-debian.bin`",
        "5) Evidències:",
        "   - Captures de `gcc` i del fitxer a `Z:\\\\`",
        "   - Sortida de `Resolve-DnsName`",
        "",
        "### Comandes (copiar i enganxar)",
        "```bash",
        "# Debian",
        "mkdir -p ~/lab-prog/src ~/lab-prog/bin",
        "cat > ~/lab-prog/src/hello.c <<'EOF'",
        "#include <stdio.h>",
        "int main(){ printf(\"Hello, World!\\n\"); return 0; }",
        "EOF",
        "gcc -O2 -Wall -o ~/lab-prog/bin/hello ~/lab-prog/src/hello.c",
        "sudo mount -t cifs //serverlab.lab.local/dropbox /mnt -o username=LAB\\\\manel-admin",
        "cp ~/lab-prog/bin/hello /mnt/hello-debian.bin",
        "```",
        "",
        "```powershell",
        "# Windows (CLIENTLAB)",
        "Resolve-DnsName serverlab.lab.local",
        "New-PSDrive -Name Z -PSProvider FileSystem -Root \\\\serverlab.lab.local\\dropbox -Persist",
        "Test-Path Z:\\\\hello-debian.bin",
        "```",
        "",
        "### Validació",
        "- [ ] `~/lab-prog/bin/hello` existeix i s’executa a Debian (`./hello` → “Hello, World!”)",
        "- [ ] `Z:\\\\hello-debian.bin` existeix a CLIENTLAB",
        "- [ ] `Resolve-DnsName serverlab.lab.local` retorna A/AAAA esperada",
        "",
        "### Cites dels apunts",
    ]
    enunciat = "\n".join(lines) + "\n" + "\n".join([f'- \"{c}\"' for c in cites])
    return enunciat.strip()


def _prompt(corpus: str, semestre: str, mes_nom: str, estat_lab: dict) -> str:
    """Prompt que prioritza apunts i autoritza baseline del LAB; prohibeix l'avís 'Sense context...'."""
    estat_compacte = json.dumps(estat_lab, ensure_ascii=False)[:1800]
    patterns = (
        "- **Pattern A (Debian → C → artefacte)**: compilar amb gcc; copiar a SERVERLAB via SMB; validar a Windows.\n"
        "- **Pattern B (Windows → DNS/AD)**: Resolve-DnsName / Test-NetConnection; recollir artefactes; logs a C:\\Lab\\logs.\n"
        "- **Pattern C (Debian → diagnosi)**: dig, curl -I; script Bash amb set -euo pipefail; retorn 0/1.\n"
        "- **Pattern D (Intercanvi Win/Debian)**: smbclient / mount -t cifs; validar timestamps i mides."
    )
    return (
        "Ets un generador d'exercicis per al LAB corporatiu (VMware, Windows Server 2025, Debian 13 sense GUI, "
        "Windows 11, AD 'lab.local').\n\n"
        "INSTRUCCIONS CLAU:\n"
        "- PRIORITZA el llenguatge i conceptes dels APUNTS (pseudocodi, C, algorismes) com a base pedagògica.\n"
        "- APLICA'ls al LAB real utilitzant els patterns (tria 2–3).\n"
        "- NO inventis teoria absent als apunts.\n"
        "- **NO** escriguis la frase exacta \"[Sense context suficient als apunts per cobrir aquesta secció, cal aportar més material]\" "
        "ni variants: si falta teoria, adapta els patterns igualment i dóna passos concrets del LAB.\n\n"
        "### APUNTS (extracte fidel – màx. 4.000 caràcters)\n" + corpus[:4000] + "\n\n"
        "### ESTAT DEL LAB (resum – màx. 1.800 caràcters)\n" + estat_compacte + "\n\n"
        "### PATTERNS\n" + patterns + "\n\n"
        "### FORMAT OBLIGATORI PER CADA EXERCICI\n"
        "- Títol específic\n"
        "- Objectius (2 punts)\n"
        "- Requisits (snapshot, màquines i rutes)\n"
        "- **Enunciat** amb:\n"
        "  - **### Passos (numerats)** (5–10 accions específiques)\n"
        "  - **### Comandes (copiar i enganxar)** (Bash/PowerShell)\n"
        "  - **### Validació** (2–4 checks mesurables)\n"
        "  - **### Cites dels apunts** (2 cites curtes literalment extretes dels apunts)\n"
        "- Extres (opcional)\n\n"
        "Genera 2 o 3 exercicis amb aquest format.\n"
    )


def _split_blocs(resposta: str) -> list[str]:
    """Separa per capçaleres '# ...'; si no n'hi ha, per dobles salts de línia."""
    r = resposta.replace("\r\n", "\n").replace("\r", "\n").strip()
    parts = re.split(r"\n(?=#+\s)", r)  # línies que comencen per '#','##',...
    if len(parts) <= 1:
        parts = [p for p in r.split("\n\n") if p.strip()]
    return [p.strip() for p in parts if p.strip()]


def _ensure_sections(text: str) -> str:
    """Assegura que Enunciat tingui Passos, Comandes, Validació i Cites."""
    if "### Passos" not in text:
        text = text.replace("## Enunciat", "## Enunciat\n\n### Passos\n1) Acció a DEBIANLAB\n2) Acció a CLIENTLAB\n3) Acció a SERVERLAB", 1)
    if "### Comandes" not in text:
        text += "\n\n### Comandes (copiar i enganxar)\n```bash\n# Debian\nuname -a\n```\n```powershell\n# Windows\nGet-ComputerInfo | Select-Object OsName,OsVersion\n```"
    if "### Validació" not in text:
        text += "\n\n### Validació\n- [ ] Evidència 1\n- [ ] Evidència 2"
    if "### Cites dels apunts" not in text:
        text += '\n\n### Cites dels apunts\n- "Cita curta 1 dels apunts"\n- "Cita curta 2 dels apunts"'
    return text


def genera_exercicis(corpus: str, semestre: str, mes_nom: str, estat_lab: dict) -> List[str]:
    """
    Retorna SEMPRE una llista (pot ser buida) de fins a 3 exercicis.
    Substitueix qualsevol bloc amb 'Sense context...' o massa curt pel fallback estable.
    """
    fitxers: List[str] = []
    try:
        model = get_model()
        prompt = _prompt(corpus, semestre, mes_nom, estat_lab)
        resposta = model.generate(prompt)
        if not resposta:
            return []

        parts = _split_blocs(resposta)
        if not parts:
            parts = [resposta.strip()]

        tpl = _carrega_template()
        guard_substr = "Sense context suficient als apunts"
        for i, bloc in enumerate(parts[:3], start=1):
            if guard_substr in bloc or len(bloc) < 200:
                bloc = _fallback_exercici(corpus, semestre, mes_nom, i)

            titol = f"Exercici {i} ({semestre} {mes_nom})"
            text = _format_exercici(
                tpl, i, titol,
                ["Aprendre i aplicar", "Operativitzar al LAB"],
                "pre-exercicis",
                ["SERVERLAB", "CLIENTLAB", "DEBIANLAB"],
                bloc,
                ["Proves funcionals", "Registre d'evidències"],
                "Documenta temps i problemes trobats."
            )
            text = _ensure_sections(text)
            fitxers.append(text)

        return fitxers
    except Exception as e:
        print(f"[ERROR] genera_exercicis ha fallat: {e}")
        return []
