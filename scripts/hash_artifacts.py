#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

ap=argparse.ArgumentParser(); ap.add_argument('paths', nargs='+'); ap.add_argument('--out', default='artifact_hashes.json')
a=ap.parse_args(); records=[]
for raw in a.paths:
    p=Path(raw)
    if p.is_dir(): files=sorted(x for x in p.rglob('*') if x.is_file())
    else: files=[p]
    for f in files: records.append({'path':str(f), 'bytes':f.stat().st_size, 'sha256':sha256(f)})
Path(a.out).write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'wrote {len(records)} records to {a.out}')
