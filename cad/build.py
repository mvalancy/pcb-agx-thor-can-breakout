#!/usr/bin/env python3
"""Printable Thor housings, recessed fasteners, keyed seams and mating references."""
import json, hashlib, importlib
from pathlib import Path
import cadquery as cq
from cadagent.geometry import export_print_stl
from cadagent.fasteners import socket_head_envelope, insert_envelope, blind_insert_stack, filleted_wall_rib
from hardware_models import mating_set
from markings import lid_markings
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'cad/parameters.json').read_text());C=P['case'];B=P['pcb'];S=P['strain_relief'];I=P['inserts'];M=P['mating'];OUT=ROOT/'exports'
def box(x,y,z,dx,dy,dz):return cq.Solid.makeBox(dx,dy,dz,cq.Vector(x,y,z))
def cyl(x,y,z,r,h):return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z))
def rounded(shape,r):return cq.Workplane(obj=shape).edges('|Z').fillet(r).val()
def source_hashes():return {f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['cad/build.py','cad/hardware_models.py','cad/markings.py','cad/parameters.json','research/mating-dsub-measurements.json']}
def library_hashes():return {name:hashlib.sha256(Path(importlib.import_module(name).__file__).read_bytes()).hexdigest() for name in ['cadagent.geometry','cadagent.fasteners','cadagent.markings']}
def counterbore(shape,x,y,top):
 return shape.cut(cyl(x,y,top-60,C['screw_clearance_mm']/2,61)).cut(cyl(x,y,top-C['counterbore_depth_mm'],C['counterbore_diameter_mm']/2,C['counterbore_depth_mm']+1))
def clamp_part():
 w=S['clamp_width_mm'];d=S['clamp_depth_mm'];h=S['clamp_thickness_mm']
 shape=rounded(box(-w/2,-d/2,0,w,d,h),1.2)
 for x in [-S['screw_pitch_mm']/2,S['screw_pitch_mm']/2]:shape=counterbore(shape,x,0,h)
 text=cq.Workplane('XY').text('RIBBON',2.4,.5,font='DejaVu Sans',combine=True).val().translate((0,0,h-.4))
 return shape.cut(text)
def ring(w,rear,outer,inner,z,h):
 return rounded(box(-outer,-outer,z,w+2*outer,rear+2*outer,h),1.2).cut(rounded(box(-inner,-inner,z-1,w+2*inner,rear+2*inner,h+2),.6))
def engrave(shape,text,size,x,y,z):
 letters=cq.Workplane('XY').text(text,size,.6,font='DejaVu Sans',combine=True).val().translate((x,y,z-.4))
 return shape.cut(letters)
