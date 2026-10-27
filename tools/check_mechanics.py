#!/usr/bin/env python3
"""Independent assembly-path and fit-sensitivity screens; no physical load claims."""
from pathlib import Path
import sys,json,hashlib,argparse
import cadquery as cq
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad'))
import build as m
parser=argparse.ArgumentParser();parser.add_argument('variant',nargs='?',choices=['2port','4port']);args=parser.parse_args()
for n in ([int(args.variant[0])] if args.variant else [2,4]):
 # Read the exact exported assembly instead of rebuilding expensive engravings.
 def read(name):return cq.importers.importStep(str(R/f'exports/{name}.step')).val()
 base=read(f'{n}port_base');lid=read(f'{n}port_lid');bar=read(f'asm_{n}port_clamp');native=read(f'asm_{n}port_pcb')
 review=json.loads((R/f'exports/{n}port/mechanical-checks.json').read_text())
 if review['mechanical_sources']!=m.source_hashes() or review.get('mechanical_library_sha256')!=m.library_hashes():raise RuntimeError('Rebuild stale mechanical exports first')
 raw=cq.importers.importStep(str(R/f'exports/{n}port/pcb.step')).val().Center();actual=native.Center()
 expected=(m.B[f'width_{n}port_mm']-raw.x,-raw.y,raw.z+m.C['floor_mm']+m.C['standoff_height_mm'])
 frame_error=max(abs(a-e) for a,e in zip((actual.x,actual.y,actual.z),expected))
 trials=[{'test':'native PCB proper rotation / asymmetric center of mass','error_mm':round(frame_error,7),'overlap_mm3':0 if frame_error<1e-4 else 1}]
 # Top-down insertion of populated board into the open base, excluding intentional final support contact.
 for z in [0,1,3,6,10,20]:
  overlap=native.translate((0,0,z)).intersect(base).Volume()
  trials.append({'test':'board insertion','z_offset_mm':z,'overlap_mm3':round(overlap,6)})
 # Nominal source models shifted in XY by conservative assembly slack. This is not a full tolerance stack.
 for x,y in [(-.2,0),(.2,0),(0,-.2),(0,.2)]:
  overlap=native.translate((x,y,0)).intersect(base.fuse(lid)).Volume()
  trials.append({'test':'PCB XY slack','shift_mm':[x,y],'overlap_mm3':round(overlap,6)})
 cx=m.B[f'width_{n}port_mm']/2+10;cy=m.S['clamp_y_mm'];z=m.S['lower_face_z_mm']+m.S['gap_mm']+m.S['clamp_thickness_mm']
 # Tool envelope with lid removed; radius3mm reaches both clamp screw heads without hitting other parts.
 for dx in [-m.S['screw_pitch_mm']/2,m.S['screw_pitch_mm']/2]:
  tool=m.cyl(cx+dx,cy,z+.05,3,30)
  trials.append({'test':'clamp driver access','x_mm':cx+dx,'overlap_mm3':round(tool.intersect(base.fuse(bar).fuse(native)).Volume(),6)})
 # Side mount driver paths stay outside the assembled enclosure, even with lid fitted.
 for x,y in review['structural_features']['mount_tab_centers_mm']:
  tool=m.cyl(x,y,m.P['mounting_tabs']['thickness_mm']+.05,3,35)
  trials.append({'test':'mounting ear driver access with lid fitted','x_mm':x,'y_mm':y,'overlap_mm3':round(tool.intersect(base.fuse(lid).fuse(native)).Volume(),6)})
  seat=m.P['mounting_tabs']['thickness_mm']-m.P['mounting_tabs']['counterbore_depth_mm']
  fastener=m.socket_head_envelope(3,10,5.5,3).translate((x,y,seat))
  trials.append({'test':'mounting ear M3 head and shank clearance','x_mm':x,'y_mm':y,'overlap_mm3':round(fastener.intersect(base.fuse(lid).fuse(native)).Volume(),6)})
 # User circuits must stay within these documented XY regions, <=12 mm above
 # the PCB and <=3 mm below it. The ribbon lane is deliberately excluded.
 proto=json.loads((R/f'exports/{n}port/prototype-review.json').read_text())
 w=m.B[f'width_{n}port_mm'];boardz=m.C['floor_mm']+m.C['standoff_height_mm']
 ribbon=read(f'asm_{n}port_ribbon')
 for grid in proto['grids']:
  xlo,xhi=grid['x_range_mm'];ylo,yhi=grid['y_range_mm'];x=w-xhi-.5;y=ylo-.5
  component=m.box(x,y,boardz+m.B['thickness_mm'],xhi-xlo+1,yhi-ylo+1,m.P['prototype']['maximum_component_height_mm'])
  leads=m.box(x,y,boardz-m.P['prototype']['maximum_lead_below_board_mm'],xhi-xlo+1,yhi-ylo+1,m.P['prototype']['maximum_lead_below_board_mm'])
  trials.append({'test':'prototype '+grid['reference']+' component and lead clearance','overlap_mm3':round(component.fuse(leads).intersect(base.fuse(lid).fuse(bar).fuse(ribbon)).Volume(),6)})
 # Tongue seats vertically without hitting the populated board or lower housing.
 for dz in [0,.5,1,2,5,12]:
  overlap=lid.translate((0,0,dz)).intersect(base.fuse(native).fuse(bar)).Volume()
  trials.append({'test':'lid insertion','z_offset_mm':dz,'overlap_mm3':round(overlap,6)})
 stack=[]
 for thick in [.5,.6,.7]:
  for gap in [1.65,1.8,1.95]:
   compression=(1.6+thick-gap)/1.6
   stack.append({'ribbon_mm':thick,'hard_gap_mm':gap,'pad_compression_fraction':round(compression,4)})
 report={'pass':all(t['overlap_mm3']<1e-5 for t in trials),'trials':trials,'pad_stack_sensitivity':stack,'pcb_washer_compression_fraction_at_board_thickness_1p44_to_1p76':[.04,.36],'limits':'Nominal/generic connector solids; XY translations are a sensitivity screen, not complete tolerance qualification. Silicone compression curve and pull strength unmeasured. Heat-set pilot and print shrink require coupons. Hood capture and thumbscrew engagement are unverified.','physical_fit_verified':False,'mechanical_library_sha256':m.library_hashes(),'mechanical_sources':{**m.source_hashes(),'tools/check_mechanics.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'artifact_sha256':{str(path.relative_to(R)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [R/f'exports/{n}port_base.step',R/f'exports/{n}port_lid.step',R/f'exports/asm_{n}port_clamp.step',R/f'exports/asm_{n}port_pcb.step']}}
 (R/f'exports/{n}port/assembly-paths.json').write_text(json.dumps(report,indent=2));print(n,report['pass'],[t for t in trials if t['overlap_mm3']>=1e-5],flush=True)
 if not report['pass']:raise SystemExit(1)
