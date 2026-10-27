#!/usr/bin/env python3
"""Independent native check of free pads, gated power rails and ribbon clearance."""
import json, hashlib, sys, subprocess, math
from pathlib import Path
import pcbnew as p
R=Path(__file__).resolve().parents[1]
if len(sys.argv)==1:
 for v in ['2port','4port']:subprocess.run([sys.executable,__file__,v],check=True)
 raise SystemExit
v=sys.argv[1];P=json.loads((R/'cad/parameters.json').read_text());s=P['prototype'];w=P['pcb'][f'width_{v}_mm'];cx=w/2-10
board=p.LoadBoard(str(R/f'hardware/{v}/thor-{v}.kicad_pcb'));fps={f.GetReference():f for f in board.GetFootprints()};errors=[];grids=[]
for ref in ['P1','P2']:
 f=fps[ref];pads=list(f.Pads());xs=sorted({round(p.ToMM(q.GetPosition().x),5) for q in pads});ys=sorted({round(p.ToMM(q.GetPosition().y),5) for q in pads})
 if any(q.GetNetCode()!=0 or q.GetNetname() for q in pads):errors.append(ref+' isolated pad has an assigned net')
 if len(pads)!=len(xs)*6 or len(ys)!=6:errors.append(ref+' incomplete rectangular 6-row grid')
 if any(abs(b-a-2.54)>1e-5 for coords in [xs,ys] for a,b in zip(coords,coords[1:])):errors.append(ref+' pitch is not 2.54 mm')
 if any(abs(p.ToMM(q.GetDrillSize().x)-1)>1e-5 or abs(p.ToMM(q.GetSize().x)-1.8)>1e-5 for q in pads):errors.append(ref+' drill/pad dimension mismatch')
 if any(abs(x-cx)<12 for x in xs):errors.append(ref+' intrudes on ribbon/component exclusion lane')
 if not f.GetAttributes()&p.FP_EXCLUDE_FROM_BOM or not f.GetAttributes()&p.FP_EXCLUDE_FROM_POS_FILES or not f.GetAttributes()&p.FP_BOARD_ONLY:errors.append(ref+' bare pads must be board-only and excluded from assembly')
 # Rule areas must suppress automatic copper, tracks and vias across each grid.
 for layer in [p.F_Cu,p.B_Cu]:
  matching=[z for z in board.Zones() if z.GetZoneName()=='Prototype '+ref and z.GetLayer()==layer]
  if len(matching)!=1 or not all([matching[0].GetDoNotAllowTracks(),matching[0].GetDoNotAllowVias(),matching[0].GetDoNotAllowZoneFills()]):errors.append(ref+' lacks full prototype copper exclusion on '+str(layer))
 grids.append({'reference':ref,'columns':len(xs),'rows':len(ys),'isolated_pads':len(pads),'pitch_mm':2.54,'x_range_mm':[xs[0],xs[-1]],'y_range_mm':[ys[0],ys[-1]]})
for ref in ['TP1','TP2']:
 pads=list(fps[ref].Pads())
 for number,net in [('1','/GND'),('2','/AUX_3V3'),('3','/AUX_5V_AO')]:
  row=[q for q in pads if q.GetNumber()==number]
  if len(row)!=3 or any(q.GetNetname()!=net for q in row):errors.append(ref+' rail '+number+' has wrong mapping')
 if not fps[ref].GetAttributes()&p.FP_EXCLUDE_FROM_BOM:errors.append(ref+' bare power pads entered assembly BOM')
 if len(pads)!=9:errors.append(ref+' should have exactly nine rail holes')
report={'pass':not errors,'errors':errors,'isolated_pads':sum(g['isolated_pads'] for g in grids),'grids':grids,'power_taps':'Two banks, each 3 GND + 3 AUX_3V3 + 3 AUX_5V_AO holes. JP5/JP6 remain open by default.','signal_access':'All 26 J47 pins retained by J10, DE9, termination links, power links and J11 on 2port. See electrical-review.json.','assembly_default':'All prototype and rail holes bare; no automatic assembly or net connections on free pads.','source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in [f'hardware/{v}/thor-{v}.kicad_pcb','cad/parameters.json','tools/check_prototype.py','tools/update_layout_features.py']}}
(R/f'exports/{v}/prototype-review.json').write_text(json.dumps(report,indent=2)+'\n');print(v,report['pass'],report['isolated_pads'],errors)
if errors:raise SystemExit(1)
