#!/usr/bin/env python3
"""Render exported STEP readbacks, verifying the geometry reviewers download."""
from pathlib import Path
import json
import cadquery as cq
from cadagent.render import Renderer
R=Path(__file__).resolve().parents[1]
P=json.loads((R/'cad/parameters.json').read_text())
def load(v,name):
 path=R/'exports'/f'{v}_{name}.step'
 if not path.exists():path=R/'exports'/f'asm_{v}_{name}.step'
 return cq.importers.importStep(str(path)).val()
colors={'base':(.20,.34,.40),'lid':(.32,.50,.58),'clamp':(.90,.48,.16),'pcb':(.10,.42,.28),'header':(.16,.17,.19),'ribbon':(.75,.73,.67),'inserts':(.85,.64,.24),'screws':(.65,.67,.69),'female':(.65,.67,.69),'hoods':(.16,.18,.21),'thumbscrews':(.82,.55,.25),'can_cables':(.09,.1,.12),'legend_paint':(.94,.93,.82)}
for v in ['2port','4port']:
 r=Renderer(R/'preview',size=(1500,1050),background=(.065,.085,.105),subtitle=f'A1 DEVELOPMENT | {v.upper()} | EXPORTED STEP READBACK',branding='THOR CAN',accent='#11cbb1')
 for mode in ['exploded','open','lid','assembled','rear-supports','mounting']:
  if r.only and f'{v}-{mode}.png' not in r.only:continue
  shapes=[]
  names=['base'] if mode in ['rear-supports','mounting'] else ['lid','legend_paint'] if mode=='lid' else list(colors)
  for name in names:
   if mode=='open' and name in ['lid','legend_paint','screws']:continue
   shape=load(v,name)
   if mode=='rear-supports':
    cx=P['pcb'][f'width_{v}_mm']/2+10;cy=P['strain_relief']['clamp_y_mm'];rear=P['pcb']['depth_mm']+P['case']['rear_extension_mm']
    # Readback section below the clamp deck exposes the real rib/root geometry.
    shape=shape.intersect(cq.Solid.makeBox(46,rear+6-(cy-7),10,cq.Vector(cx-23,cy-7,0)))
   if mode=='exploded':
    clamp_dx=P['pcb'][f'width_{v}_mm']/2+P['case']['wall_mm']+P['case']['board_clearance_mm']+14
    if name=='screws':
     screws=shape.Solids();assert len(screws)==6, 'Exploded hardware must show all six enclosure screws'
     shape=cq.Compound.makeCompound([s.translate((0,0,92)) if s.BoundingBox().zlen>15 else s.translate((clamp_dx,0,53)) for s in screws])
    elif name=='clamp':shape=shape.translate((clamp_dx,0,36))
    elif name=='inserts':
     shape=cq.Compound.makeCompound([s.translate((clamp_dx,0,20)) if s.BoundingBox().zmax>10 else s.translate((0,0,18)) for s in shape.Solids()])
    else:shape=shape.translate((0,0,{'base':0,'lid':58,'legend_paint':58}.get(name,40)))
   if name=='pcb':
    solids=shape.Solids();shapes.extend((s,(.62,.65,.67)) for s in solids[:-1]);shapes.append((solids[-1],colors['pcb']))
   else:shapes.append((shape,colors[name]))
  r.render(f'{v}-{mode}.png',shapes=shapes,view=(.25,-.18,1) if mode=='mounting' else 'top' if mode=='lid' else 'iso',caption=f'{v} / '+mode+' / STEP readback',note=('4 × M3 corner mounts · 26 mm wide · R4 roots · unchanged 7 mm thickness · physical load rating unverified' if mode=='mounting' else 'Section at Z10 below the clamp deck · 3.2 mm ribs with R1.6 wall roots · no load rating' if mode=='rear-supports' else '4 × M3×20 lid screws · 2 × M3×6 clamp screws · 6 × M3 heat-set inserts' if mode=='exploded' else 'Recessed legends with optional paint fill · mating seating assumptions and physical tests remain open'))
 for part in ['base','lid']:
  if r.only and f'{v}_{part}.png' not in r.only:continue
  shapes=[(load(v,part),colors[part])]
  if part=='lid':shapes.append((load(v,'legend_paint'),colors['legend_paint']))
  r.render(f'{v}_{part}.png',shapes=shapes,view='iso',caption=f'{v} / printable {part} / STEP readback',note='STEP assembly orientation shown · STL and 3MF are already oriented for printing')
r=Renderer(R/'preview',size=(1000,750),background=(.065,.085,.105),subtitle='A1 DEVELOPMENT | PRINTED PARTS',branding='THOR CAN',accent='#11cbb1')
for name in ['ribbon_clamp','fastener_coupon','port_coupon']:
 if r.only and name+'.png' not in r.only:continue
 shape=cq.importers.importStep(str(R/f'exports/{name}.step')).val()
 r.render(name+'.png',shapes=[(shape,(.90,.48,.16))],view='iso',caption=name.replace('_',' ')+' / STEP readback',note='Print coupons and verify received hardware before assembling electronics')
