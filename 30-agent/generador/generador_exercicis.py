
from pathlib import Path
from typing import List
import json
from providers.model_router import get_model

def _carrega_template() -> str:
    return (Path(__file__).parent / 'prompts' / 'template-exercici.md').read_text(encoding='utf-8')

def _format_exercici(tpl: str, num: int, titol: str, objectius: list, snapshot: str, maquines: list, enunciat: str, checks: list, bonus: str) -> str:
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

def _prompt(corpus: str, semestre: str, mes_nom: str, estat_lab: dict) -> str:
    return f"""
Ets un generador d'exercicis per a un laboratori corporatiu (VMware, Windows Server 2025, Debian 13 sense GUI, Windows 11) amb domini AD `lab.local`.
Objectiu: Proposa 2-3 exercicis per al semestre {semestre}, mes {mes_nom}, alineats amb les assignatures i certificacions d'aquest semestre, utilitzant els apunts següents i l'estat real del LAB.

### Apunts consolidats (extracte)
{corpus[:4000]}

### Estat del LAB (resumit)
{json.dumps(estat_lab, ensure_ascii=False)[:4000]}

### Requisits d'estil
- Idioma: Català
- Granularitat: pas a pas, amb comandes exactes quan cal
- Debian: sense GUI
- Windows: bones pràctiques d'empresa, GPO, AD, DNS
- Inclou *Validació* i *Extres*
- Assumeix que hi ha snapshot previ si es demana

### Sortida esperada
Crea 2 o 3 exercicis breus, cadascun amb:
- Títol
- Objectius (2 punts)
- Requisits (snapshot, màquines)
- Enunciat amb passos concrets
- Validació (2 checks)
- Extres (opcional)
"""

def genera_exercicis(corpus: str, semestre: str, mes_nom: str, estat_lab: dict) -> List[str]:
    model = get_model()
    prompt = _prompt(corpus, semestre, mes_nom, estat_lab)
    resposta = model.generate(prompt)
    parts = [p.strip() for p in resposta.split('

# ') if p.strip()]
    if len(parts) < 2:
        parts = [resposta]
    tpl = _carrega_template()
    fitxers = []
    for i, bloc in enumerate(parts[:3], start=1):
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
        fitxers.append(text)
    return fitxers
