
import os
import subprocess
from pathlib import Path
from typing import Dict, Any
import yaml

def _run(cmd: list, timeout=30) -> str:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=timeout)
        return out.decode('utf-8', errors='ignore')
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"[ERROR execució {' '.join(cmd)}: {e}]"

def _vm_snapshot_all(vmware_cfg: dict):
    vmrun = vmware_cfg.get('vmrun_path', 'vmrun')
    vmx = vmware_cfg.get('vmx_paths', {})
    report = {}
    for nom, ruta in vmx.items():
        if not ruta or not Path(ruta).exists():
            report[nom] = f"vmx no trobat: {ruta}"
            continue
        snap_name = 'pre-exercicis'
        out = _run([vmrun, '-T', 'ws', 'snapshot', ruta, snap_name])
        report[nom] = out.strip() or 'OK'
    return report

def _dns_check(dns_ip: str, domini: str) -> Dict[str, Any]:
    res = {}
    res['soa'] = _run(['dig', f"@{dns_ip}", domini, 'SOA', '+short'])
    res['dc_srv'] = _run(['dig', f"@{dns_ip}", f"_ldap._tcp.dc._msdcs.{domini}", 'SRV', '+short'])
    return res

def _ad_query(ad_host: str, base_dn: str) -> Dict[str, Any]:
    user = os.environ.get('AD_BIND_USER')
    pwd = os.environ.get('AD_BIND_PASSWORD')
    if not user or not pwd:
        return {"info": "AD_BIND_USER/AD_BIND_PASSWORD no definits; saltant consulta AD"}
    q_users = _run(['ldapsearch', '-x', '-H', f"ldap://{ad_host}", '-D', user, '-w', pwd, '-b', base_dn, '(objectClass=user)', 'cn', 'sAMAccountName', '-z', '5'])
    q_comps = _run(['ldapsearch', '-x', '-H', f"ldap://{ad_host}", '-D', user, '-w', pwd, '-b', base_dn, '(objectClass=computer)', 'cn', 'dNSHostName', '-z', '5'])
    return {"users_sample": q_users, "computers_sample": q_comps}

def recull_estat_lab(cfg_path: Path, fer_snapshot=False) -> Dict[str, Any]:
    cfg = yaml.safe_load(Path(cfg_path).read_text(encoding='utf-8'))
    domini = cfg['domini']
    vmware = cfg['vmware']
    out = {'domini': domini,'vmware': {'vmx_paths': vmware.get('vmx_paths', {})},'checks': {}}
    if fer_snapshot:
        out['checks']['snapshots'] = _vm_snapshot_all(vmware)
    out['checks']['dns'] = _dns_check(domini['dns_server'], domini['nom_dns'])
    out['checks']['ad'] = _ad_query(domini['ad_host'], domini['base_dn'])
    return out
