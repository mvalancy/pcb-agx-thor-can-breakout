#!/usr/bin/env python3
"""Native copper path/return-plane measurements. Run with KiCad Python."""
import sys,subprocess,json,hashlib,math,os
from pathlib import Path
import pcbnew as p
R=Path(__file__).resolve().parents[1]
# Shared cad-agent is installed in the main project venv; KiCad has its own Python.
module_root=subprocess.check_output([str(R/'.venv/bin/python'),'-c','import cadagent,pathlib;print(pathlib.Path(cadagent.__file__).parent.parent)'],text=True,env={k:v for k,v in os.environ.items() if k not in {'PYTHONHOME','PYTHONPATH'}}).strip()
sys.path.insert(0,module_root)
import cadagent.pcb_routing as routing_library
from cadagent.pcb_routing import copper_graph,shortest_path,path_segments,pair_geometry,sample_segments
xy=lambda q:(round(p.ToMM(q.x),5),round(p.ToMM(q.y),5))
if len(sys.argv)==1:
 for v in ['2port','4port']:subprocess.run([sys.executable,__file__,v],check=True)
 raise SystemExit
v=sys.argv[1];n=int(v[0]);path=R/f'hardware/{v}/thor-{v}.kicad_pcb';board=p.LoadBoard(str(path));pads={(f.GetReference(),pad.GetNumber()):pad for f in board.GetFootprints() for pad in f.Pads()};zones=[z for z in board.Zones() if z.GetNetname()=='/GND'];errors=[];channels=[];drawing=[]
for k in range(n):
 results={};paths={};graphs={};sample_points=[]
 for side,pin,outpin in [('H',3+4*k,'7'),('L',5+4*k,'2')]:
  source=pads['J1',str(pin)];net=source.GetNetname();segments=[];vias=[]
  for t in board.GetTracks():
   if t.GetNetname()!=net:continue
   if isinstance(t,p.PCB_VIA):vias.append({'xy':xy(t.GetPosition()),'layers':['F.Cu','B.Cu']})
   else:segments.append({'a':xy(t.GetStart()),'b':xy(t.GetEnd()),'layer':t.GetLayerName(),'width':p.ToMM(t.GetWidth())})
  graph=copper_graph(segments,vias);start=(*xy(source.GetPosition()),'F.Cu');end=(*xy(pads[f'J{k+2}',outpin].GetPosition()),'F.Cu');length,nodes=shortest_path(graph,start,end);main=path_segments(graph,nodes);graphs[side]=graph;paths[side]=main
  tvs=(*xy(pads[f'D{k+1}','1' if side=='H' else '2'].GetPosition()),'F.Cu');changes=sum(a[2]!=b[2] for a,b in zip(nodes,nodes[1:]));missing=0;total=0;longest=0;run=0
  for q,s,weight in sample_segments(main,.1):
   # Connector/header/TVS fanouts are measured separately from the paired trunk.
   if not 15<=q[1]<=45:continue
   ref=p.B_Cu if s['layer']=='F.Cu' else p.F_Cu
   supported=any(z.GetLayer()==ref and z.HitTestFilledArea(ref,p.VECTOR2I(p.FromMM(q[0]),p.FromMM(q[1]))) for z in zones)
   total+=weight
   if not supported:missing+=weight;run+=weight;sample_points.append(q)
   else:run=0
   longest=max(longest,run)
  results[side]={'main_length_mm':round(length,4),'layer_transitions':changes,'tvs_on_main_path':tvs in nodes,'trunk_reference_coverage_fraction':round(1-missing/total,4),'longest_reference_gap_mm':round(longest,4)}
  if tvs not in nodes:errors.append(f'CAN{k} {side}: TVS bypassed by main path')
  if changes!=2:errors.append(f'CAN{k} {side}: unexpected layer changes {changes}')
  if longest>1.0:errors.append(f'CAN{k} {side}: return-plane gap exceeds 1 mm')
  if missing/total>.05:errors.append(f'CAN{k} {side}: trunk ground reference below 95%')
  if side=='H':
   branch=(*xy(pads[f'JP{k+1}','1'].GetPosition()),'F.Cu');stub=min(shortest_path(graph,branch,node)[0] for node in nodes)
   results[side]['termination_branch_mm']=round(stub,4)
   if stub>2:errors.append(f'CAN{k}: termination branch >2 mm')
  drawing.extend((s,side,k) for s in main)
 mismatch=abs(results['H']['main_length_mm']-results['L']['main_length_mm']);coupling=pair_geometry(paths['H'],paths['L'],window=(-1,15,200,45),step=.1)
 if mismatch>3.2:errors.append(f'CAN{k}: length imbalance >3.2 mm')
 if coupling['edge_gap_min_mm'] is None or coupling['edge_gap_min_mm']<.24 or coupling['edge_gap_max_mm']>.46 or coupling['straight_edge_gap_max_mm']>.26 or coupling['missing_peer_layer_mm']>0:errors.append(f'CAN{k}: paired trunk gap outside 0.25 mm straight / 0.46 mm miter-corner limits')
 channels.append({'channel':k,'paths':results,'length_imbalance_mm':round(mismatch,4),'paired_trunk':{key:round(value,4) if isinstance(value,float) else value for key,value in coupling.items()},'reference_gap_samples':sample_points})
