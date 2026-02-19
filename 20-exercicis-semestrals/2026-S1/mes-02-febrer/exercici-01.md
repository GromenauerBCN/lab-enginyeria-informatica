
# Exercici 1 - Exercici 1 (2026-S1 febrer)

## Objectius
- Aprendre i aplicar
- Operativitzar al LAB

## Requisits
- Snapshot previ: pre-exercicis
- Maquina(s) afectades: SERVERLAB, CLIENTLAB, DEBIANLAB

## Enunciat
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
   - Mapa la unitat: `New-PSDrive -Name Z -PSProvider FileSystem -Root \\serverlab.lab.local\dropbox -Persist`
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
```

```powershell
# Windows (CLIENTLAB)
Resolve-DnsName serverlab.lab.local
New-PSDrive -Name Z -PSProvider FileSystem -Root \\serverlab.lab.local\dropbox -Persist
Test-Path Z:\\hello-debian.bin
```

### Validació
- [ ] `~/lab-prog/bin/hello` existeix i s’executa a Debian (`./hello` → “Hello, World!”)
- [ ] `Z:\\hello-debian.bin` existeix a CLIENTLAB
- [ ] `Resolve-DnsName serverlab.lab.local` retorna A/AAAA esperada

### Cites dels apunts
- "Pseudocodi, codificació en C i eines per a la progra..."
- "https://aula.uoc.edu/courses/78741/pages/1-pseudocod..."

## Validació
- Proves funcionals
- Registre d'evidències

## Extres (opcional)
Documenta temps i problemes trobats.
