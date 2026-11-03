#!/usr/bin/env python3
"""Apply the source-dated JLC capability profile to each native KiCad project."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
profile=json.loads((R/'hardware/jlcpcb-profile.json').read_text());r=profile['project_limits_mm']
rules='''(version 1)
# Project transcription of JLCPCB capabilities retrieved 2026-10-26.
# Not a vendor DFM approval. See ../jlcpcb-profile.json.
(rule "JLC conservative copper"
 (constraint clearance (min 0.20mm))
 (constraint track_width (min 0.20mm))
 (constraint hole_size (min 0.30mm))
 (constraint hole_to_hole (min 0.45mm))
 (constraint hole_clearance (min 0.28mm))
 (constraint edge_clearance (min 0.30mm)))
(rule "JLC through-hole annular ring"
 (condition "A.Type == 'Pad' && A.Pad_Type == 'Through-hole'")
 (constraint annular_width (min 0.25mm)))
(rule "JLC via annular ring"
 (condition "A.Type == 'Via'")
 (constraint annular_width (min 0.15mm)))
(rule "JLC legible silkscreen"
 (layer outer)
 (constraint text_height (min 1mm))
 (constraint text_thickness (min 0.15mm)))
'''
def block_span(text):
 """Start and end (with its line) of the first (title_block ...) s-expression, matched by parentheses."""
 i=text.index('(title_block');depth=0
 for j in range(i,len(text)):
  depth+={'(':1,')':-1}.get(text[j],0)
  if depth==0:break
 e=text.find('\n',j);return text.rfind('\n',0,i)+1,(e+1 if e>=0 else len(text))
for v in ['2port','4port']:
 base=R/f'hardware/{v}/thor-{v}';p=base.with_suffix('.kicad_pro');d=json.loads(p.read_text());s=d['board']['design_settings'];s['rules'].update(min_clearance=r['clearance'],min_track_width=r['track_width'],min_via_annular_width=r['via_annular'],min_via_diameter=r['via_diameter'],min_through_hole_diameter=r['via_drill'],min_hole_clearance=r['hole_to_copper'],min_hole_to_hole=r['hole_to_hole'],min_copper_edge_clearance=r['copper_to_edge'],min_silk_clearance=r['silk_to_pad'],min_text_height=r['silk_height'],min_text_thickness=r['silk_stroke'])
 s['solder_mask_min_width']=r['soldermask_bridge'];s['solder_mask_clearance']=0.0
 # KiCad defaults disable these checks. Enable them explicitly: no blanket waivers.
 for key in ['missing_courtyard','track_not_centered_on_via','tuning_profile_track_geometries','footprint_filters_mismatch','footprint_type_mismatch']:
  s['rule_severities'][key]='warning'
 erc=d.setdefault('erc',{}).setdefault('rule_severities',{})
 for key in ['single_global_label','four_way_junction','simulation_model_issue','footprint_filter']:erc[key]='warning'
 p.write_text(json.dumps(d,indent=2)+'\n');base.with_suffix('.kicad_dru').write_text(rules)
 # Gerber X2 and job files take the revision from the board's title block: mirror the schematic's.
 pcb=base.with_suffix('.kicad_pcb');board=pcb.read_text();flat=lambda s:re.sub(r'\s+','',s)
 sch=base.with_suffix('.kicad_sch').read_text();a,b=block_span(sch);block=re.sub(r'\s+',' ',sch[a:b].strip())
 if '(title_block' not in board or flat(board[slice(*block_span(board))])!=flat(block):   # else keep KiCad's layout
  board=board[:block_span(board)[0]]+board[block_span(board)[1]:] if '(title_block' in board else board
  pcb.write_text(board.replace('\t(paper "A4")\n','\t(paper "A4")\n\t'+block+'\n',1))
 print(v,'JLC-derived fabrication rules applied')
