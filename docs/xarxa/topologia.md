# Topologia del Laboratori (VMware Workstation)

## Xarxa virtual
- Segment: **VMnet1 (Host-Only)**
- Subxarxa: 192.168.53.0/24
- Gateway: **192.168.53.1 (PC Host)**
- DHCP: desactivat (DHCP gestionat per serverlab)
- Domini AD: lab.local

## Màquines
| Màquina     | IP             | Gateway        | Funció                      |
|-------------|----------------|----------------|-----------------------------|
| PC Host     | 192.168.53.1   | —              | Gateway del LAB             |
| serverlab   | 192.168.53.10  | 192.168.53.1   | AD / DNS / DHCP / GPO       |
| debianlab   | 192.168.53.20  | 192.168.53.1   | Serveis Linux               |
| clientlab   | 192.168.53.30  | 192.168.53.1   | Client Windows (IP fixa)    |

## Notes
- El PC Host actua com **gateway** del laboratori.
- Això permet: accés al host, navegació (si el host té Internet Sharing), ping extern, etc.
- Les proves del domini AD funcionen igual.