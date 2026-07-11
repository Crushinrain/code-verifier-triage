#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
h=hashlib.sha256()
for p in sorted((ROOT/'contracts').glob('*.yaml')):
    h.update(p.name.encode()); h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
print(h.hexdigest())
