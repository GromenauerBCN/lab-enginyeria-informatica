
# Troubleshooting LDAP
```bash
ldapsearch -x -H ldap://serverlab.lab.local -D manel-ro@lab.local -w 'PASS'  -b DC=lab,DC=local -z 5 '(objectClass=user)' cn sAMAccountName
```
