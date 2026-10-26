#!/usr/bin/env python3
"""Dimensioned review plan from the canonical parameters (millimeters)."""
import json,html,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=json.loads((R/'cad/parameters.json').read_text());B=P['pcb'];C=P['case'];S=P['strain_relief'];M=P['mating']
for n in [2,4]:
 w=B[f'width_{n}port_mm'];outer=C['wall_mm']+C['board_clearance_mm'];rear=B['depth_mm']+C['rear_extension_mm'];scale=min(4.0,840/(w+2*outer));ox=65+outer*scale;oy=295
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="850" viewBox="0 0 1200 850">','<rect width="1200" height="850" fill="#f6f5ef"/>','<style>text{font-family:DejaVu Sans,sans-serif;fill:#152b36} .dim{stroke:#176962;stroke-width:1;fill:none} .body{stroke:#233d49;stroke-width:2;fill:#e0e9e8}</style>']
 def text(x,y,t,size=15):out.append(f'<text x="{x}" y="{y}" font-size="{size}">{html.escape(str(t))}</text>')
 def rect(x,y,dx,dy,fill,stroke='#334d5b'):
  out.append(f'<rect x="{ox+x*scale:.2f}" y="{oy+y*scale:.2f}" width="{dx*scale:.2f}" height="{dy*scale:.2f}" fill="{fill}" stroke="{stroke}"/>')
 def dim(x1,y1,x2,y2,label):
  a,b,c,d=ox+x1*scale,oy+y1*scale,ox+x2*scale,oy+y2*scale
  out.append(f'<path class="dim" d="M {a} {b} L {c} {d} M {a-4} {b-4} L {a+4} {b+4} M {c-4} {d-4} L {c+4} {d+4}"/>');text((a+c)/2+4,(b+d)/2-6,label,13)
 text(45,43,f'THOR CAN / {n}-PORT ENCLOSURE',27);text(45,73,'A0 DEVELOPMENT · DIMENSIONAL REVIEW · ALL DIMENSIONS mm',15)
 text(45,101,'github.com/mvalancy/pcb-agx-thor-can-breakout',14)
 rect(-outer,-outer,w+2*outer,rear+2*outer,'#dbe7e6');rect(0,0,w,65,'#f6f5ef')
 for x,y in [(4,4),(w-4,4),(4,61),(w-4,61)]:
  out.append(f'<circle cx="{ox+x*scale}" cy="{oy+y*scale}" r="{3.2*scale}" fill="none" stroke="#233d49"/>')
 for k in range(n):
  x=B['first_port_x_mm']+k*B['port_pitch_mm'];rect(x-16.9,-36.9,33.8,33.3,'#566670')
  text(ox+(x-8)*scale,oy+9*scale,f'CAN{k}' if k<2 else f'RES{k}',14)
  rect(x-C['db9_window_width_mm']/2,-outer,C['db9_window_width_mm'],outer,'#f7f6ee')
  if k<n-1:dim(x,-42,x+B['port_pitch_mm'],-42,'42 pitch')
 cx=w/2-10;rect(cx-S['clamp_width_mm']/2,S['clamp_y_mm']-5,S['clamp_width_mm'],10,'#dba76c')
 for dx in [-14,14]:out.append(f'<circle cx="{ox+(cx+dx)*scale}" cy="{oy+72*scale}" r="{3.2*scale}" fill="#f6f5ef" stroke="#233d49"/>')
 dim(-outer,rear+outer+7,w+outer,rear+outer+7,f'{w+2*outer:.1f} overall')
 dim(w+outer+6,-outer,w+outer+6,rear+outer,f'{rear+2*outer:.1f}')
 tx=935
 for i,line in enumerate(['ASSEMBLY NOTES','Height 26.8','Port rib 9.8','Hood gap ≥7.7*','Wall 3.0','Floor / roof 2.4','Tongue 1.4 × 1.6','Groove clearance 0.25/side','6 × M3 heat-set inserts','4 × M3×20 lid screws','2 × M3×6 clamp screws','Counterbores Ø6.4 × 3.3','Head recess 0.3','Clamp screw pitch 28','Clamp hard gap 1.8']):text(tx,145+29*i,line,16 if i==0 else 13)
 text(45,770,'* Maximum-width A-FT09 hood envelope; exact capture and thumbscrew seating remain unverified.',14)
 text(45,797,'Plan envelopes shown; use STEP for geometry. Print coupons and verify actual parts before ordering a batch.',14)
 text(45,824,'Parameter SHA256 '+hashlib.sha256((R/'cad/parameters.json').read_bytes()).hexdigest()[:20],11)
 out.append('</svg>');(R/f'exports/{n}port/enclosure-plan.svg').write_text('\n'.join(out)+'\n')
