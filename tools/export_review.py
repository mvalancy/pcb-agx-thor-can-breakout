#!/usr/bin/env python3
"""Export native KiCad checks, drawings and explicitly unreleased fabrication data."""
from pathlib import Path
import subprocess,json,csv,zipfile,hashlib
ROOT=Path(__file__).resolve().parents[1]
def run(*args):
 p=subprocess.run(['kicad-cli',*map(str,args)],cwd=ROOT,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr+p.stdout)
 return p.stdout
for v in ('2port','4port'):
 base=Path('hardware')/v/f'thor-{v}';out=Path('exports')/v
 sch=base.with_suffix('.kicad_sch');pcb=base.with_suffix('.kicad_pcb')
 run('sch','erc','--format','json','-o',out/'erc.json',sch)
 run('pcb','drc','--format','json','--schematic-parity','-o',out/'drc.json',pcb)
 run('sch','export','pdf','-o',out/'schematic.pdf',sch)
 run('sch','export','netlist','--format','kicadxml','-o',out/'netlist.xml',sch)
 # Strip machine-local prefixes from distributable XML metadata only.
 f=ROOT/out/'netlist.xml';f.write_text(f.read_text().replace(str(ROOT)+'/', ''))
 run('pcb','export','svg','--mode-single','--layers','F.Cu,F.Silkscreen,Edge.Cuts','--fit-page-to-board','--exclude-drawing-sheet','-o',out/'pcb-top.svg',pcb)
 run('pcb','export','svg','--mode-single','--layers','B.Cu,Edge.Cuts','--fit-page-to-board','--exclude-drawing-sheet','-o',out/'pcb-bottom.svg',pcb)
 run('pcb','export','svg','--mode-single','--layers','F.Fab,F.Silkscreen,Edge.Cuts','--sketch-pads-on-fab-layers','--fit-page-to-board','--exclude-drawing-sheet','-o',out/'assembly.svg',pcb)
 run('pcb','export','pos','--format','csv','--units','mm','-o',out/'positions-kicad.csv',pcb)
 run('pcb','export','step','--force','--subst-models','-o',out/'pcb.step',pcb)
 fab=out/'fabrication-review';(ROOT/fab).mkdir(exist_ok=True)
 run('pcb','export','gerbers','--layers','F.Cu,B.Cu,F.Paste,F.Silkscreen,F.Mask,B.Mask,Edge.Cuts','-o',str(fab)+'/',pcb)
 run('pcb','export','drill','--format','excellon','--excellon-separate-th','--generate-map','--map-format','pdf','-o',str(fab)+'/',pcb)
 (ROOT/fab/'README.txt').write_text('A0 DEVELOPMENT / DO NOT ORDER\nPrototype connector mating, exact DE9 sourcing, assembly placement review and hardware qualification are incomplete.\n2 layers, 1.6 mm FR4, 1 oz copper; supplier DFM and stackup approval required.\nSee docs/release-checklist.md and docs/manufacturing.md.\n')
 with zipfile.ZipFile(ROOT/out/f'thor-{v}-A0-fabrication-REVIEW.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in sorted((ROOT/fab).iterdir()):z.write(f,f.name)
 # Assemble only the exact-source TVS at this stage. Header is manual/consigned.
 parts=json.loads((ROOT/out/'components.json').read_text());smt=[p for p in parts if p['kind']=='tvs']
 with (ROOT/out/'jlc-bom.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['Comment','Designator','Footprint','LCSC Part #'])
  for p in smt:w.writerow([p['mpn'],p['ref'],p['footprint'].split(':')[1],p['lcsc']])
 positions={r['Ref']:r for r in csv.DictReader((ROOT/out/'positions-kicad.csv').open())}
 with (ROOT/out/'jlc-cpl.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
  for p in smt:
   r=positions[p['ref']];w.writerow([r['Ref'],r['PosX'],r['PosY'],'top',r['Rot']])
 with (ROOT/out/'manual-assembly.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['Designator','Description','MPN','Disposition'])
  for p in parts:
   if p['kind']!='mount' and p['kind']!='tvs':w.writerow([p['ref'],p['value'],p['mpn'],'Manual/consigned; sourcing and fit approval pending'])
 with (ROOT/out/'bom-review.csv').open('w') as f:
  writer=csv.writer(f);writer.writerow(['Designator','Comment','Footprint','Manufacturer Part','LCSC Part #','Assembly','Status'])
  for p in parts:
   if p['kind']=='mount':continue
   writer.writerow([p['ref'],p['value'],p['footprint'],p['mpn'],p['lcsc'],'SMT' if p['kind'] in ('header','tvs') else 'THT','Header consignment/mating pending' if not p['lcsc'] else 'Exact SKU; assembly/stock approval pending'])
 with (ROOT/out/'jlc-full-bom.csv').open('w') as f, (ROOT/out/'jlc-full-cpl.csv').open('w') as g:
  bw=csv.writer(f);cw=csv.writer(g);bw.writerow(['Comment','Designator','Footprint','LCSC Part #']);cw.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
  for p in parts:
   if not p['lcsc']:continue
   bw.writerow([p['mpn'],p['ref'],p['footprint'].split(':')[1],p['lcsc']]);r=positions[p['ref']];cw.writerow([r['Ref'],r['PosX'],r['PosY'],'top',r['Rot']])
 print(v,'exported',flush=True)
