"""Thor visual identity and male DE-9 pinout: same strokes drive print and proof."""
from cadagent.markings import PanelMarkings

def lid_markings(n,w):
 m=PanelMarkings();cx=w/2
 # A compact nameplate with a paired-line motif, leaving the insert towers clear.
 m.text('THOR',cx-9,97,6.7,bold=True);m.text('CAN',cx+19,97,5.1,bold=True)
 for dy in [-1.4,1.4]:m.line([(cx-35.5,97+dy),(cx-31.5,97+dy),(cx-28.5,100+dy),(cx-23.5,100+dy)],.7)
 m.line([(10,89),(w-10,89)],.6)
 m.text('PCB-THOR-CAN  /  A1 DEV',cx,92,2.15,bold=True)
 m.text('120R: JP1 / JP2  -  DEFAULT OPEN',cx,78,2.1,bold=True)
 m.text('AUX + PROTOTYPING INSIDE',cx,83,2.2,bold=True)
 m.text('DE-9 MALE  /  MATING FACE',cx,57.7,2.25,bold=True)
 # Male mating face, 5-pin wide row above 4-pin row. No solder-side mirroring.
 m.line([(cx-17,52.5),(cx+17,52.5),(cx+14.2,35.5),(cx-14.2,35.5),(cx-17,52.5)],.65)
 for i in range(5):
  x=cx+(i-2)*6;m.circle(x,47,1.85,.45);m.text(str(i+1),x,47,2.2,bold=True)
 for i in range(4):
  x=cx+(i-1.5)*6;m.circle(x,40.5,1.85,.45);m.text(str(i+6),x,40.5,2.2,bold=True)
 # Short labeled leaders read as a wiring diagram, not a text paragraph.
 m.line([(cx-6,49),(cx-6,54.7),(cx-29,54.7),(cx-29,50)],.45)
 m.text('2 / CAN-L',cx-29,47.3,2.2,bold=True)
 m.line([(cx-3,38.5),(cx-3,33),(cx-29,33),(cx-29,37)],.45)
 m.text('7 / CAN-H',cx-29,39.7,2.2,bold=True)
 m.line([(cx+0,49),(cx+0,54.7),(cx+29,54.7),(cx+29,50)],.45)
 m.text('3,6 / GND',cx+29,47.3,2.2,bold=True)
 m.line([(cx+15.2,41),(cx+20,41),(cx+20,33),(cx+29,33),(cx+29,37)],.45)
 m.text('5 + SHELL',cx+29,40.5,2.1,bold=True);m.text('SHIELD',cx+29,37.9,1.9,bold=True)
 m.text('1 / 4 / 8 / 9 : NC   -   NO POWER ON PIN 9',cx,27.9,2,bold=True)
 # Port badges align with the actual 42 mm connector pitch.
 for k in range(n):
  x=w-(25.5+42*k);mark=f'CAN {k}' if k<2 else f'RES {k}'
  m.line([(x-16,6),(x+13,6),(x+16,9),(x+16,19),(x-13,19),(x-16,16),(x-16,6)],.6)
  m.text(mark,x,12.3,4,bold=True)
  m.line([(x-3,4),(x,1.8),(x+3,4)],.65)
 m.text('github.com/mvalancy',cx,23.1,2.2,bold=True)
 return m
