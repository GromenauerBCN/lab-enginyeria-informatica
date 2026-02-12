# Debianlab — Debian 13 Instal·lació i Configuració Base

## Configuració VMware
- Xarxa: **VMnet1 (Host-only)**
- CPU: 4 vCPU
- RAM: 4 GB
- Disc: 60 GB
- Interfície: ens32

## Configuració IP
Fitxer `/etc/network/interfaces`:

allow-hotplug ens32
iface ens32 inet static
address 192.168.53.20
netmask 255.255.255.0
gateway 192.168.53.1
dns-nameservers 192.168.53.10



📄 docs/xarxa/topologia.md (actualitzat)
Markdown
📄 docs/xarxa/ip-plan.md (actualitzat)
Markdown
🐧 docs/linux/debian-core.md (actualitzat)
MarkdownMostra més línies
allow-hotplug ens32
iface ens32 inet static
address 192.168.53.20
netmask 255.255.255.0
gateway 192.168.53.1
dns-nameservers 192.168.53.10

## Notes VMware
- Assegura que l’adaptador està configurat com:
  - Network Adapter → Custom → VMnet1