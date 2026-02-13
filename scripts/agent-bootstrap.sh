
#!/usr/bin/env bash
set -euo pipefail

# Bootstrap ràpid per a l'agent (executar al root del repo)
VENV=.venv-agent
AGENT_DIR=30-agent

python3 -m venv "$VENV"
"$VENV/bin/pip" install -r "$AGENT_DIR/requirements.txt"

cp -n "$AGENT_DIR/.env.example" "$AGENT_DIR/.env" || true

echo "
[OK] Entorn creat. Edita $AGENT_DIR/.env i $AGENT_DIR/config/lab-info.yaml, i posa els .vmx."
