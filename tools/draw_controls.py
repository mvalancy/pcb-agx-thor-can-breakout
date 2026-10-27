#!/usr/bin/env python3
"""Readable assembly/control maps from actual exported native pad coordinates."""
from pathlib import Path
import json, html
R=Path(__file__).resolve().parents[1];P=json.loads((R/'cad/parameters.json').read_text())
for v in ['2port','4port']:
 n=int(v[0]);w=P['pcb'][f'width_{v}_mm'];d=P['pcb']['depth_mm'];s=min(6.8,690/w);ox=65;oy=155
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1030" viewBox="0 0 1200 1030">','<rect width="1200" height="1030" fill="#f6f5ef"/>','<style>text{font-family:DejaVu Sans,sans-serif;fill:#17313b} .small{font-size:13px}</style>']
 def text(x,y,t,size=16,color='#17313b',anchor='start'):
  out.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" style="fill:{color}">{html.escape(t)}</text>')
 def rect(x,y,ww,hh,fill,stroke='none',rx=0):out.append(f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')
 def line(points,color='#25665f',width=2):out.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="{width}"/>')
 def pad(x,y,color='#f8e7af',r=.75):out.append(f'<circle cx="{ox+x*s}" cy="{oy+y*s}" r="{r*s}" fill="{color}" stroke="#244e4c" stroke-width="1"/>')
 def box(x,y,ww,hh,color,stroke='#357970'):rect(ox+x*s,oy+y*s,ww*s,hh*s,color,stroke)
 text(45,50,f'THOR CAN / {n}-PORT CONTROLS',30);text(45,81,'PCB component-side plan · all shunts removed at delivery · dimensions in millimeters',16)
 text(45,112,'Native KiCad orientation shown; enclosure assembly views use their own marked viewing direction.',14)
 box(0,0,w,d,'#d8e8df');cx=w/2-10
 for x,y in [(4,4),(w-4,4),(4,d-4),(w-4,d-4)]:pad(x,y,'#fff',1.6)
 for k in range(n):
  x=25.5+k*42;name=f'CAN {k}' if k<2 else f'RES {k}'
  box(x-15,0,30,10,'#748995');text(ox+x*s,oy+6*s,name,14,'#fff','middle')
  box(x-2.5,17,5.2,6.4,'#fff3d4');pad(x+.08,19);pad(x+.08,21.54)
  text(ox+x*s,oy+27*s,f'JP{k+1} / 120Ω',13,anchor='middle')
 box(cx-11.5,48.5,23,8.5,'#33474e');text(ox+cx*s,oy+53.5*s,'J1 / THOR',12,'#fff','middle')
 box(cx-12,59,24,27,'#f0c8bb');text(ox+cx*s,oy+76*s,'RIBBON',11,anchor='middle');text(ox+cx*s,oy+79*s,'KEEP CLEAR',10,anchor='middle')
 for ref,x,color in [('JP5',w/2+7,'#e8bc48'),('JP6',w/2+13,'#e69573')]:
  box(x-1.7,49.5,3.4,5.5,color);pad(x,51);pad(x,53.54);text(ox+x*s,oy+47*s,ref,10,anchor='middle')
 for row in range(7):
  for col in range(2):pad(w-16+col*2.54,39+row*2.54)
 text(ox+(w-14.7)*s,oy+36*s,'J10',12,anchor='middle')
 box(w-11.7,24.5,3.4,5.5,'#d3d3e8');pad(w-10,26);pad(w-10,28.54)
 text(ox+(w-10)*s,oy+32*s,'J12 / SHIELD',9,anchor='middle')
 if n==2:
  for row in range(3):
   for col in range(2):pad(13+col*2.54,40+row*2.54)
  text(ox+14.2*s,oy+49*s,'J11 / RESERVED',10,anchor='middle')
 proto=json.loads((R/f'exports/{v}/prototype-review.json').read_text())
 for grid in proto['grids']:
  x,y=grid['x_range_mm'][0],grid['y_range_mm'][0]
  for row in range(6):
   for col in range(grid['columns']):pad(x+2.54*col,y+2.54*row,'#edc66f',.65)
  text(ox+(sum(grid['x_range_mm'])/2)*s,oy+87.8*s,f"{grid['reference']} / {grid['columns']} × 6",10,anchor='middle')
  for row,color in enumerate(['#b0c0b9','#e8bc48','#e69573']):
   for col in range(3):pad(x+2.54*col,62+row*2.54,color)
   text(ox+(x+7)*s,oy+(62+row*2.54+.5)*s,['GND','3V3','5V'][row],9)
 tx=805
 text(tx,175,'TERMINATION',20)
 for i,t in enumerate(['JP1 → CAN0 (J47 3–4)','JP2 → CAN1 (J47 7–8)','JP3/JP4 → reserved channels','only on a verified carrier.','Fit shunts only at the two','physical ends of the CAN bus.']):text(tx,204+25*i,t,15)
 text(tx,385,'POWER & RAW I/O',20)
 for i,t in enumerate(['JP5 → enable AUX 3.3 V','JP6 → enable AUX 5 V','No shunts = power taps OFF','J10 exposes all non-CAN I/O.','FSI6 is FSI firmware owned;','it is not a Linux GPIO.','No 24 V inputs or backfeed.']):text(tx,414+25*i,t,15)
 text(tx,620,'PROTOTYPING',20)
 for i,t in enumerate([f"{proto['isolated_pads']} isolated plated holes",'2.54 pitch / 1.0 drill / 1.8 pad','Each pad is independent.','3-hole rows: GND / 3V3 / 5V','Keep parts inside pad regions.','Max: 12 above PCB / 3 below.']):text(tx,649+25*i,t,15)
 rect(45,805,1110,185,'#e6ece8',rx=12)
 text(65,835,'HOW THE SHUNT ENABLES THE CARRIER’S EXISTING 120 Ω RESISTOR',19)
 # Functional circuit; the resistor is on the host, not the adapter.
 text(75,888,'CAN_H',16);line([(150,883),(220,883)])
 for x in [220,270]:out.append(f'<circle cx="{x}" cy="883" r="5" fill="#fff" stroke="#25665f" stroke-width="2"/>')
 line([(270,883),(380,883)]);text(292,872,'TERM',14)
 rect(380,871,95,24,'#fff','#25665f');text(427,889,'120 Ω',15,anchor='middle');line([(475,883),(555,883)]);text(568,888,'CAN_L',16)
 text(65,924,'OPEN (default): leave both pins uncovered.',15)
 text(65,950,'ON: fit one 2.54 mm jumper cap over the two pins of the selected JP header.',15)
 rect(760,856,360,105,'#fff',rx=8)
 text(780,883,'Power OFF before fitting or measuring.',14);text(780,910,'One enabled endpoint: about 120 Ω.',14);text(780,937,'Two endpoints on the bus: about 60 Ω.',14)
 text(45,1015,'Development hardware · physical qualification pending · github.com/mvalancy/pcb-agx-thor-can-breakout',13)
 out.append('</svg>');(R/f'exports/{v}/controls.svg').write_text('\n'.join(out)+'\n')
