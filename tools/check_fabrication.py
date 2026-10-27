#!/usr/bin/env python3
"""Measure native fabrication features and prove the custom rule parser is active.
Run with KiCad Python. This is a local profile check, NOT a JLCDFM report.
"""
import json,sys,subprocess,tempfile,shutil,hashlib
from pathlib import Path
import pcbnew as p
R=Path(__file__).resolve().parents[1];profile=json.loads((R/'hardware/jlcpcb-profile.json').read_text());mm=p.ToMM
if len(sys.argv)==1:
 for v in ['2port','4port']:subprocess.run([sys.executable,__file__,v],check=True)
 raise SystemExit
v=sys.argv[1];base=R/f'hardware/{v}/thor-{v}';b=p.LoadBoard(str(base.with_suffix('.kicad_pcb')));pads=[pad for f in b.GetFootprints() for pad in f.Pads()];pth=[pad for pad in pads if pad.GetAttribute()==p.PAD_ATTRIB_PTH];vias=[t for t in b.GetTracks() if isinstance(t,p.PCB_VIA)];silk=[t for f in b.GetFootprints() for t in [f.Reference(),f.Value()] if t.IsVisible() and t.GetLayer()==p.F_SilkS]+[t for t in b.GetDrawings() if isinstance(t,p.PCB_TEXT) and t.GetLayer()==p.F_SilkS]
metrics={'pth_annular_min_mm':min((min(mm(q.GetSize().x),mm(q.GetSize().y))-max(mm(q.GetDrillSize().x),mm(q.GetDrillSize().y)))/2 for q in pth),'via_annular_min_mm':min((mm(q.GetWidth(p.F_Cu))-mm(q.GetDrill()))/2 for q in vias),'via_drill_min_mm':min(mm(q.GetDrill()) for q in vias),'silk_height_min_mm':min(mm(t.GetTextHeight()) for t in silk),'silk_stroke_min_mm':min(mm(t.GetTextThickness()) for t in silk),'track_width_min_mm':min(mm(t.GetWidth()) for t in b.GetTracks() if not isinstance(t,p.PCB_VIA))}
errors=[];limits=profile['project_limits_mm']
for metric,limit in [('pth_annular_min_mm','pth_annular'),('via_annular_min_mm','via_annular'),('via_drill_min_mm','via_drill'),('silk_height_min_mm','silk_height'),('silk_stroke_min_mm','silk_stroke'),('track_width_min_mm','track_width')]:
 if metrics[metric]<limits[limit]-1e-6:errors.append(f'{metric} below profile')
# A native negative control prevents a rule-parse failure from masquerading as a
# clean zero-findings CLI exit. The temporary PCB never replaces design source.
with tempfile.TemporaryDirectory(prefix='thor-drc-probe-') as tmp:
 tmp=Path(tmp);fixture=tmp/base.name
 for ext in ['.kicad_pcb','.kicad_pro','.kicad_dru']:shutil.copy2(base.with_suffix(ext),fixture.with_suffix(ext))
 with fixture.with_suffix('.kicad_dru').open('a') as f:f.write('\n(rule "DFM enforcement probe" (constraint track_width (min 0.8mm)))\n')
 run=subprocess.run(['kicad-cli','pcb','drc','--format','json','-o',str(tmp/'probe.json'),str(fixture.with_suffix('.kicad_pcb'))],capture_output=True,text=True)
 data=json.loads((tmp/'probe.json').read_text()) if (tmp/'probe.json').exists() else {}
 detections=[e for e in data.get('violations',[]) if e['type']=='track_width' and '0.8000' in e['description']]
 probe={'pass':bool(detections),'intentional_requirement_mm':.8,'expected_violation':'track_width with intentional 0.8000 mm minimum','detected_count':len(detections)}
 if not probe['pass']:errors.append('Native custom-rule negative control did not detect the intentional violation')
sources=['hardware/jlcpcb-profile.json','tools/apply_fab_rules.py','tools/check_fabrication.py']+[f'hardware/{v}/thor-{v}.{ext}' for ext in ['kicad_pcb','kicad_pro','kicad_dru']]
result={'pass':not errors,'errors':errors,'metrics':{k:round(value,5) for k,value in metrics.items()},'native_rules_negative_control':probe,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources},'vendor_dfm':profile['vendor_dfm'],'scope':'Local native feature measurements and custom-rule enforcement. Full board DRC is separately required. No vendor DFM approval, panelization, placement-library orientation or PCBA process qualification.'}
(R/f'exports/{v}/fabrication-profile-check.json').write_text(json.dumps(result,indent=2)+'\n');print(v,'fabrication profile',result['pass'],metrics,'probe',probe['pass'])
if errors:raise SystemExit(1)
