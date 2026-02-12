# IP Plan — Xarxa 192.168.53.0/24

## Dades generals
- Segment VMware: VMnet1 (Host-only)
- Subxarxa: 192.168.53.0/24
- Gateway del LAB: **192.168.53.1 (PC Host)**
- DNS principal: 192.168.53.10 (serverlab)
- Domini: lab.local

## IPs estàtiques
| Host/Màquina | IP             | Gateway        | Notes                       |
|--------------|----------------|----------------|------------------------------|
| PC Host      | 192.168.53.1   | —              | Gateway del LAB              |
| serverlab    | 192.168.53.10  | 192.168.53.1   | DC/DNS/DHCP                  |
| debianlab    | 192.168.53.20  | 192.168.53.1   | Linux                        |
| clientlab    | 192.168.53.30  | 192.168.53.1   | Windows Client (IP fixa)     |

## DHCP del domini
- Scope: 192.168.53.50 – 192.168.53.200

### Exclusions
- 192.168.53.10  
- 192.168.53.20  
- 192.168.53.30  

## Notes
- El PC Host proporciona connectivitat i pot compartir la seva sortida a Internet.