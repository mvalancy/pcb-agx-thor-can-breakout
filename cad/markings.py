"""Large, bold Thor lid markings: the same drawing drives engraving and proof."""
from cadagent.markings import PanelMarkings

def lid_markings(n,w,style):
 m=PanelMarkings();cx=w/2;stroke=style['stroke_width_mm'];body=style['text_height_mm']
 # The smallest lettering is now 4 mm; all lines/rings are 1 mm wide. Move the
 # URL to the nameplate and split the front notes to preserve whitespace.
 m.text('THOR',cx-10,98,8.5,bold=True);m.text('CAN',cx+23,98,6.5,bold=True)
 for dy in [-1.8,1.8]:m.line([(cx-40,97+dy),(cx-36,97+dy),(cx-32,100+dy),(cx-28,100+dy)],stroke)
 m.text('PCB-THOR-CAN  /  A1 DEV',cx,92.3,body,bold=True)
 m.text('github.com/mvalancy',cx,86.7,body,bold=True)
 m.line([(10,82.7),(w-10,82.7)],stroke)
 m.text('AUX + PROTOTYPING INSIDE',cx,78.7,body,bold=True)
 m.text('120R: JP1 / JP2',cx,72.8,body,bold=True)
 m.text('DEFAULT OPEN',cx,68.2,body,bold=True)
 m.text('DE-9 MALE / MATING FACE',cx,62.8,body,bold=True)
 # Male mating face: five pins above four, with enlarged digits and islands.
 m.line([(cx-23.5,58),(cx+23.5,58),(cx+20,35.5),(cx-20,35.5),(cx-23.5,58)],stroke)
 for i in range(5):
  x=cx+(i-2)*8.5;m.circle(x,51.8,3.1,stroke);m.text(str(i+1),x,51.8,style['pin_number_height_mm'],bold=True)
 for i in range(4):
  x=cx+(i-1.5)*8.5;m.circle(x,43,3.1,stroke);m.text(str(i+6),x,43,style['pin_number_height_mm'],bold=True)
 m.line([(cx-8.5,54.9),(cx-8.5,60),(cx-35.5,60),(cx-35.5,54.5)],stroke)
 m.text('2 CAN-L',cx-35.5,49.6,body,bold=True)
 m.line([(cx-4.25,39.9),(cx-4.25,33),(cx-35.5,33),(cx-35.5,37)],stroke)
 m.text('7 CAN-H',cx-35.5,40.7,body,bold=True)
 m.line([(cx,54.9),(cx,60),(cx+35.5,60),(cx+35.5,54.5)],stroke)
 m.text('3,6 GND',cx+35.5,50,body,bold=True)
 m.line([(cx+21.5,46.3),(cx+24.5,46.3),(cx+24.5,33),(cx+35.5,33),(cx+35.5,36)],stroke)
 m.text('5+SHELL',cx+35.5,44.4,body,bold=True);m.text('SHIELD',cx+35.5,39.6,body,bold=True)
 m.text('1 / 4 / 8 / 9 : NC',cx,29.5,body,bold=True)
 m.text('PIN 9: NO POWER',cx,24.4,body,bold=True)
 for k in range(n):
  x=w-(25.5+42*k);mark=f'CAN {k}' if k<2 else f'RES {k}'
  m.line([(x-16,6),(x+13,6),(x+16,9),(x+16,19),(x-13,19),(x-16,16),(x-16,6)],stroke)
  m.text(mark,x,12.3,5.2,bold=True)
  m.line([(x-3,4),(x,1.8),(x+3,4)],stroke)
 return m
