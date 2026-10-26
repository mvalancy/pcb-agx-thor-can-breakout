#!/usr/bin/env python3
"""Generate both native KiCad review projects from the interface authority.
Run with KiCad's Python interpreter (pcbnew), not the mechanical venv.
"""
from pathlib import Path
import json, uuid, os, shutil, math, csv, sys
import pcbnew as pcb
ROOT=Path(__file__).resolve().parents[1]
LIB=Path(os.environ.get('KICAD_FOOTPRINT_DIR',str(Path.home()/'.local/share/kicad-10.0.1/share/kicad/footprints')))
P=json.loads((ROOT/'cad/parameters.json').read_text()); I=json.loads((ROOT/'hardware/interface.json').read_text())
UUID=lambda s:str(uuid.uuid5(uuid.NAMESPACE_URL,'thor-breakout/'+s))
q=lambda s:json.dumps(str(s))
mm=pcb.FromMM
vec=lambda x,y:pcb.VECTOR2I(mm(x),mm(y))
FPDIR=ROOT/'hardware/Thor.pretty'; FPDIR.mkdir(exist_ok=True)
# Original footprint, dimensions from Samtec SHF manufacturer layout rev A.
shf='Samtec_SHF-113-01-L-D-SM'
s=[f'(footprint "{shf}" (version 20241229) (generator "pcbnew") (layer "F.Cu") (attr smd)',
 '(descr "Samtec SHF 26 way: manufacturer footprint rev A, no LC. Prototype substitute for Wieson; mating untested.")',
 '(property "Reference" "REF**" (at 0 -4.3 0) (layer "F.SilkS") (effects (font (size 1 1)(thickness 0.15))))',
 f'(property "Value" "{shf}" (at 0 4.5 0) (layer "F.Fab") (effects (font (size 1 1)(thickness 0.15))))']
for layer,dx,dy in [('F.Fab',11.43,2.54),('F.CrtYd',11.93,3.93)]:
 s.append(f'(fp_rect (start {-dx} {-dy})(end {dx} {dy})(stroke (width 0.05)(type default))(fill none)(layer "{layer}"))')
