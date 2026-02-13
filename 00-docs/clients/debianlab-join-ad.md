
# DEBIANLAB — Debian 13 (sense GUI)

## Join a AD
```bash
sudo apt install realmd sssd adcli krb5-user
sudo realm join lab.local -U manel-admin
```

## Validació
```bash
id manel.student@lab.local
kinit manel.student@lab.local
```
