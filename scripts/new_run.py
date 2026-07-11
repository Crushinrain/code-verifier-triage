#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, shutil
from pathlib import Path
import yaml
ap=argparse.ArgumentParser(); ap.add_argument('--stage', required=True); ap.add_argument('--method', required=True); ap.add_argument('--seed', type=int, required=True); ap.add_argument('--out-dir', default='runs')
a=ap.parse_args()
run_id=f"{dt.datetime.now():%Y%m%d_%H%M%S}_{a.stage}_{a.method}_seed{a.seed}"
out=Path(a.out_dir)/run_id; out.mkdir(parents=True, exist_ok=False)
template=Path(__file__).resolve().parents[1]/'templates/run_manifest.yaml'
data=yaml.safe_load(template.read_text(encoding='utf-8'))
data.update(run_id=run_id, stage=a.stage, method=a.method, seed=a.seed, started_at=dt.datetime.now(dt.timezone.utc).isoformat())
(out/'run_manifest.yaml').write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding='utf-8')
print(out)
