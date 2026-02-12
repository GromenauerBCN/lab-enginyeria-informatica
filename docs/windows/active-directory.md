# Active Directory — serverlab (Windows Server 2022)

## Configuració VMware
- Xarxa: VMnet1 (Host-only)

## Configuració IP
- IP: 192.168.53.10
- Mask: 255.255.255.0
- Gateway: **192.168.53.1 (PC Host)**
- DNS: 127.0.0.1 (després 192.168.53.10)

## Domini
- Nom del domini: lab.local

## Notes
- El gateway 192.168.53.1 permet que serverlab tingui:
  - connexió amb el PC Host
  - accés a Internet si el PC Host ho permet