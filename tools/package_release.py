#!/usr/bin/env python3
"""Build separate review PCB and housing archives from a validated snapshot."""
from pathlib import Path
import json,zipfile,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(R/'tools/validate_release.py')],cwd=R,check=True)
manifest=json.loads((R/'releases/manifest.json').read_text());revision=manifest['revision']
common=['LICENSE','THIRD_PARTY.md','ASSEMBLY.md','docs/manufacturing.md','docs/interface-and-protection.md','docs/release-checklist.md','research/connector-sourcing.md','research/j47-footprint-audit.md','research/igx-compatibility.md','releases/manifest.json']
common += [str(p.relative_to(R)) for folder in ['docs','research','preview'] for p in (R/folder).glob('*') if p.suffix in {'.md','.json','.png'}]
common += ['exports/enclosure-bom.csv']
packages={}
for v in ['2port','4port']:
 files=common+[str(p.relative_to(R)) for directory in [R/'hardware'/v,R/'hardware/Thor.pretty',R/'exports'/v] for p in directory.rglob('*') if p.is_file() and p.suffix not in ['.log','.dsn','.ses']]+['hardware/interface.json','research/j47-footprint-measurements.json']
 packages[f'thor-{revision}-{v}-pcb']=files
parts=json.loads((R/'exports/geometry-checks.json').read_text())
packages[f'thor-{revision}-housings']=common+[f'exports/{p}.{ext}' for p in parts for ext in ['stl','step','3mf']]+[str(p.relative_to(R)) for p in (R/'preview').glob('*.png')]+['cad/parameters.json','exports/geometry-checks.json','research/enclosure-hardware.md','research/mating-dsub-measurements.json']+[f'exports/{v}/{f}.json' for v in ['2port','4port'] for f in ['mechanical-checks','assembly-paths']]
checksums=[]
for name,files in packages.items():
 out=R/'releases'/f'{name}.zip';hashes=[]
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  for rel in sorted(set(files)):
   data=(R/rel).read_bytes();z.writestr(rel,data);hashes.append(hashlib.sha256(data).hexdigest()+'  '+rel)
  readme=f'# {name}\n\nA0 engineering prototype / NOT PRODUCTION RELEASED.\n\nFor PCB quoting: see docs/manufacturing.md, then exports/<variant>/ for the Gerber/drill review ZIP and assembly population files. J1 Wieson procurement/consignment is unresolved. Inspect the schematic, layers and placement before ordering any prototype.\n\nFor printing: choose one matching base/lid pair plus ribbon_clamp; print coupons first. Files are millimeters. Read ASSEMBLY.md for hardware, pads, fasteners and cable pull testing.\n\nNo physical fit, signal-integrity or transient qualification has occurred. See docs/release-checklist.md. Source: https://github.com/mvalancy/pcb-agx-thor-can-breakout\n'
  z.writestr('README.md',readme);hashes.append(hashlib.sha256(readme.encode()).hexdigest()+'  README.md')
  z.writestr('SHA256SUMS','\n'.join(hashes)+'\n')
 checksums.append(hashlib.sha256(out.read_bytes()).hexdigest()+'  '+out.name);print(out.relative_to(R),round(out.stat().st_size/1e6,2),'MB')
(R/'releases/SHA256SUMS').write_text('\n'.join(checksums)+'\n')
(R/'releases/release-prerelease').write_text('true\n')
(R/'releases/release-notes.md').write_text('''# A0 engineering pre-release

Download the PCB ZIP for the selected variant and the housings ZIP. SHA256SUMS identifies every download; each ZIP also includes member hashes.

Contains native KiCad schematics/routed boards, Gerber/drill review files, schematic PDFs, PCB/assembly views, exact-source assembly populations and check reports. Housing files include STL/STEP/3MF, two fit coupons, a replaceable ribbon clamp, heat-set insert and silicone-pad instructions.

The design has undergone multiple electrical and mechanical iterations. Native reports, semantic connector checks, source freshness, assembly-path/collision screens and mesh/3MF checks are recorded. CI verifies committed evidence; it does not fabricate or test hardware.

Open: Wieson procurement/current mechanical drawing and cable fit, exact IGX carrier compatibility, printed fit/pull/creep tests, intended CAN bitrates and transient qualification, JLC DFM/stock/panelization/placement approval. No production order has been placed. This release is not suitable for an unreviewed 50-unit order.
''')
