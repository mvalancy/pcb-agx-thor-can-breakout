#!/usr/bin/env python3
from pathlib import Path
import json
from cadagent.pcb import evidence_bundle,check_jlc_files
R=Path(__file__).resolve().parents[1]
for v in ['2port','4port']:
 out=R/'exports'/v
 gates=[{'id':i,'pass':False,'detail':d} for i,d in [('mating','Native Wieson lands verified; current drawing/height, procurement and physical FFSD fit/continuity pending'),('sourcing','Exact manufacturer connector footprint and assembly quote'),('protection','CAN waveform, ESD/EFT/surge and sustained fault scope'),('mechanical','Printed housing, clamp pull test and cable routing'),('assembly','JLC DFM, placement rotation and first article inspection')]]
 if v=='4port':gates.append({'id':'igx','pass':False,'detail':'Specific IGX carrier revision pinout and population audit'})
 manifest={'reports':{'erc':f'exports/{v}/erc.json','drc':f'exports/{v}/drc.json'},'sources':[f'hardware/{v}/thor-{v}.{ext}' for ext in ['kicad_sch','kicad_pcb','kicad_pro','kicad_dru']]+['hardware/interface.json','research/j47-footprint-measurements.json'],'release_gates':gates}
 (R/'hardware'/v/'evidence-manifest.json').write_text(json.dumps(manifest,indent=2))
 (out/'pcb-evidence.json').write_text(json.dumps(evidence_bundle(R,manifest['reports'],manifest['sources'],manifest['release_gates']),indent=2))
 (out/'assembly-file-checks.json').write_text(json.dumps(check_jlc_files(out/'jlc-bom.csv',out/'jlc-cpl.csv'),indent=2))
print('Electrical report/source hashes and assembly files checked.')
