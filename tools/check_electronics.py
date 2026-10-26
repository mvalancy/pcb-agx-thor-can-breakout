#!/usr/bin/env python3
"""Check externally meaningful pin mappings and assembly files, beyond generic ERC."""
from pathlib import Path
import json,xml.etree.ElementTree as ET
from cadagent.pcb import kicad_report,check_jlc_files
R=Path(__file__).resolve().parents[1]
for v,n in [('2port',2),('4port',4)]:
 root=ET.parse(R/f'exports/{v}/netlist.xml').getroot();nodes={}
 for net in root.findall('nets/net'):
  for x in net.findall('node'):nodes[(x.attrib['ref'],x.attrib['pin'])]=net.attrib['name']
 errors=[]
 def same(a,b):
  if nodes.get(a)!=nodes.get(b) or a not in nodes:errors.append(f'Expected connection {a} -> {b}')
 for k,(hp,lp,tp) in enumerate([(3,5,4),(7,9,8),(11,13,12),(15,17,16)][:n]):
  j=f'J{k+2}';d=f'D{k+1}';jp=f'JP{k+1}'
  same(('J1',str(hp)),(j,'7'));same(('J1',str(lp)),(j,'2'))
  same((j,'7'),(d,'1'));same((j,'2'),(d,'2'));same((d,'3'),('J1','10'))
  same((j,'3'),('J1','10'));same((j,'6'),('J1','21'));same((j,'5'),(j,'SH'))
  same((jp,'1'),(j,'7'));same((jp,'2'),('J1',str(tp)))
  for pin in ['1','4','8','9']:
   if not nodes.get((j,pin),'').startswith('unconnected-'):errors.append(f'{j}.{pin} must remain isolated')
 for pin,allowed in [('1',{('J1','1'),('JP5','1')}),('2',{('J1','2'),('JP6','1')})]:
  attached={node for node,net in nodes.items() if net==nodes['J1',pin]}
  if attached!=allowed:errors.append(f'Host rail J1.{pin} escapes open-link boundary: {attached}')
 for kind in ['erc','drc']:
  if not kicad_report(R/f'exports/{v}/{kind}.json',kind)['pass']:errors.append(kind+' not clean')
 assemblies={name:check_jlc_files(R/f'exports/{v}/{prefix}bom.csv',R/f'exports/{v}/{prefix}cpl.csv') for name,prefix in [('smt','jlc-'),('full','jlc-full-')]}
 if not all(r['pass'] for r in assemblies.values()):errors.append('Assembly file check failed')
 result={'pass':not errors,'errors':errors,'assembly':assemblies,'pins_checked':'DE9 CAN H/L/GND/shield/NC; TVS pin3; host termination tap; open auxiliary power boundaries','physical_tested':False}
 (R/f'exports/{v}/electrical-review.json').write_text(json.dumps(result,indent=2));print(v,result['pass'],errors)
 if errors:raise SystemExit(1)
