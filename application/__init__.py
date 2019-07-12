import os
from pathlib import Path

with open(str(Path(__file__).parent.parent) + '/variables.env') as f:
    for line in f:
        if line.startswith('#'):
            continue
        if '=' not in line:
            continue
        key, value = line.strip().split('=', 1)
        os.environ[key] = value
