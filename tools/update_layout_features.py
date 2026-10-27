#!/usr/bin/env python3
"""Add fabrication-safe prototype pads and legends without moving paired CAN routes.

Run with KiCad Python after --schematic-only and netlist export. Existing copper
is locked before exporting auxiliary routing. Both variants are separate native
processes to avoid KiCad SWIG ownership problems.
"""
import json, math, sys, subprocess, uuid
from pathlib import Path
import pcbnew as p
R=Path(__file__).resolve().parents[1]
if len(sys.argv)==1:
 for variant in ['2port','4port']:subprocess.run([sys.executable,__file__,variant],check=True)
 raise SystemExit
v=sys.argv[1];n=int(v[0]);P=json.loads((R/'cad/parameters.json').read_text());spec=P['prototype']
w=P['pcb'][f'width_{v}_mm'];d=P['pcb']['depth_mm'];cx=w/2-10
path=R/f'hardware/{v}/thor-{v}.kicad_pcb';b=p.LoadBoard(str(path));mm=p.FromMM
vec=lambda x,y:p.VECTOR2I(mm(x),mm(y))
parts=json.loads((R/f'exports/{v}/components.json').read_text());fps={f.GetReference():f for f in b.GetFootprints()}
schid=str(uuid.uuid5(uuid.NAMESPACE_URL,'thor-breakout/'+v+'/schematic'))
for part in parts:
 ref=part['ref']
 if part['kind'] not in {'rail','proto1','proto2'}:continue
 if ref in fps:b.Delete(fps[ref])
 name=part['footprint'].split(':')[1];f=p.FootprintLoad(str(R/'hardware/Thor.pretty'),name)
 f.SetFPID(p.LIB_ID('Thor',name));f.SetReference(ref);f.SetValue(part['value']);f.SetPosition(vec(part['x'],part['y']));f.SetPath(p.KIID_PATH('/'+schid+'/'+part['uuid']))
 f.Reference().SetVisible(False);f.Value().SetVisible(False)
 f.SetAttributes(f.GetAttributes()|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES)
 if part['kind'].startswith('proto'):f.SetAttributes(f.GetAttributes()|p.FP_BOARD_ONLY)
 b.Add(f)
for ref,x in [('H3',4),('H4',w-4)]:fps[ref].SetPosition(vec(x,d-4))
for obj in list(b.GetDrawings()):
 if obj.GetLayer()==p.Edge_Cuts or isinstance(obj,p.PCB_TEXT):b.Delete(obj)
for a,c in [((0,0),(w,0)),((w,0),(w,d)),((w,d),(0,d)),((0,d),(0,0))]:
 line=p.PCB_SHAPE();line.SetShape(p.SHAPE_T_SEGMENT);line.SetStart(vec(*a));line.SetEnd(vec(*c));line.SetLayer(p.Edge_Cuts);line.SetWidth(mm(.05));b.Add(line)
for zone in list(b.Zones()):
 if not zone.GetIsRuleArea():b.Delete(zone)
 # Idempotent update of the prototype keepouts.
 elif zone.GetZoneName().startswith('Prototype '):b.Delete(zone)
for part in parts:
 if not part['kind'].startswith('proto'):continue
 f=next(f for f in b.GetFootprints() if f.GetReference()==part['ref']);xs=[p.ToMM(x.GetPosition().x) for x in f.Pads()];ys=[p.ToMM(x.GetPosition().y) for x in f.Pads()]
 for layer in [p.F_Cu,p.B_Cu]:
  zone=p.ZONE(b);zone.SetLayer(layer);zone.SetIsRuleArea(True);zone.SetZoneName('Prototype '+part['ref'])
  zone.SetDoNotAllowTracks(True);zone.SetDoNotAllowVias(True);zone.SetDoNotAllowZoneFills(True);zone.SetDoNotAllowPads(False);zone.SetDoNotAllowFootprints(False)
  poly=zone.Outline();poly.NewOutline()
  for x,y in [(min(xs)-1.2,min(ys)-1.2),(max(xs)+1.2,min(ys)-1.2),(max(xs)+1.2,max(ys)+1.2),(min(xs)-1.2,max(ys)+1.2)]:poly.Append(mm(x),mm(y))
  b.Add(zone)
def label(text,x,y,size=1,layer=p.F_SilkS,justify=None):
 t=p.PCB_TEXT(b);t.SetText(text);t.SetPosition(vec(x,y));t.SetTextSize(vec(size,size));t.SetTextThickness(mm(.15));t.SetLayer(layer)
 if layer==p.B_SilkS:t.SetMirrored(True)
 if justify is not None:t.SetHorizJustify(justify)
 b.Add(t)
label('PIN 9 NC / CAN ONLY',w/2,33)
for k in range(n):
 x=25.5+42*k;name=f'CAN{k}' if k<2 else f'RES{k}'
 label(name+' TERM',x,25);label(f'JP{k+1} = 120R',x,27.4);label('DEFAULT OPEN',x,29.8)
 label(name,x,16.3)
for ref,voltage in [('JP5','3V3'),('JP6','5V')]:
 f=fps[ref];x=p.ToMM(f.GetPosition().x);label(voltage,x,47.8);f.Reference().SetPosition(vec(x,56.6))
label('AUX: SHUNT = ON',w/2+10,59)
label('J10 RAW I/O',w-15,35)
for row,(left,right) in enumerate([('3V3','5V'),('FSI6','GND'),('STOP1','STOP2'),('OUT1','PWM'),('PGOOD','WAKE'),('SCL','SDA'),('GND','GND')]):
 y=39+row*2.54;label(left,w-19.7,y,justify=p.GR_TEXT_H_ALIGN_RIGHT);label(right,w-9.7,y,justify=p.GR_TEXT_H_ALIGN_LEFT)
label('SHIELD',w-10,23);label('OPEN',w-10,31)
fps['J12'].Reference().SetPosition(vec(w-10,20.6))
if n==2:label('J11 RESERVED',13,49)
for part in parts:
 if part['kind']=='rail':
  for row,name in enumerate(['GND','3V3','5V']):
   for layer in [p.F_SilkS,p.B_SilkS]:label(name,part['x']+8.8,part['y']+row*2.54,layer=layer)
 elif part['kind'].startswith('proto'):
  f=next(f for f in b.GetFootprints() if f.GetReference()==part['ref']);cols=len(list(f.Pads()))//spec['rows']
  for col in range(cols):label(str(col+1),part['x']+col*spec['pitch_mm'],69.8)
  for row in range(spec['rows']):label(chr(65+row),part['x']-2.1,part['y']+row*spec['pitch_mm'])
  for layer in [p.F_SilkS,p.B_SilkS]:label(f'{part["ref"]} / ISOLATED 2.54',part['x']+(cols-1)*spec['pitch_mm']/2,87.3,layer=layer)
for y,text in [(64,'RIBBON'),(66.5,'KEEP CLEAR'),(76,'THOR CAN'),(78.5,'A1 DEV')]:label(text,cx,y)
label('github.com/mvalancy',w/2,88,layer=p.B_SilkS)
label('FSI6: FSI FIRMWARE / NOT LINUX GPIO',w/2,59,layer=p.B_SilkS)
# Existing reviewed copper remains fixed when routing the new power taps.
for t in b.GetTracks():t.SetLocked(True)
p.SaveBoard(str(path),b)
print(v,'prototype pads, board outline and silk updated')
