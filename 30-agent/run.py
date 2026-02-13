
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import datetime as dt
import json
from pathlib import Path
from dotenv import load_dotenv
from processador.extractor import extreu_texts
from processador.neteja_text import neteja
from integracions.lab_state import recull_estat_lab
from generador.generador_exercicis import genera_exercicis

BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parent

def detecta_semestre(data: dt.date) -> str:
    any_ = data.year
    return f"{any_}-S1" if data.month <= 6 else f"{any_}-S2"

def nom_mes_ca(m: int) -> str:
    noms = ["gener","febrer","març","abril","maig","juny","juliol","agost","setembre","octubre","novembre","desembre"]
    return noms[m-1]

def main():
    parser = argparse.ArgumentParser(description="Agent del LAB – Generador d'exercicis (integrat)")
    parser.add_argument('--mes', help='Mes en format YYYY-MM (si no, avui)')
    parser.add_argument('--apunts', required=True, help='Directori amb apunts (PDF/MD/DOCX)')
    parser.add_argument('--snapshot', action='store_true', help='Fer snapshot de les VMs abans de generar')
    parser.add_argument('--push', action='store_true', help='Fer git push després d'escriure')
    parser.add_argument('--dry-run', action='store_true', help='No escriure fitxers, només mostrar paths')
    args = parser.parse_args()

    load_dotenv(BASE/'/.env', override=True)

    if args.mes:
        any_, mes = map(int, args.mes.split('-'))
        data = dt.date(any_, mes, 1)
    else:
        data = dt.date.today()

    semestre = detecta_semestre(data)
    mes_nom = nom_mes_ca(data.month)
    dest = REPO_ROOT / f"20-exercicis-semestrals/{semestre}/mes-{data.month:02d}-{mes_nom}"

    texts = extreu_texts(Path(args.apunts))
    corpus = neteja('\n'.join(texts))

    estat = recull_estat_lab(BASE / 'config' / 'lab-info.yaml', fer_snapshot=args.snapshot)

    exercicis = genera_exercicis(corpus, semestre, mes_nom, estat)

    if args.dry_run:
        print("[dry-run] Escriuria a:", dest)
        print(json.dumps(exercicis, ensure_ascii=False, indent=2))
    else:
        dest.mkdir(parents=True, exist_ok=True)
        for i, ex in enumerate(exercicis, start=1):
            out = dest / f"exercici-{i:02d}.md"
            out.write_text(ex, encoding='utf-8')
        print(f"S'han generat {len(exercicis)} exercicis a {dest}")

    if (not args.dry_run) and args.push:
        from integracions.github_push import git_commit_push
        git_commit_push(dest, f"Afegits exercicis {semestre} {mes_nom}")

if __name__ == '__main__':
    main()
