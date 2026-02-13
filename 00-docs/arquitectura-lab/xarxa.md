
# Xarxa del LAB

## 1. Objectiu del disseny
Simular una xarxa corporativa petita però realista, amb:
- Segment intern aïllat (`VMnet10`)
- Servidor Windows actuant com a Gateway + DNS + AD
- Sortida a Internet a través del servidor
- Clients heterogenis (Windows 11 + Debian sense GUI)

## 2. Esquemàtica de xarxa
```
[ Internet ]
      |
 [NIC pública - NAT/Bridged]
      |
[ SERVERLAB - Windows Server 2025 ]
  NIC1: VMnet10   -> 192.168.10.10 (GW+DNS+AD+RRAS)
  NIC2: NAT/Bridge (sortida externa)
      |
   -----------------------------
   |                           |
[CLIENTLAB Win11]       [DEBIANLAB]
192.168.10.20           192.168.10.30
DNS: 192.168.10.10      DNS: 192.168.10.10
GW: 192.168.10.10       GW: 192.168.10.10
```

## 3. Assignació d’adreces IP (estàtiques)
| Màquina       | IP              | DNS | GW |
|---------------|------------------|-----|----|
| SERVERLAB     | 192.168.10.10    | -   | -  |
| CLIENTLAB     | 192.168.10.20    | 192.168.10.10 | 192.168.10.10 |
| DEBIANLAB     | 192.168.10.30    | 192.168.10.10 | 192.168.10.10 |

## 4. Domini corporatiu
- Nom DNS del domini: **lab.local**
- Controlador de Domini: **SERVERLAB**
- Zona DNS: `lab.local` + `_msdcs.lab.local`

## 5. Requisits
- DNS intern obligatori
- Hora sincronitzada
- RRAS NAT operatiu

## 6. Validacions
### Windows
```powershell
Resolve-DnsName serverlab.lab.local
Test-NetConnection 8.8.8.8 -CommonTCPPort HTTPS
```
### Debian
```bash
dig @192.168.10.10 lab.local SOA +short
curl -I https://www.microsoft.com
```
