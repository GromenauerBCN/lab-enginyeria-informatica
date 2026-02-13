
# Routing i NAT a SERVERLAB (RRAS)

## Configuració
1. Afegir rol Remote Access
2. Seleccionar Routing
3. Configure and Enable Routing and Remote Access
4. Triar NAT
5. Seleccionar NIC “externa”

## Validació
```powershell
Resolve-DnsName www.microsoft.com
Test-NetConnection 1.1.1.1 -CommonTCPPort HTTPS
```
```bash
dig @192.168.10.10 lab.local SOA +short
```
