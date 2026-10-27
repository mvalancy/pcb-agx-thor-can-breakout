#!/usr/bin/env python3
"""Dimensioned review plan from the canonical parameters (millimeters)."""
import json,html,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=json.loads((R/'cad/parameters.json').read_text());B=P['pcb'];C=P['case'];S=P['strain_relief'];M=P['mating']
for n in [2,4]:
 w=B[f'width_{n}port_mm'];outer=C['wall_mm']+C['board_clearance_mm'];rear=B['depth_mm']+C['rear_extension_mm'];scale=min(3.8,775/(w+2*outer+2*(P['mounting_tabs']['hole_offset_from_wall_mm']+P['mounting_tabs']['outer_radius_mm'])));ox=100+outer*scale;oy=275
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="850" viewBox="0 0 1200 850">','<rect width="1200" height="850" fill="#f6f5ef"/>','<style>text{font-family:DejaVu Sans,sans-serif;fill:#152b36} .dim{stroke:#176962;stroke-width:1;fill:none} .body{stroke:#233d49;stroke-width:2;fill:#e0e9e8}</style>']
 def text(x,y,t,size=15):out.append(f'<text x="{x}" y="{y}" font-size="{size}">{html.escape(str(t))}</text>')
 def rect(x,y,dx,dy,fill,stroke='#334d5b'):
  out.append(f'<rect x="{ox+x*scale:.2f}" y="{oy+y*scale:.2f}" width="{dx*scale:.2f}" height="{dy*scale:.2f}" fill="{fill}" stroke="{stroke}"/>')
 def dim(x1,y1,x2,y2,label):
  a,b,c,d=ox+x1*scale,oy+y1*scale,ox+x2*scale,oy+y2*scale
  out.append(f'<path class="dim" d="M {a} {b} L {c} {d} M {a-4} {b-4} L {a+4} {b+4} M {c-4} {d-4} L {c+4} {d+4}"/>');text((a+c)/2+4,(b+d)/2-6,label,13)
 text(45,43,f'THOR CAN / {n}-PORT ENCLOSURE',27);text(45,73,'A1 DEVELOPMENT · DIMENSIONAL REVIEW · ALL DIMENSIONS mm',15)
 text(45,91,'github.com/mvalancy/pcb-agx-thor-can-breakout',14)
 T=P['mounting_tabs']
 for side in [-1,1]:
  wx=-outer if side<0 else w+outer;x=wx+side*T['hole_offset_from_wall_mm'];r=T['outer_radius_mm'];fillet=T['root_radius_mm']
  def pt(px,py):return f'{ox+px*scale:.2f} {oy+py*scale:.2f}'
  for y in T['y_centers_mm']:
   sweep=1 if side>0 else 0;root_sweep=1-sweep
   path=(f'M {pt(x,y-r)} A {r*scale} {r*scale} 0 0 {sweep} {pt(x,y+r)} '
         f'L {pt(wx+side*fillet,y+r)} A {fillet*scale} {fillet*scale} 0 0 {root_sweep} {pt(wx,y+r+fillet)} '
         f'L {pt(wx-side*T["overlap_mm"],y+r+fillet)} L {pt(wx-side*T["overlap_mm"],y-r-fillet)} '
         f'L {pt(wx,y-r-fillet)} A {fillet*scale} {fillet*scale} 0 0 {root_sweep} {pt(wx+side*fillet,y-r)} Z')
   out.append(f'<path d="{path}" fill="#dbe7e6" stroke="#233d49"/>')
   for radius,fill in [(T['counterbore_diameter_mm']/2,'#b7cfcd'),(T['hole_diameter_mm']/2,'#fff')]:
    out.append(f'<circle cx="{ox+x*scale}" cy="{oy+y*scale}" r="{radius*scale}" fill="{fill}" stroke="#233d49"/>')
 rect(-outer,-outer,w+2*outer,rear+2*outer,'#dbe7e6');rect(0,0,w,B['depth_mm'],'#f6f5ef')
 for x,y in [(4,4),(w-4,4),(4,B['depth_mm']-4),(w-4,B['depth_mm']-4)]:
  out.append(f'<circle cx="{ox+x*scale}" cy="{oy+y*scale}" r="{3.2*scale}" fill="none" stroke="#233d49"/>')
 for k in range(n):
  x=w-(B['first_port_x_mm']+k*B['port_pitch_mm']);rect(x-16.9,-36.9,33.8,33.3,'#566670')
  text(ox+(x-8)*scale,oy+9*scale,f'CAN{k}' if k<2 else f'RES{k}',14)
  rect(x-C['db9_window_width_mm']/2,-outer,C['db9_window_width_mm'],outer,'#f7f6ee')
  if k<n-1:dim(x,-42,x-B['port_pitch_mm'],-42,'42 pitch')
 cx=w/2+10;rect(cx-S['clamp_width_mm']/2,S['clamp_y_mm']-S['clamp_depth_mm']/2,S['clamp_width_mm'],S['clamp_depth_mm'],'#dba76c')
 for dx in [-14,14]:out.append(f'<circle cx="{ox+(cx+dx)*scale}" cy="{oy+S['clamp_y_mm']*scale}" r="{3.2*scale}" fill="#f6f5ef" stroke="#233d49"/>')
 dim(-outer,rear+outer+7,w+outer,rear+outer+7,f'{w+2*outer:.1f} case body')
 dim(w+outer+30,-outer,w+outer+30,rear+outer,f'{rear+2*outer:.1f}')
 ext=T['hole_offset_from_wall_mm']+T['outer_radius_mm']
 dim(-outer-ext,rear+outer+14,w+outer+ext,rear+outer+14,f'{w+2*outer+2*ext:.1f} including ears')
 tx=935
 for i,line in enumerate(['ASSEMBLY NOTES','Height 26.8','Port rib 9.8','Hood gap ≥7.7*',f"Wall {C['wall_mm']}",'Floor / roof 2.4',f"Tongue {C['lip_width_mm']} × {C['lip_height_mm']}",'Groove clearance 0.25/side','6 × M3 heat-set inserts','4 × M3×20 lid screws','2 × M3×6 clamp screws','Counterbores Ø6.4 × 3.3','Head recess 0.3','Clamp screw pitch 28','Clamp hard gap 1.8','4 × 26-wide M3 ears / R4 roots',f'Mount pitch {w+2*outer+2*T["hole_offset_from_wall_mm"]:.1f} × 76','Rear ribs 3.2 / roots R1.6']):text(tx,145+29*i,line,16 if i==0 else 13)
 text(45,770,'* Maximum-width A-FT09 hood envelope; exact capture and thumbscrew seating remain unverified.',14)
 text(45,797,'Plan envelopes shown; use STEP for geometry. Print coupons and verify actual parts before ordering a batch.',14)
 text(45,824,'Parameter SHA256 '+hashlib.sha256((R/'cad/parameters.json').read_bytes()).hexdigest()[:20],11)
 out.append('</svg>');(R/f'exports/{n}port/enclosure-plan.svg').write_text('\n'.join(out)+'\n')
