#!/usr/bin/env python3
"""Route paired CAN trunks before routing auxiliary nets; run with KiCad Python.
Preserves footprint identities and schematic nets. Both sides follow one offset
centerline; connector/header fan-outs remain explicit and are checked separately.
"""
import json,math,subprocess,sys
from pathlib import Path
import pcbnew as p
R=Path(__file__).resolve().parents[1];mm=p.FromMM
vec=lambda x,y:p.VECTOR2I(mm(x),mm(y))
xy=lambda q:(p.ToMM(q.x),p.ToMM(q.y))
if len(sys.argv)==1:
 for v in ['2port','4port']:subprocess.run([sys.executable,__file__,v],check=True)
 raise SystemExit
v=sys.argv[1];n=int(v[0]);path=R/f'hardware/{v}/thor-{v}.kicad_pcb';b=p.LoadBoard(str(path));fps={f.GetReference():f for f in b.GetFootprints()}
for t in list(b.GetTracks()):b.Delete(t)
for z in list(b.Zones()):
 if not z.GetZoneName().startswith('Prototype '):b.Delete(z)
nets={net.GetNetname():net for net in b.GetNetsByName().values()}
ground='/GND' if '/GND' in nets else 'GND'
def trace(net,points,layer=p.F_Cu,width=.25):
 for a,c in zip(points,points[1:]):
  if math.dist(a,c)<1e-6:continue
  t=p.PCB_TRACK(b);t.SetStart(vec(*a));t.SetEnd(vec(*c));t.SetLayer(layer);t.SetWidth(mm(width));t.SetNet(nets[net]);t.SetLocked(True);b.Add(t)
def via(net,x,y):
 t=p.PCB_VIA(b);t.SetPosition(vec(x,y));t.SetWidth(mm(.6));t.SetDrill(mm(.3));t.SetViaType(p.VIATYPE_THROUGH);t.SetLayerPair(p.F_Cu,p.B_Cu);t.SetNet(nets[net]);t.SetLocked(True);b.Add(t)
def offset(points,d):
 # Left normal of the direction of travel, with mitered corners.
 dirs=[((c[0]-a[0])/math.dist(a,c),(c[1]-a[1])/math.dist(a,c)) for a,c in zip(points,points[1:])]
 normals=[(-y,x) for x,y in dirs];out=[]
 for i,(x,y) in enumerate(points):
  if i==0:nx,ny=normals[0]
  elif i==len(points)-1:nx,ny=normals[-1]
  else:
   u=normals[i-1];z=normals[i];den=1+u[0]*z[0]+u[1]*z[1];nx=(u[0]+z[0])/den;ny=(u[1]+z[1])/den
  out.append((x+d*nx,y+d*ny))
 return out
def protect_return(points):
 # Native B.Cu track/via keepouts reserve GND beneath each F.Cu paired trunk.
 # Copper pour remains allowed; these areas constrain auxiliary autorouting.
 for a,c in zip(points,points[1:]):
  length=math.dist(a,c);nx=-(c[1]-a[1])/length;ny=(c[0]-a[0])/length;half=1.15
  z=p.ZONE(b);z.SetLayer(p.B_Cu);z.SetIsRuleArea(True);z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowZoneFills(False);z.SetDoNotAllowPads(False);z.SetDoNotAllowFootprints(False)
  poly=z.Outline();poly.NewOutline()
  for x,y in [(a[0]+nx*half,a[1]+ny*half),(c[0]+nx*half,c[1]+ny*half),(c[0]-nx*half,c[1]-ny*half),(a[0]-nx*half,a[1]-ny*half)]:poly.Append(mm(x),mm(y))
  b.Add(z)