def build_variant(n):
 w=B[f'width_{n}port_mm'];d=B['depth_mm'];rear=d+C['rear_extension_mm'];clear=C['board_clearance_mm'];wall=C['wall_mm'];floor=C['floor_mm'];boardz=floor+C['standoff_height_mm'];top=floor+C['inner_height_mm'];roof=top+C['lid_mm'];axis=boardz+B['thickness_mm']+C['db9_axis_above_pcb_mm'];seam=axis
 x0=-clear-wall;y0=x0;ow=w+2*(clear+wall);od=rear+2*(clear+wall);cx=w/2+10
 shell=rounded(box(x0,y0,0,ow,od,roof).cut(box(-clear,-clear,floor,w+2*clear,rear+2*clear,C['inner_height_mm'])),C['corner_radius_mm'])
 def openings(shape):
  for k in range(n):
   px=w-(B['first_port_x_mm']+k*B['port_pitch_mm']);ww=C['db9_window_width_mm'];hh=C['db9_window_height_mm']
   shape=shape.cut(box(px-ww/2,y0-1,axis-hh/2,ww,wall+2*clear+2,hh))
  return shape.cut(box(cx-C['ribbon_slot_width_mm']/2,rear-clear-.2,axis-C['ribbon_slot_height_mm']/2,C['ribbon_slot_width_mm'],wall+2*clear+1.2,C['ribbon_slot_height_mm']))
 shell=openings(shell)
 base=shell.intersect(box(x0-1,y0-1,-1,ow+2,od+2,seam+1));lid=shell.intersect(box(x0-1,y0-1,seam,ow+2,od+2,roof-seam+1))
 # Four broad corner mounts on the cable-free sides. The screw seats are outside the
 # wall so an installed lid never obstructs the driver or mounting hardware.
 tabs=P['mounting_tabs'];tab_centers=[];tab_root_widths=[]
 assert tabs['quantity']==4 and len(tabs['y_centers_mm'])==2
 for side in [-1,1]:
  wx=x0 if side<0 else w-x0;tx=wx+side*tabs['hole_offset_from_wall_mm']
  for ty in tabs['y_centers_mm']:
   rib=filleted_wall_rib(thickness=2*tabs['outer_radius_mm'],reach=tabs['hole_offset_from_wall_mm'],height=tabs['thickness_mm'],root_radius=tabs['root_radius_mm'],overlap=tabs['overlap_mm'])
   rib=rib.rotate((0,0,0),(0,0,1),-90 if side<0 else 90).translate((tx,ty,0))
   ear=rib.fuse(cyl(tx,ty,0,tabs['outer_radius_mm'],tabs['thickness_mm']))
   ear=ear.cut(cyl(tx,ty,-1,tabs['hole_diameter_mm']/2,tabs['thickness_mm']+2)).cut(cyl(tx,ty,tabs['thickness_mm']-tabs['counterbore_depth_mm'],tabs['counterbore_diameter_mm']/2,tabs['counterbore_depth_mm']+1))
   base=base.fuse(ear);tab_centers.append((tx,ty))
   # Measure actual plastic in a thin section just outside the wall, including
   # the roots after fusion/cutting. The case wall itself is outside this probe.
   root_half=tabs['outer_radius_mm']+tabs['root_radius_mm']
   probe=box(wx+side*.5-.1,ty-root_half,0,.2,2*root_half,tabs['thickness_mm'])
   tab_root_widths.append(round(base.intersect(probe).Volume()/(.2*tabs['thickness_mm']),4))
 # Continuous perimeter tongue is interrupted only by connector/cable openings.
 outer=clear+C['lip_width_mm'];h=C['lip_height_mm'];tol=C['lip_clearance_mm']
 base=base.fuse(openings(ring(w,rear,outer,clear,seam-.4,h+.4)))
 # Groove is cut after the lid sleeves are fused so it also clears their wall overlap.
 holes=[(4,4),(w-4,4),(4,d-4),(w-4,d-4)]
 inserts=[];screws=[]
 def insert_at(x,y,face):return insert_envelope(I['outer_diameter_mm'],3,I['length_mm']).translate((x,y,face-I['recess_mm']))
 for x,y in holes:
  base=base.fuse(cyl(x,y,floor-.1,C['boss_diameter_mm']/2,C['standoff_height_mm']+.1)).cut(cyl(x,y,boardz-I['pilot_depth_mm'],C['pilot_diameter_mm']/2,I['pilot_depth_mm']+.2))
  sleeve_z=boardz+B['thickness_mm']+C['pcb_retention_gap_mm']
  lid=lid.fuse(cyl(x,y,sleeve_z,4.3,seam+.2-sleeve_z)).fuse(cyl(x,y,seam,C['boss_diameter_mm']/2,roof-seam));lid=counterbore(lid,x,y,roof)
  inserts.append(insert_at(x,y,boardz));screws.append(socket_head_envelope(3,C['lid_screw_length_mm'],5.5,3).translate((x,y,roof-C['counterbore_depth_mm'])))
 lid=lid.cut(ring(w,rear,outer+tol,clear-tol,seam-.1,h+tol+.1))
 cy=S['clamp_y_mm'];low=S['lower_face_z_mm'];high=low+S['gap_mm'];cw=S['clamp_width_mm'];cd=S['clamp_depth_mm'];bar=clamp_part().translate((cx,cy,high))
 deck=box(cx-cw/2,cy-cd/2,low-2.8,cw,rear+clear-(cy-cd/2)+.1,2.8)
 for dx in [-S['screw_pitch_mm']/2,S['screw_pitch_mm']/2]:
  x=cx+dx
  deck=deck.fuse(cyl(x,cy,floor-.1,S['boss_diameter_mm']/2,high-floor+.1))
  rib=filleted_wall_rib(thickness=S['support_rib_mm'],reach=rear+clear-cy,height=low-floor+.1,root_radius=S['support_root_radius_mm'],overlap=S['support_overlap_mm']).translate((x,cy,floor-.1))
  deck=deck.fuse(rib)
  deck=deck.cut(cyl(x,cy,high-I['pilot_depth_mm'],C['pilot_diameter_mm']/2,I['pilot_depth_mm']+.2))
  inserts.append(insert_at(x,cy,high));screws.append(socket_head_envelope(3,S['screw_length_mm'],5.5,3).translate((x,cy,high+S['clamp_thickness_mm']-C['counterbore_depth_mm'])))
 # The load paths run beside the ribbon, through both insert bosses to the
 # floor and rear wall; no thin central blade underneath the cable.
 deck=deck.cut(box(cx-9.2,cy-cd/2-.1,low,18.4,cd+.2,high-low+.3));base=base.fuse(deck)
 # A single vector drawing drives the engraved roof, paint reference and 2-D proof.
 artwork=lid_markings(n,w)
 lid=artwork.engrave(lid,roof,.4)
 paint=artwork.solids(roof-.39,.03)
 (ROOT/f'preview/{n}port-lid-artwork.svg').write_text(artwork.svg((x0,y0,ow,od)))
 board=box(0,0,boardz,w,d,B['thickness_mm'])
 for x,y in holes:board=board.cut(cyl(x,y,boardz-1,1.6,4))
 pcbpath=OUT/f'{n}port/pcb.step';native=cq.importers.importStep(str(pcbpath)).val().rotate((0,0,0),(0,0,1),180).translate((w,0,boardz)) if pcbpath.exists() else None
 cable=box(cx-S['ribbon_width_mm']/2,57,axis-S['ribbon_thickness_assumed_mm']/2,S['ribbon_width_mm'],rear+10-57,S['ribbon_thickness_assumed_mm'])
 checks={'board_shell_intersection_mm3':round(board.intersect(base.fuse(lid)).Volume(),6),'native_pcb_shell_intersection_mm3':round(native.intersect(base.fuse(lid)).Volume(),6) if native else None,'base_lid_intersection_mm3':round(base.intersect(lid).Volume(),6),'clamp_shell_intersection_mm3':round(bar.intersect(base.fuse(lid)).Volume(),6),'ribbon_hard_parts_intersection_mm3':round(cable.intersect(base.fuse(lid).fuse(bar)).Volume(),6),'screw_plastic_intersection_mm3':round(sum(s.intersect(base.fuse(lid).fuse(bar)).Volume() for s in screws),6)}
 features={'minimum_structural_web_mm':2.0,'lid_counterbore_radial_web_mm':(C['boss_diameter_mm']-C['counterbore_diameter_mm'])/2,'lid_engraved_roof_mm':C['lid_mm']-.4,'lid_lower_sleeve_radial_wall_mm':4.3-C['screw_clearance_mm']/2,'clamp_counterbore_floor_mm':S['clamp_thickness_mm']-C['counterbore_depth_mm'],'insert_blind_floor_mm':boardz-I['pilot_depth_mm'],'seam_outer_web_mm':wall-C['lip_width_mm']-tol,'key_width_mm':C['lip_width_mm'],'clamp_counterbore_end_web_mm':cw/2-S['screw_pitch_mm']/2-C['counterbore_diameter_mm']/2,'clamp_counterbore_side_web_mm':cd/2-C['counterbore_diameter_mm']/2,'insert_radial_wall_mm':(S['boss_diameter_mm']-I['outer_diameter_mm'])/2,'rear_support_rib_mm':S['support_rib_mm'],'rear_support_root_radius_mm':S['support_root_radius_mm'],'rear_support_wall_overlap_mm':S['support_overlap_mm'],'mount_tab_counterbore_web_mm':tabs['thickness_mm']-tabs['counterbore_depth_mm'],'mount_tab_radial_web_mm':tabs['outer_radius_mm']-tabs['counterbore_diameter_mm']/2,'mount_tab_centers_mm':tab_centers,'base_solid_count':len(base.Solids()),'lid_solid_count':len(lid.Solids())}
 features['pass']=all(features[k]>=2 for k in ['lid_counterbore_radial_web_mm','lid_engraved_roof_mm','lid_lower_sleeve_radial_wall_mm','clamp_counterbore_floor_mm','insert_blind_floor_mm','seam_outer_web_mm','key_width_mm','clamp_counterbore_end_web_mm','clamp_counterbore_side_web_mm','insert_radial_wall_mm','rear_support_rib_mm','mount_tab_counterbore_web_mm','mount_tab_radial_web_mm']) and len(base.Solids())==len(lid.Solids())==1
 features.update(mount_tab_quantity=len(tab_centers),mount_tab_width_mm=2*tabs['outer_radius_mm'],mount_tab_root_radius_mm=tabs['root_radius_mm'],mount_tab_root_section_widths_mm=tab_root_widths)
 features['pass']=features['pass'] and len(tab_centers)==4 and all(width>=28 for width in tab_root_widths)
 mates=[];plugchecks=[];male_flange=B['port_pin_y_mm']-10.94
 for k in range(n):
  px=w-(B['first_port_x_mm']+k*B['port_pitch_mm']);parts=mating_set(px,axis,male_flange);mates.append(parts)
  for g in [M['flange_separation_min_mm'],M['flange_separation_max_mm']]:
   grown=mating_set(px,axis,male_flange,g,M['hood_tolerance_mm'])
   plugchecks.append({'port':k,'flange_separation_mm':g,'housing_intersection_mm3':round(sum(s.intersect(base.fuse(lid)).Volume() for s in grown[:3]),6)})
 lidstack=blind_insert_stack(head_seat=roof-C['counterbore_depth_mm'],screw_length=C['lid_screw_length_mm'],insert_top=boardz-I['recess_mm'],insert_length=I['length_mm'],hole_bottom=boardz-I['pilot_depth_mm'])
 clampstack=blind_insert_stack(head_seat=high+S['clamp_thickness_mm']-C['counterbore_depth_mm'],screw_length=S['screw_length_mm'],insert_top=high-I['recess_mm'],insert_length=I['length_mm'],hole_bottom=high-I['pilot_depth_mm'])
 compression=(2*S['pad_thickness_mm']+S['ribbon_thickness_assumed_mm']-S['gap_mm'])/(2*S['pad_thickness_mm'])
 review={'pass':all(v is not None and v<1e-5 for v in checks.values()) and all(c['housing_intersection_mm3']<1e-5 for c in plugchecks) and all(s['engagement_mm']>=3 and s['tip_clearance_mm']>.3 for s in [lidstack,clampstack]) and .1<=compression<=.35,'checks':checks,'physical_fit_verified':False,'slicer_run':False,'protection_tested':False,'release_ready':False,'port_checks':plugchecks,'outer_size_mm':[ow,od,roof],'mechanical_sources':source_hashes(),'mechanical_library_sha256':library_hashes(),'native_step_sha256':hashlib.sha256(pcbpath.read_bytes()).hexdigest() if pcbpath.exists() else None,'pcb_frame':{'mapping':'KiCad STEP (x,-y,z) -> housing (width-x,y,z+board_z) by 180 degree Z rotation','determinant':1,'reflection_used':False},'envelope_basis':'Native KiCad models plus original Assmann drawing envelopes; hood capture and screw seating assumed. No official manufacturer STEP.','mating':{'hood_gap_nominal_mm':B['port_pitch_mm']-M['hood_width_mm'],'hood_gap_max_width_mm':B['port_pitch_mm']-M['hood_width_mm']-M['hood_tolerance_mm'],'front_rib_mm':B['port_pitch_mm']-C['db9_window_width_mm'],'screw_engagement_verified':False,'reference':'research/mating-dsub-measurements.json'},'heat_set_inserts':{'quantity':6,'mpn':I['mpn'],'pilot_mm':C['pilot_diameter_mm'],'intentional_knurl_plastic_interference_mm3':round(sum(s.intersect(base).Volume() for s in inserts),3),'physical_installation_verified':False},'lid_screws':{'quantity':4,'size':'M3x20','counterbore_mm':[6.4,3.3],'head_recess_mm':.3,**lidstack,'pcb_pad_gap_mm':C['pcb_retention_gap_mm'],'pad_thickness_mm':C['pcb_retention_pad_mm']},'strain_relief':{'hard_stop_gap_mm':S['gap_mm'],'pad_compression_fraction_assumed':round(compression,3),'screws':'2 x M3x6 with heat-set inserts',**clampstack,'pull_test_target_N':10,'pull_test_passed':False,'ribbon_thickness_assumed_mm':.6,'limits':'Cable thickness, compression curve, pull strength, creep and bend radius unqualified.'}}
 header=box(cx-11.43,48.57,boardz+1.6,22.86,8.07,6.456)
 review['structural_features']=features;review['pass']=review['pass'] and features['pass']
 review['size_including_mounting_tabs_mm']=[ow+2*(tabs['hole_offset_from_wall_mm']+tabs['outer_radius_mm']),od,roof]
 hardware={'legend_paint':paint,'inserts':cq.Compound.makeCompound(inserts),'screws':cq.Compound.makeCompound(screws),'female':cq.Compound.makeCompound([m[0] for m in mates]),'hoods':cq.Compound.makeCompound([m[1] for m in mates]),'thumbscrews':cq.Compound.makeCompound([m[2] for m in mates]),'can_cables':cq.Compound.makeCompound([m[3] for m in mates])}
 return base,lid,bar,board,native,header,cable,hardware,review

