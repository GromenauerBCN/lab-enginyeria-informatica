
# Rols del Windows Server 2025 — SERVERLAB

- AD DS (lab.local)
- DNS Server
- RRAS NAT
- RDP habilitat

## OUs
- LAB-USERS
- LAB-COMPUTERS

## Validació
```powershell
Get-ADDomain
Get-ADUser -Filter * -SearchBase "OU=LAB-USERS,DC=lab,DC=local"
```