parts=json.loads((R/f'exports/{v}/components.json').read_text())
for k in range(n):
 j=fps[f'J{k+2}'];dp={pad.GetNumber():xy(pad.GetPosition()) for pad in j.Pads()};cx=25.5+42*k;dx=cx+2.08
 tvs=fps[f'D{k+1}'];tvs.SetPosition(vec(dx,12.5));tvs.SetOrientationDegrees(90)
 jp=fps[f'JP{k+1}'];jp.SetPosition(vec(dx-2,19))
 for part in parts:
  if part['ref']==tvs.GetReference():part.update(x=dx,y=12.5,a=90)
  if part['ref']==jp.GetReference():part.update(x=dx-2,y=19,a=0)
 hp,lp=(3+4*k,5+4*k);header={int(pad.GetNumber()):pad for pad in fps['J1'].Pads()};sx=(xy(header[hp].GetPosition())[0]+xy(header[lp].GetPosition())[0])/2
 delta=dx-sx
 if abs(delta)<15:centers=[(sx,46.3),(sx,45),(dx,45-abs(delta)),(dx,15)]
 else:
  bendy=30 if k in [0,n-1] else 24;turnx=sx+math.copysign(45-bendy,delta)
  centers=[(sx,46.3),(sx,45),(turnx,bendy),(dx,bendy),(dx,15)]
 protect_return(centers[1:])
 for side,pin,dpad,portpin,d in [('H',hp,'1','7',-.25),('L',lp,'2','2',.25)]:
  net=header[pin].GetNetname();hx,hy=xy(header[pin].GetPosition());route=offset(centers,d)
  trace(net,[(hx,hy),(hx,56.2)]);via(net,hx,56.2)
  trace(net,[(hx,56.2),(hx,47.3)],p.B_Cu);via(net,hx,47.3)
  trace(net,[(hx,47.3),(sx+d,46.915),route[0],*route[1:]])
  pad=next(pad for pad in tvs.Pads() if pad.GetNumber()==dpad);px,py=xy(pad.GetPosition())
  trace(net,[route[-1],(px,14.3),(px,py)])
  end=dp[portpin];trace(net,[(px,py),(px,11.3),(end[0],11.3-abs(px-end[0])),end])
 # A short side branch to the open termination shunt; no bus-length detour.
 hnet=header[hp].GetNetname();trace(hnet,[(dx-.25,19),(dx-2,19)])
 # Route the four-port termination controls inside each fanout wedge.
 # A short bottom header escape returns to top between adjacent CAN pairs.
 if v=='4port' and k>0:
  term=header[hp+1];tx,ty=xy(term.GetPosition());net=term.GetNetname()
  trace(net,[(tx,ty),(tx,51.365),(sx,52)]);via(net,sx,52)
  ux=sx-1.27;trace(net,[(sx,52),(sx,46.67),(ux,46.67)],p.B_Cu);via(net,ux,46.67)
  control=offset(centers,-.9);control[-1]=(dx-.9,21.54)
  trace(net,[(ux,46.67),*control,(dx-2,21.54)])
 # Two short ground vias immediately at the protection device's ground pad.
 gx,gy=xy(next(pad for pad in tvs.Pads() if pad.GetNumber()=='3').GetPosition())
 for vy in [gy-.9,gy-1.7]:trace(ground,[(gx,gy),(gx,vy)],width=.4);via(ground,gx,vy)
# Dense header escapes use fixed between-pad vias, never vias in SMD pads.
escapes=[(8,.635),(20,-.635)] if v=='2port' else [(6,-.635)]
for number,offset_x in escapes:
 pad=next(pad for pad in fps['J1'].Pads() if pad.GetNumber()==str(number));hx,hy=xy(pad.GetPosition());net=pad.GetNetname()
 if number%2:trace(net,[(hx,hy),(hx,56.2)]);via(net,hx,56.2)
 else:
  trace(net,[(hx,hy),(hx,51.365),(hx+offset_x,52.0)]);via(net,hx+offset_x,52.0)
  if v=='4port':trace(net,[(hx+offset_x,52.0),(hx+offset_x,58)],p.B_Cu)
# Ground stitching at both ends of the local header layer transitions.
for x in [xy(next(pad for pad in fps['J1'].Pads() if pad.GetNumber()==str(q)).GetPosition())[0] for q in [1,19]]:
 for y in [46.2,57.5]:via(ground,x,y)
# Factory minimum readable silk; placement is rechecked after auxiliary routing.
if v=='2port':
 # Keep the added prototype supply above the rear raw-I/O crossings and away
 # from the adjacent GND tap's exposed solder mask.
 power='/AUX_3V3' if '/AUX_3V3' in nets else 'AUX_3V3'
 trace(power,[(53.5,53.54),(53.5,57.5)],p.B_Cu);via(power,53.5,57.5)
 trace(power,[(53.5,57.5),(53.73,57.27),(55.4,57.27),(55.4,62.72),(53.58,64.54)])
for f in b.GetFootprints():
 for t in [f.Reference(),f.Value()]:
  if t.IsVisible():t.SetTextSize(vec(1,1));t.SetTextThickness(mm(.15))
for t in b.GetDrawings():
 if isinstance(t,p.PCB_TEXT):t.SetTextSize(vec(1,1));t.SetTextThickness(mm(.15))
b.BuildConnectivity();p.SaveBoard(str(path),b)
p.ExportSpecctraDSN(b,str(R/f'exports/{v}/unrouted.dsn'))
(R/f'exports/{v}/components.json').write_text(json.dumps(parts,indent=2)+'\n')
print(v,'paired routes locked; auxiliary nets require routing and native DRC')