def fit_coupon():
 s=box(0,0,0,44,24,8)
 for i,d in enumerate([3.8,3.9,4.0]):
  s=s.cut(cyl(7+i*14,6,2.9,d/2,6));s=engrave(s,str(d),2.3,7+i*14,12,8)
 for i,d in enumerate([6.2,6.4,6.6]):
  x=7+i*14;s=s.cut(cyl(x,19,-1,1.7,10)).cut(cyl(x,19,4.7,d/2,4))
 return s

def port_coupon():return box(0,0,0,38,19,3).cut(box((38-C['db9_window_width_mm'])/2,2.5,-1,C['db9_window_width_mm'],14,5))
def print_parts():
 parts={}
 for n in [2,4]:
  b,l,*_=build_variant(n);parts[f'{n}port_base']=b;parts[f'{n}port_lid']=l
 parts.update(ribbon_clamp=clamp_part(),fastener_coupon=fit_coupon(),port_coupon=port_coupon());return parts

if __name__=='__main__':
 geometry={}
 for n in (2,4):
  base,lid,bar,board,native,header,cable,hardware,review=build_variant(n)
  for name,shape,rot in [('base',base,None),('lid',lid,((1,0,0),180))]:
   part=f'{n}port_{name}';cq.exporters.export(shape,str(OUT/f'{part}.step'));geometry[part]=export_print_stl(shape,OUT/f'{part}.stl',rotation=rot);geometry[part]['physical_fit_verified']=False
  (OUT/f'{n}port/mechanical-checks.json').write_text(json.dumps(review,indent=2)+'\n')
  for name,shape in [('clamp',bar),('pcb',native),('ribbon',cable),('header',header),*hardware.items()]:
   if shape:cq.exporters.export(shape,str(OUT/f'asm_{n}port_{name}.step'))
  print(n,review['pass'],review['checks'],flush=True)
 for part,shape in [('ribbon_clamp',clamp_part()),('fastener_coupon',fit_coupon()),('port_coupon',port_coupon())]:
  cq.exporters.export(shape,str(OUT/f'{part}.step'));geometry[part]=export_print_stl(shape,OUT/f'{part}.stl');geometry[part]['physical_fit_verified']=False
 (OUT/'geometry-checks.json').write_text(json.dumps(geometry,indent=2)+'\n')
