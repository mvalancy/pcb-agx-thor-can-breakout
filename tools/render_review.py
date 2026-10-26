#!/usr/bin/env python3
"""Render exported STEP readbacks, verifying the geometry reviewers download."""
from pathlib import Path
import cadquery as cq
from cadagent.render import Renderer
R=Path(__file__).resolve().parents[1]
def load(v,name):
 path=R/'exports'/f'{v}_{name}.step'
 if not path.exists():path=R/'exports'/f'asm_{v}_{name}.step'
 return cq.importers.importStep(str(path)).val()
colors={'base':(.20,.34,.40),'lid':(.32,.50,.58),'clamp':(.90,.48,.16),'pcb':(.10,.42,.28),'header':(.16,.17,.19),'ribbon':(.75,.73,.67),'inserts':(.85,.64,.24),'screws':(.65,.67,.69),'female':(.65,.67,.69),'hoods':(.16,.18,.21),'thumbscrews':(.82,.55,.25),'can_cables':(.09,.1,.12),'legend_paint':(.94,.93,.82)}
for v in ['2port','4port']:
 r=Renderer(R/'preview',size=(1500,1050),background=(.065,.085,.105),subtitle=f'A0 DEVELOPMENT | {v.upper()} | EXPORTED STEP READBACK',branding='THOR CAN',accent='#11cbb1')
 for mode in ['exploded','open','lid','assembled']:
  shapes=[]
  names=['lid','legend_paint'] if mode=='lid' else list(colors)
  for name in names:
   if mode=='open' and name in ['lid','legend_paint','screws']:continue
   shape=load(v,name)
   if mode=='exploded' and name in ['lid','legend_paint']:shape=shape.translate((0,0,32))
   if mode=='exploded' and name=='clamp':shape=shape.translate((0,0,14))
   if mode=='exploded' and name=='screws':continue
   if name=='pcb':
    solids=shape.Solids();shapes.extend((s,(.62,.65,.67)) for s in solids[:-1]);shapes.append((solids[-1],colors['pcb']))
   else:shapes.append((shape,colors[name]))
  r.render(f'{v}-{mode}.png',shapes=shapes,view='top' if mode=='lid' else 'iso',caption=f'{v} / '+mode+' / STEP readback',note='Recessed legends with optional paint fill · mating seating assumptions and physical tests remain open')
