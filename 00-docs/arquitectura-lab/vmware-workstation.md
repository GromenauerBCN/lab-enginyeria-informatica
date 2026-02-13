
# VMware Workstation — Configuració del LAB

## 1. Carpeta recomanada
```
/srv/vms/
   ├── serverlab/
   ├── clientlab/
   └── debianlab/
```

## 2. VMnets
- VMnet10 → intern LAB
- NAT → sortida Internet

CLIENTLAB i DEBIANLAB → només VMnet10
SERVERLAB → VMnet10 + NAT

## 3. Snapshots
```bash
vmrun -T ws snapshot "/srv/vms/serverlab/serverlab.vmx" pre-exercicis
```

## 4. Bones pràctiques
- No versionar VMs
- Rutes .vmx a 30-agent/config/lab-info.yaml
