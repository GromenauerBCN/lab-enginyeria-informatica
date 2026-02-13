
import subprocess
from pathlib import Path

def git_commit_push(path: Path, missatge: str):
    subprocess.check_call(['git', 'add', str(path)])
    subprocess.check_call(['git', 'commit', '-m', missatge])
    subprocess.check_call(['git', 'push'])
