#!/usr/bin/env python3
"""Import a route session, synchronize canonical netlist names, and add return plane.
Run with KiCad Python after build_electronics + routing + netlist export.
"""
import pcbnew as p
import sys,subprocess,math,json,xml.etree.ElementTree as ET
from pathlib import Path
root=Path(__file__).resolve().parents[1]
mm=p.FromMM
vec=lambda x,y:p.VECTOR2I(mm(x),mm(y))
# KiCad10 legacy SWIG ownership after Remove can corrupt a second board load.
# Isolate each board mutation in a separate interpreter process.
if len(sys.argv)==1:
 for variant in ['2port','4port']:subprocess.run([sys.executable,__file__,variant],check=True)
 sys.exit(0)
params=json.loads((root/'cad/parameters.json').read_text())
for v,w in [(sys.argv[1],params['pcb'][f'width_{sys.argv[1]}_mm'])]:
 path=root/f'hardware/{v}/thor-{v}.kicad_pcb';b=p.LoadBoard(str(path))
 parts={x['ref']:x for x in json.loads((root/f'exports/{v}/components.json').read_text())}
 for f in b.GetFootprints():
  part=parts.get(f.GetReference())
  if part is None:continue
  name=part['footprint'].split(':')[1]
  if f.GetFPID().GetLibItemName()!=name:
   # These audited derivatives change pad drills/SH centers only; keep routed footprint identity.
   template=p.FootprintLoad(str(root/'hardware/Thor.pretty'),name)
   f.SetFPID(p.LIB_ID('Thor',name));f.SetLibDescription(template.GetLibDescription())
   pads={pad.GetNumber():pad for pad in template.Pads()}
   shell=sorted([pad for pad in f.Pads() if pad.GetNumber()=='SH'],key=lambda pad:pad.GetPosition().x)
   local_shell=sorted([pad for pad in template.Pads() if pad.GetNumber()=='SH'],key=lambda pad:pad.GetPosition().x,reverse=True)
   for pad in f.Pads():
    source=pads[pad.GetNumber()];pad.SetDrillSize(source.GetDrillSize())
   angle=math.radians(f.GetOrientationDegrees());origin=f.GetPosition()
   for pad,source in zip(shell,local_shell):
    x=p.ToMM(source.GetPosition().x);y=p.ToMM(source.GetPosition().y)
    pad.SetPosition(vec(p.ToMM(origin.x)+x*math.cos(angle)+y*math.sin(angle),p.ToMM(origin.y)-x*math.sin(angle)+y*math.cos(angle)))
 if not list(b.GetTracks()):
  assert p.ImportSpecctraSES(b,str(root/f'exports/{v}/routed.ses'))
 netlist=ET.parse(root/f'exports/{v}/netlist.xml').getroot()
 # Preserve routed net IDs while adopting schematic's root-sheet namespace.
 for net in list(b.GetNetsByName().values()):
  name=net.GetNetname()
  if name and not name.startswith(('/', 'unconnected-')):net.SetNetname('/'+name)
 nets={n.GetNetname():n for n in b.GetNetsByName().values()}
 nodes={}
 for n in netlist.findall('nets/net'):
  name=n.attrib['name']
  if name not in nets:
   net=p.NETINFO_ITEM(b,name);b.Add(net);nets[name]=net
  for node in n.findall('node'):nodes[(node.attrib['ref'],node.attrib['pin'])]=nets[name]
 fields={c.attrib['ref']:{f.attrib['name']:f.text or '' for f in c.findall('fields/field')} for c in netlist.findall('components/comp')}
 for f in b.GetFootprints():
  ref=f.GetReference()
  if ref.startswith('H'):f.SetAttributes(f.GetAttributes()|p.FP_BOARD_ONLY)
  for pad in f.Pads():
   if (ref,pad.GetNumber()) in nodes:pad.SetNet(nodes[ref,pad.GetNumber()])
  for key in ['MPN','LCSC']:
   if key in fields.get(ref,{}):
    f.SetField(key,fields[ref][key]);f.GetField(key).SetVisible(False)
  if ref.startswith('D'):f.Reference().SetPosition(vec(p.ToMM(f.GetPosition().x)+3.5,17.5))
  if ref in {'J2','J3','J4','J5'}:
   # Clip only off-board silk; retain full body/courtyard on fabrication layers.
   for graphic in f.GraphicalItems():
    if graphic.GetLayer()==p.F_SilkS and isinstance(graphic,p.PCB_SHAPE):
     for getter,setter in [(graphic.GetStart,graphic.SetStart),(graphic.GetEnd,graphic.SetEnd)]:
      point=getter()
      if p.ToMM(point.y)<.3:setter(vec(p.ToMM(point.x),.3))
  if ref=='J10':
   f.Reference().SetPosition(vec(w-14.7,57))
   for pad in f.Pads():
    if pad.GetNumber()=='14':pad.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL)
 for t in b.GetDrawings():
  if isinstance(t,p.PCB_TEXT):
   if t.GetText()=='TERM=SHUNT':t.SetPosition(vec(p.ToMM(t.GetPosition().x)+7,28.2));t.SetText('TERM')
   if t.GetText()=='AUX RAW':t.SetPosition(vec(w-15,35))
 if not list(b.Zones()):
  z=p.ZONE(b);z.SetLayer(p.B_Cu);z.SetNet(nets['/GND']);z.SetLocalClearance(mm(.25));z.SetThermalReliefGap(mm(.3));z.SetThermalReliefSpokeWidth(mm(.3));z.SetPadConnection(p.ZONE_CONNECTION_THERMAL)
  poly=z.Outline();poly.NewOutline()
  for x,y in [(.5,.5),(w-.5,.5),(w-.5,64.5),(.5,64.5)]:poly.Append(mm(x),mm(y))
  b.Add(z)
 # Short direct ground via at each TVS reduces return inductance; no thermal relief.
 for f in b.GetFootprints():
  if f.GetReference().startswith('D'):
   pad=next(x for x in f.Pads() if x.GetNumber()=='3');pad.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL)
   pos=pad.GetPosition()
   offset=-.9 if v=='2port' and f.GetReference()=='D1' else 1.2
   end=vec(p.ToMM(pos.x)+offset,p.ToMM(pos.y))
   if True:
    old=vec(p.ToMM(pos.x)+(1.2 if offset<0 else -.9),p.ToMM(pos.y))
    for track in list(b.GetTracks()):
     if track.GetNetname()=='/GND' and ((isinstance(track,p.PCB_VIA) and track.GetPosition()==old) or (not isinstance(track,p.PCB_VIA) and track.GetStart()==pos and track.GetEnd()==old)):b.Remove(track)
   if not any(isinstance(t,p.PCB_VIA) and t.GetPosition()==end for t in b.GetTracks()):
    t=p.PCB_TRACK(b);t.SetStart(pos);t.SetEnd(end);t.SetWidth(mm(.4));t.SetLayer(p.F_Cu);t.SetNet(nets['/GND']);b.Add(t)
    via=p.PCB_VIA(b);via.SetPosition(end);via.SetWidth(mm(.6));via.SetDrill(mm(.3));via.SetViaType(p.VIATYPE_THROUGH);via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNet(nets['/GND']);b.Add(via)
 # Three asymmetric optical fiducials, board-only and excluded from assembly population.
 import shutil,os
 lib=Path(os.environ.get('KICAD_FOOTPRINT_DIR',str(Path.home()/'.local/share/kicad-10.0.1/share/kicad/footprints')))
 name='Fiducial_1mm_Mask2mm';shutil.copy2(lib/'Fiducial.pretty'/f'{name}.kicad_mod',root/'hardware/Thor.pretty'/f'{name}.kicad_mod')
 refs={f.GetReference() for f in b.GetFootprints()}
 for i,(x,y) in enumerate([(10,58),(w-10,58),(w-8,7)],1):
  ref=f'FID{i}'
  if ref in refs:
   next(f for f in b.GetFootprints() if f.GetReference()==ref).SetPosition(vec(x,y))
   continue
  f=p.FootprintLoad(str(root/'hardware/Thor.pretty'),name);f.SetFPID(p.LIB_ID('Thor',name));f.SetReference(ref);f.SetPosition(vec(x,y));f.SetAttributes(f.GetAttributes()|p.FP_BOARD_ONLY|p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES);f.Reference().SetVisible(False);f.Value().SetVisible(False);b.Add(f)
 # The solid bottom ground zone carries return current; redundant router ground traces
 # can crowd connector shell holes after exact manufacturer pad updates.
 for t in list(b.GetTracks()):
  if not isinstance(t,p.PCB_VIA) and t.GetNetname()=='/GND' and t.GetLayer()==p.B_Cu:b.Remove(t)
 b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b)
 print(v,'finalized')