sources=[f'hardware/{v}/thor-{v}.kicad_pcb','tools/check_can_routing.py','tools/route_can_pairs.py','hardware/jlcpcb-profile.json']
result={'pass':not errors,'errors':errors,'library_sha256':hashlib.sha256(Path(routing_library.__file__).read_bytes()).hexdigest(),'channels':channels,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sources},'limits':'Length includes nominal 1.6 mm via barrels. Trunk Y15–45 mm: 0.25 mm traces / 0.25 mm gap; header and component fanouts excluded from coupling screen. Return reference sampled under trace centerlines at 0.1 mm, not an EM simulation. Short two-layer routes and the ribbon are NOT controlled 120-ohm impedance. No data-rate or EMC qualification.'}
(R/f'exports/{v}/can-routing-review.json').write_text(json.dumps(result,indent=2)+'\n')
w=93 if n==2 else 177
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -9 {w+10} 83">',f'<rect x="-5" y="-9" width="{w+10}" height="83" fill="#10242e"/>',f'<rect width="{w}" height="65" fill="#183d45" stroke="#b6c2bb" stroke-width=".25"/>']
for f in board.GetFootprints():
 for pad in f.Pads():
  x,y=xy(pad.GetPosition());sx,sy=xy(pad.GetSize());svg.append(f'<rect x="{x-sx/2}" y="{y-sy/2}" width="{sx}" height="{sy}" fill="#768786" opacity=".65"/>')
for s,side,k in drawing:
 a,c=s['a'],s['b'];color='#ffc05c' if side=='H' else '#56dded';dash=' stroke-dasharray=".8 .5"' if s['layer']=='B.Cu' else ''
 svg.append(f'<path d="M{a[0]},{a[1]} L{c[0]},{c[1]}" stroke="{color}" stroke-width=".35" fill="none"{dash}/>')
for channel in channels:
 k=channel['channel'];x=25.5+42*k
 svg.append(f'<text x="{x}" y="-3" text-anchor="middle" fill="#e6e8dd" font-size="2.3" font-family="sans-serif">CAN {k} / Δ {channel["length_imbalance_mm"]:.2f} mm</text>')
 for x,y in channel['reference_gap_samples']:svg.append(f'<circle cx="{x}" cy="{y}" r=".32" fill="#fa698b"/>')
svg.append(f'<text x="{w/2}" y="70" text-anchor="middle" fill="#e6e8dd" font-size="2" font-family="sans-serif">H amber · L cyan · dashed bottom layer · pink ground-reference gaps</text></svg>')
(R/f'exports/{v}/can-routing.svg').write_text('\n'.join(svg))
print(v,'PASS' if not errors else 'FAIL',json.dumps([{'channel':c['channel'],'imbalance':c['length_imbalance_mm'],'gap':c['paired_trunk'],'reference':[p['longest_reference_gap_mm'] for p in c['paths'].values()]} for c in channels]),errors)
if errors:raise SystemExit(1)
