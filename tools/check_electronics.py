#!/usr/bin/env python3
"""Check externally meaningful pin mappings and assembly files, beyond generic ERC."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
from cadagent.pcb import kicad_report,check_jlc_files
R=Path(__file__).resolve().parents[1]
for v,n in [('2port',2),('4port',4)]:
 root=ET.parse(R/f'exports/{v}/netlist.xml').getroot();nodes={}
 for net in root.findall('nets/net'):
  for x in net.findall('node'):nodes[(x.attrib['ref'],x.attrib['pin'])]=net.attrib['name']
 errors=[]
 def same(a,b):
  if nodes.get(a)!=nodes.get(b) or a not in nodes:errors.append(f'Expected connection {a} -> {b}')
 # Independent transcription of P4071 A02 sheet 11, not imported from the builder.
 expected=['HOST_3V3','HOST_5V_AO','FSI_CAN0_H','FSI_CAN0_TERM','FSI_CAN0_L','FSI_EXT_GPIO1','FSI_CAN1_H','FSI_CAN1_TERM','FSI_CAN1_L','GND','AURIX_CAN1_H','AURIX_CAN1_TERM','AURIX_CAN1_L','ESTOP_IN1','AURIX_CAN2_H','AURIX_CAN2_TERM','AURIX_CAN2_L','ESTOP_IN2','ESTOP_OUT1','AURIX_PWM_GPIO','GND','AURIX_SMCU_PGOOD','AURIX_SCL_TXD','AURIX_SMCU_WAKE','AURIX_SDA_RXD','GND']
 for pin,name in enumerate(expected,1):
  if nodes.get(('J1',str(pin)))!='/'+name:errors.append(f'J47 source-map mismatch at J1.{pin}')
 for aux,host in [(3,6),(4,10),(5,14),(6,18),(7,19),(8,20),(9,22),(10,24),(11,23),(12,25),(13,21),(14,26)]:same(('J10',str(aux)),('J1',str(host)))
 same(('JP5','2'),('J10','1'));same(('JP6','2'),('J10','2'))
 same(('J12','1'),('J2','SH'));same(('J12','2'),('J1','10'))
 if len({nodes['J1','1'],nodes['J1','2'],nodes['J10','1'],nodes['J10','2'],nodes['J1','10'],nodes['J2','SH']})!=6:errors.append('Power, ground or shield domains merged across an open link')
 if n==2:
  for pin,host in enumerate([11,12,13,15,16,17],1):same(('J11',str(pin)),('J1',str(host)))
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
 result={'pass':not errors,'errors':errors,'assembly':assemblies,'pins_checked':'All 26 J47 pins against independent source transcription; full AUX and reserved mapping; distinct power/ground/shield domains; DE9 CAN H/L/GND/shield/NC; TVS pin3; host termination tap; open auxiliary power boundaries','physical_tested':False,'source_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in [f'exports/{v}/netlist.xml',f'exports/{v}/erc.json',f'exports/{v}/drc.json','tools/check_electronics.py','hardware/interface.json']}}
 (R/f'exports/{v}/electrical-review.json').write_text(json.dumps(result,indent=2));print(v,result['pass'],errors)
 if errors:raise SystemExit(1)
