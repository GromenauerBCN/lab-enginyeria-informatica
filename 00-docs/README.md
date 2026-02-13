
# Documentació del LAB — lab.enginyeria-informatica

Aquest directori conté la **documentació tècnica completa** del LAB corporatiu que estàs construint amb:

- **Windows Server 2025** (SERVERLAB)
- **Windows 11** (CLIENTLAB)
- **Debian 13 sense GUI** (DEBIANLAB)
- **VMware Workstation** com a hipervisor
- **AD DS** domini `lab.local`
- **DNS intern** amb forwarders públics
- **RRAS NAT** per donar sortida a tot el segment intern

## Estructura del directori

### `arquitectura-lab/`
Conté la definició de xarxa, topologia, VMnets, configuració VMware Workstation i NAT corporatiu.

### `servidor-windows/`
Documentació del Windows Server 2025: rols instal·lats, configuració d’AD DS, DNS, RRAS, GPOs i checklists d’operació.

### `clients/`
Guies de configuració i diagnosi del client Windows 11 (CLIENTLAB) i del Debian 13 integrat a AD (DEBIANLAB).

### `seguretat-lab/`
Bones pràctiques: snapshots, control de canvis, gestió de credencials i secrets.

### `troubleshooting/`
Guies de resolució de problemes: DNS, Kerberos, LDAP, vmrun i AD.

## Estil
- **Idioma:** Català
- **Nivell:** professional (estil d’empresa)
- **Objectiu:** documentació estable per a un LAB de llarga durada (estudis 2026–2032)
