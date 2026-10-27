#!/usr/bin/env python3
"""Optional route regeneration. Uses external GPL FreeRouting, never vendored.
Run after build_electronics.py and route_can_pairs.py; finalization and native checks are mandatory.
"""
from pathlib import Path
import argparse,hashlib,subprocess
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--jar',required=True,type=Path);args=p.parse_args()
expected='9084a4888937a7f31f857ecc12aa7a37407f51160e4d2892dff9c9bb47ae3102'
if hashlib.sha256(args.jar.read_bytes()).hexdigest()!=expected:raise SystemExit('Expected audited FreeRouting1.9.0 JAR hash; review any version change first')
for v in ['2port','4port']:
 out=R/'exports'/v
 with (out/'routing.log').open('w') as log:
  subprocess.run(['xvfb-run','-a','java','-jar',str(args.jar.resolve()),'-de',str(out/'unrouted.dsn'),'-do',str(out/'routed.ses'),'-mp','10','-mt','1','-oit','15','-da'],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=600)
 if not (out/'routed.ses').is_file():raise SystemExit(v+': missing router output')
 print(v,'route session written; run finalize_board.py and all checks')