s.append('(fp_line(start -11.4 2.8)(end -9.3 2.8)(stroke(width 0.2)(type default))(layer "F.SilkS"))')
for n in range(1,27):
 x=((n-1)//2-6)*1.27;y=2.16 if n%2 else -2.16
 s.append(f'(pad "{n}" smd rect (at {x} {y})(size 0.74 2.54)(layers "F.Cu" "F.Paste" "F.Mask"))')
s.append(')');(FPDIR/f'{shf}.kicad_mod').write_text('\n'.join(s))
FP={
 'header':f'Thor:{shf}',
 'de9':'Connector_Dsub:DSUB-9_Pins_Horizontal_P2.77x2.84mm_EdgePinOffset7.70mm_Housed_MountingHolesOffset9.12mm',
 'tvs':'Package_TO_SOT_SMD:SOT-23',
 'jumper':'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
 'aux':'Connector_PinHeader_2.54mm:PinHeader_2x07_P2.54mm_Vertical',
 'extra':'Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical',
 'mount':'MountingHole:MountingHole_3.2mm_M3',
}
# Vendor standard footprints locally so projects open without global-library setup.
for key,fid in list(FP.items()):
 if key=='header':continue
 lib,name=fid.split(':'); shutil.copy2(LIB/(lib+'.pretty')/(name+'.kicad_mod'),FPDIR/(name+'.kicad_mod')); FP[key]='Thor:'+name

# Part-specific derivatives retain KiCad library attribution (see THIRD_PARTY.md).
source=FPDIR/(FP['de9'].split(':')[1]+'.kicad_mod')
target='Assmann_A-DS_09_A-KG-T2S'
f=pcb.FootprintLoad(str(FPDIR),source.stem);f.SetFPID(pcb.LIB_ID('Thor',target));f.SetValue(target)
f.SetLibDescription('Assmann ASS 4888 CO rev10 male9; face datum10.94; SH nominal chainY1.44, drill3.05. Generic KiCad 3D model, physical fit pending.')
for pad in f.Pads():
 if pad.GetNumber()=='SH':
  pos=pad.GetPosition();x=-6.955 if pcb.ToMM(pos.x)<0 else 18.035
  pad.SetPosition(vec(x,1.44));pad.SetDrillSize(vec(3.05,3.05))
# Shorten off-board silk for the near-flush front placement; body stays on F.Fab.
for graphic in f.GraphicalItems():
 if graphic.GetLayer()==pcb.F_SilkS and isinstance(graphic,pcb.PCB_SHAPE):
  for getter,setter in [(graphic.GetStart,graphic.SetStart),(graphic.GetEnd,graphic.SetEnd)]:
   point=getter()
   if pcb.ToMM(point.y)>7.2:setter(vec(pcb.ToMM(point.x),7.2))
pcb.FootprintSave(str(FPDIR),f);FP['de9']='Thor:'+target
f=pcb.FootprintLoad(str(FPDIR),FP['jumper'].split(':')[1]);target='XFCN_PZ254V-11-02P';f.SetFPID(pcb.LIB_ID('Thor',target));f.SetValue(target);f.SetLibDescription('XFCN PZ254V-11-02P C492401 manufacturer recommended drill1.02; KiCad standard header geometry')
for pad in f.Pads():pad.SetDrillSize(vec(1.02,1.02))
pcb.FootprintSave(str(FPDIR),f);FP['jumper']='Thor:'+target

# Exact carrier J47 lands from the reviewed native NVIDIA ODB/ASCII measurement authority.
M=json.loads((ROOT/'research/j47-footprint-measurements.json').read_text())
wieson='Wieson_AC2800-0011-022-H0'
lines=[f'(footprint "{wieson}" (version 20241229) (generator "pcbnew") (layer "F.Cu") (attr smd)',
 '(descr "Wieson J47 P4071A02 ODB/ASCII lands; source-normalized top view. Current drawing, height and mating unverified.")',
 '(property "Reference" "REF**" (at 0 -4.8)(layer "F.SilkS")(effects(font(size 0.8 0.8)(thickness 0.12))))',
 f'(property "Value" "{wieson}" (at 0 5.6)(layer "F.Fab")(effects(font(size 1 1)(thickness 0.15))))']
for key,layer,width,style in [('nominal_wieson_body_outline','F.Fab',.1,'default'),('cap_outline','F.Fab',.05,'dash'),('source_pin1_silk_triangle','F.SilkS',.15,'default')]:
 pts=M[key]['closed_polygon']
 for start,end in zip(pts,pts[1:]):lines.append(f'(fp_line(start {start[0]} {start[1]})(end {end[0]} {end[1]})(stroke(width {width})(type {style}))(layer "{layer}"))')
bounds=M['source_dfa_envelope']['bounds']
lines.append(f'(fp_rect(start {bounds["xmin"]-.5} {bounds["ymin"]-.5})(end {bounds["xmax"]+.5} {bounds["ymax"]+.5})(stroke(width 0.05)(type default))(fill none)(layer "F.CrtYd"))')
for pad in M['land_pattern']['pads']:
 n=pad['pin'];x,y=pad['at'];sx,sy=M['land_pattern']['copper_size'];mask=M['land_pattern']['mask_expansion_per_edge']
 lines.append(f'(pad "{n}" smd rect(at {x} {y})(size {sx} {sy})(layers "F.Cu" "F.Paste" "F.Mask")(solder_mask_margin {mask}))')
lines.append(')');(FPDIR/f'{wieson}.kicad_mod').write_text('\n'.join(lines));FP['header']='Thor:'+wieson

def symbol_def(name,pins):
 # Original passive functional symbols: pin names establish exact mapping, not MCU functions.
 n=len(pins); h=(math.ceil(n/2)+1)*2.54
 out=[f'(symbol "Thor:{name}" (pin_names(offset 1.0) hide) (in_bom yes)(on_board yes)',
 f'(property "Reference" "J" (at 0 {h/2+2.54} 0)(effects(font(size 1.27 1.27))))',
 f'(property "Value" "{name}" (at 0 {-h/2-2.54} 0)(effects(font(size 1.27 1.27))))',
 f'(symbol "{name}_0_1" (rectangle(start -12.7 {h/2})(end 12.7 {-h/2})(stroke(width 0.254)(type default))(fill(type background))))',f'(symbol "{name}_1_1"']
 positions={}
 for j,(num,label) in enumerate(pins):
  side=j%2; row=j//2; y=h/2-2.54*(row+1); x=17.78 if side else -17.78; a=180 if side else 0
  out.append(f'(pin passive line(at {x} {y} {a})(length 5.08)(name {q(label)}(effects(font(size 1 1))))(number {q(num)}(effects(font(size 1 1)))))')
  positions[str(num)]=(x,-y,side)
 out+=['))'];return '\n'.join(out),positions,h

def build(variant):
 n=I['variants'][variant]['channels'];w=P['pcb'][f'width_{variant}_mm'];d=P['pcb']['depth_mm']
 out=ROOT/'hardware'/variant;out.mkdir(exist_ok=True);base=out/f'thor-{variant}'
 parts=[]
 def add(ref,value,kind,nets,x,y,a=0,mpn='',lcsc='',dnp=False):
  parts.append(dict(ref=ref,value=value,kind=kind,nets={str(k):v for k,v in nets.items()},x=x,y=y,a=a,mpn=mpn,lcsc=lcsc,dnp=dnp,uuid=UUID(variant+'/'+ref),footprint=FP[kind]))
 add('J1','THOR J47 / Wieson','header',I['pins'],w/2-10,52,mpn=I['header']['design_mpn'])
 add('J10','AUX / RAW IO','aux',I['aux_header'],w-16,39,mpn='BOOMELE 2.54-2x7P male C71397',lcsc='C71397')
 for k,c in enumerate(I['channels'][:n]):
  cx=P['pcb']['first_port_x_mm']+k*P['pcb']['port_pitch_mm']; prefix=c['id']; h,t,l=c['pins']
  nets={pin: (prefix+'_H' if net=='CAN_H' else prefix+'_L' if net=='CAN_L' else net) for pin,net in I['de9'].items()}
  add('J'+str(k+2),prefix+' / CAN','de9',nets,cx+5.54,P['pcb']['port_pin_y_mm'],180,mpn='A-DS 09 A/KG-T2S',lcsc='C3127392')
  add('D'+str(k+1),'CDSOT23-SM712','tvs',{'1':prefix+'_H','2':prefix+'_L','3':'GND'},cx,17.5,mpn=I['protection']['mpn'],lcsc=I['protection']['lcsc'])
  add('JP'+str(k+1),'120R HOST TERM / OPEN','jumper',{'1':prefix+'_H','2':prefix+'_TERM'},cx,27,mpn='PZ254V-11-02P',lcsc='C492401')
 if n==2:
  add('J11','RESERVED CAN / RAW','extra',{str(k+1):I['pins'][str(p)] for k,p in enumerate([11,12,13,15,16,17])},13,40,mpn='BOOMELE 2.54-2x3P male C65114',lcsc='C65114')
 add('JP5','3V3 AUX ENABLE / OPEN','jumper',{'1':'HOST_3V3','2':'AUX_3V3'},w/2+7,51,mpn='PZ254V-11-02P',lcsc='C492401')
 add('JP6','5V AUX ENABLE / OPEN','jumper',{'1':'HOST_5V_AO','2':'AUX_5V_AO'},w/2+13,51,mpn='PZ254V-11-02P',lcsc='C492401')
 add('J12','SHIELD / GND / OPEN','jumper',{'1':'SHIELD','2':'GND'},w-10,26,mpn='PZ254V-11-02P',lcsc='C492401')
 for k,(x,y) in enumerate([(4,4),(w-4,4),(4,d-4),(w-4,d-4)]):add('H'+str(k+1),'M3','mount',{},x,y)
 # Schematic: labels and short explicit wires make every net readable and testable.
 defs={};positions={};heights={}
 for part in parts:
  if part['kind']=='mount':continue
  name=part['ref']+'_function'; pins=[(p,(net or 'NC')) for p,net in part['nets'].items()]
  defs[name],positions[name],heights[name]=symbol_def(name,pins);part['symbol']=name
 schid=UUID(variant+'/schematic');lib='\n'.join(defs.values())
 sch=[f'(kicad_sch(version 20250114)(generator "eeschema")(uuid {schid})(paper "A3")',
 f'(title_block(title "Thor CAN breakout - {n} ports")(rev "A0 REVIEW")(comment 1 "Not released: prototype mating, sourcing and bench qualification pending")(comment 2 "J47 bus-side signals; passive TVS protection, no galvanic isolation"))',f'(lib_symbols {lib})']
 schpos={'J1':(62.23,66.04),'J10':(62.23,139.7),'J11':(62.23,208.28),'JP5':(62.23,248.92),'JP6':(149.86,248.92),'J12':(243.84,248.92)}
 for k in range(n):
  x=170.18+(k%2)*127;y=55.88+(k//2)*91.44
  schpos['J'+str(k+2)]=(x,y);schpos['D'+str(k+1)]=(x,y+38.1);schpos['JP'+str(k+1)]=(x+55.88,y+53.34)
 for part in parts:
  if part['kind']=='mount':continue
  ref=part['ref'];name=part['symbol'];x,y=schpos[ref];hh=heights[name]
  sch.append(f'(symbol(lib_id "Thor:{name}")(at {x} {y} 0)(unit 1)(in_bom yes)(on_board yes)(dnp no)(uuid {part["uuid"]})')
  for prop,val,py,hide in [('Reference',ref,y-hh/2-2.54,False),('Value',part['value'],y+hh/2+2.54,False),('Footprint',part['footprint'],y,True),('MPN',part['mpn'],y,True),('LCSC',part['lcsc'],y,True)]:
   sch.append(f'(property {q(prop)} {q(val)}(at {x} {py} 0)(effects(font(size 1 1))'+('(hide yes)' if hide else '')+'))')
  for pin in part['nets']: sch.append(f'(pin {q(pin)}(uuid {UUID(variant+ref+pin)}))')
  sch.append(f'(instances(project "thor-{variant}"(path "/{schid}"(reference {q(ref)})(unit 1)))))')
  for pin,net in part['nets'].items():
   dx,dy,side=positions[name][pin];px=x+dx;py=y+dy;end=px+(7.62 if side else -7.62)
   if net is None:sch.append(f'(no_connect(at {px} {py})(uuid {UUID(variant+ref+pin+"NC")}))');continue
   sch.append(f'(wire(pts(xy {px} {py})(xy {end} {py}))(stroke(width 0)(type default))(uuid {UUID(variant+ref+pin+"wire")}))')
   # labels point away from symbol: justify right on left-side wires.
   sch.append(f'(label {q(net)}(at {end} {py} 0)(effects(font(size 1 1))(justify {"left" if side else "right"} bottom))(uuid {UUID(variant+ref+pin+"label")}))')
 for text,y in [('Termination: fit shunt only at a bus endpoint; JP connects CAN_H to host TERM (internal 120R).',270),('DE9: 2=L, 7=H, 3/6=GND, 5/shell=SHIELD; 1/4/8/9 open. No power on pin 9.',274),('AUX power links ship open. AUX is unbuffered: not 24V tolerant. Reserved pins require carrier-specific verification.',278)]:
  sch.append(f'(text {q(text)}(at 18 {y} 0)(effects(font(size 1.2 1.2))(justify left))(uuid {UUID(variant+text)}))')
 sch.append(')');base.with_suffix('.kicad_sch').write_text('\n'.join(sch))
 # Project-local symbol library matching the embedded instances.
 (out/'Thor.kicad_sym').write_text('(kicad_symbol_lib(version 20241209)(generator "kicad_symbol_editor")\n'+lib.replace('symbol "Thor:','symbol "')+'\n)')
 (out/'sym-lib-table').write_text('(sym_lib_table\n (version 7)\n (lib (name "Thor")(type "KiCad")(uri "${KIPRJMOD}/Thor.kicad_sym")(options "")(descr "Project functional symbols")))\n')
 (out/'fp-lib-table').write_text('(fp_lib_table\n (version 7)\n (lib (name "Thor")(type "KiCad")(uri "${KIPRJMOD}/../Thor.pretty")(options "")(descr "Pinned footprints")))\n')
 pro={'meta':{'filename':base.name+'.kicad_pro','version':1},'board':{'design_settings':{'rules':{'min_clearance':0.2,'min_track_width':0.2,'min_via_diameter':0.6,'min_through_hole_diameter':0.3,'min_hole_clearance':0.25,'min_copper_edge_clearance':0.3,'min_silk_clearance':0.15},'rule_severities':{}}},'net_settings':{'classes':[{'name':'Default','clearance':0.2,'track_width':0.25,'via_diameter':0.6,'via_drill':0.3,'diff_pair_width':0.25,'diff_pair_gap':0.2}], 'meta':{'version':3}},'schematic':{'legacy_lib_dir':'','legacy_lib_list':[]}}
 base.with_suffix('.kicad_pro').write_text(json.dumps(pro,indent=2))
 base.with_suffix('.kicad_dru').write_text('(version 1)\n(rule "Conservative JLCPCB prototype" (constraint clearance (min 0.2mm)) (constraint track_width (min 0.2mm)) (constraint hole_size (min 0.3mm)))\n')
 if '--schematic-only' in sys.argv:
  exp=ROOT/'exports'/variant
  (exp/'components.json').write_text(json.dumps(parts,indent=2))
  return
 b=pcb.BOARD();b.SetFileName(str(base.with_suffix('.kicad_pcb')));b.SetCopperLayerCount(2);b.GetDesignSettings().SetBoardThickness(mm(1.6))
 netmap={}
 for net in sorted({v for part in parts for v in part['nets'].values() if v}):
  netmap[net]=pcb.NETINFO_ITEM(b,net,len(netmap)+1);b.Add(netmap[net])
 for part in parts:
  fid=part['footprint'];fname=fid.split(':')[1];f=pcb.FootprintLoad(str(FPDIR),fname);f.SetReference(part['ref']);f.SetValue(part['value']);f.SetFPID(pcb.LIB_ID('Thor',fname));f.SetPath(pcb.KIID_PATH('/'+schid+'/'+part['uuid']))
  f.SetPosition(vec(part['x'],part['y']));f.SetOrientationDegrees(part['a']);b.Add(f)
  f.Reference().SetTextSize(vec(0.8,0.8));f.Reference().SetTextThickness(mm(0.12));f.Value().SetVisible(False)
  for p in f.Pads():
   net=part['nets'].get(p.GetNumber());
   if net:p.SetNet(netmap[net])
  if part['kind']=='mount':f.Reference().SetVisible(False);f.SetAttributes(f.GetAttributes()|pcb.FP_EXCLUDE_FROM_BOM|pcb.FP_EXCLUDE_FROM_POS_FILES)
 for a,z in [((0,0),(w,0)),((w,0),(w,d)),((w,d),(0,d)),((0,d),(0,0))]:
  e=pcb.PCB_SHAPE();e.SetShape(pcb.SHAPE_T_SEGMENT);e.SetStart(vec(*a));e.SetEnd(vec(*z));e.SetLayer(pcb.Edge_Cuts);e.SetWidth(mm(.05));b.Add(e)
 def label(txt,x,y,size=1):
  t=pcb.PCB_TEXT(b);t.SetText(txt);t.SetPosition(vec(x,y));t.SetTextSize(vec(size,size));t.SetTextThickness(mm(.15));t.SetLayer(pcb.F_SilkS);b.Add(t)
 label(f'THOR CAN {n} / A0 REVIEW',w/2,61)
 label('PIN 9: NC / NOT RS232',w/2,33,0.9)
 for k,c in enumerate(I['channels'][:n]):
  cx=P['pcb']['first_port_x_mm']+k*P['pcb']['port_pitch_mm'];label(c['id'],cx,21,0.9);label('TERM=SHUNT',cx,31,0.8)
 label('AUX RAW',w-15,36,.8);label('1',w/2-19,56,.8)
 pcb.SaveBoard(str(base.with_suffix('.kicad_pcb')),b)
 # Reload settings from the native project before exporting router constraints.
 b=pcb.LoadBoard(str(base.with_suffix('.kicad_pcb')))
 exp=ROOT/'exports'/variant;exp.mkdir(exist_ok=True)
 pcb.ExportSpecctraDSN(b,str(exp/'unrouted.dsn'))
 (exp/'components.json').write_text(json.dumps(parts,indent=2))
 with (exp/'bom-review.csv').open('w') as f:
  writer=csv.writer(f);writer.writerow(['Designator','Comment','Footprint','Manufacturer Part','LCSC Part #','Assembly','Status'])
  for p in parts:
   if p['kind']=='mount':continue
   writer.writerow([p['ref'],p['value'],p['footprint'],p['mpn'],p['lcsc'],'SMT' if p['kind'] in ('header','tvs') else 'THT','Supplier approval pending' if not p['lcsc'] else 'Exact manufacturer; availability recheck'])
 print(variant,len(parts),'footprints',len(netmap),'nets')
for v in I['variants']:build(v)
