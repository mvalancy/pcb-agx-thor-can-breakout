#!/usr/bin/env python3
"""Validate committed evidence, actual meshes and local docs; bind release bytes.
CI verifies artifacts/snapshots; it does not claim to rerun KiCad or physical tests.
"""
from pathlib import Path
import sys,json,hashlib,subprocess,re,zipfile,importlib
from urllib.parse import unquote,urlsplit
import trimesh
from cadagent.pcb import evidence_is_current
import cadagent.pcb_routing as routing_library
from cadagent.mesh3mf import read_3mf,is_edge_manifold,mesh_volume
R=Path(__file__).resolve().parents[1]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def public_files():
 return sorted({p for rel in subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=R,text=True).splitlines() if (p:=R/rel).is_file()})
errors=[]
def require(ok,msg):
 if not ok:errors.append(msg)
for v in ['2port','4port']:
 out=R/'exports'/v
 for name in ['electrical-review','mechanical-checks','assembly-paths','can-routing-review','fabrication-profile-check']:
  data=json.loads((out/f'{name}.json').read_text());require(data.get('pass') is True,f'{v}: {name} failed')
 for name in ['electrical-review','can-routing-review','fabrication-profile-check']:
  data=json.loads((out/f'{name}.json').read_text())
  require(bool(data.get('source_sha256')),v+': missing source hashes '+name)
  for rel,sha in data.get('source_sha256',{}).items():require(digest(R/rel)==sha,rel+': stale '+name)
 route=json.loads((out/'can-routing-review.json').read_text())
 require(route.get('library_sha256')==digest(Path(routing_library.__file__)),v+': routing library changed since measurement')
 paths=json.loads((out/'assembly-paths.json').read_text())
 for rel,sha in {**paths.get('mechanical_sources',{}),**paths.get('artifact_sha256',{})}.items():require(digest(R/rel)==sha,rel+': stale assembly path evidence')
 require('tools/check_mechanics.py' in paths.get('mechanical_sources',{}),v+': missing assembly checker source hash')
 require(bool(paths.get('artifact_sha256')),v+': missing exported assembly hashes')
 mechanics=json.loads((out/'mechanical-checks.json').read_text())
 require(mechanics['native_step_sha256']==digest(out/'pcb.step'),v+': mechanical report uses stale PCB STEP')
 for data in [mechanics,paths]:
  require(bool(data.get('mechanical_library_sha256')),v+': missing geometry-library hashes')
  for name,sha in data.get('mechanical_library_sha256',{}).items():require(digest(Path(importlib.import_module(name).__file__))==sha,v+': geometry helper changed '+name)
 for rel,sha in mechanics['mechanical_sources'].items():require(digest(R/rel)==sha,rel+': stale mechanical evidence')
 evidence=json.loads((out/'pcb-evidence.json').read_text())
 require(evidence.get('pass') is True and evidence_is_current(R,evidence),v+': electrical evidence failing/stale')
 require(evidence.get('production_ready') is False,v+': current prototype must not be marked production ready')
 with zipfile.ZipFile(out/f'thor-{v}-A1-fabrication-REVIEW.zip') as z:
  names=z.namelist()
  for name in names:
   raw=out/'fabrication-review'/name
   require(raw.is_file() and hashlib.sha256(z.read(name)).hexdigest()==digest(raw),v+': fabrication ZIP has stale member '+name)
  for ending in ['F_Cu.gtl','B_Cu.gbl','F_Mask.gts','B_Mask.gbs','Edge_Cuts.gm1','PTH.drl','NPTH.drl']:
   require(any(n.endswith(ending) for n in names),v+': missing fabrication layer '+ending)
geometry=json.loads((R/'exports/geometry-checks.json').read_text())
for name,g in geometry.items():
 require(g.get('cad_valid') and g.get('solid_count')==1 and g.get('watertight'),name+': invalid source geometry report')
 mesh=trimesh.load_mesh(R/f'exports/{name}.stl')
 require(mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0,name+': invalid STL')
 require(mesh.bounds[0,2]>=-.02 and max(mesh.extents)<=256,name+': print orientation/bed limit')
 vertices,faces=read_3mf(R/f'exports/{name}.3mf')
 require(is_edge_manifold(faces),name+': 3MF not manifold')
 require(abs(mesh_volume(vertices,faces)-mesh.volume)/mesh.volume<.001,name+': 3MF/STL volume mismatch')
# The embedded model must represent the exported housing, not an older scene.
params=json.loads((R/'cad/parameters.json').read_text())
for v in ['2port','4port']:
 scene=json.loads((R/f'exports/view/{v}.json').read_text())
 require(len(scene['parts'])==13 and all(p['name'].startswith(v+'_') for p in scene['parts']),v+': mixed/incomplete viewer assembly')
 parts={p['name']:p for p in scene['parts']}
 for name in ['base','lid']:
  part=parts[v+'_'+name];mesh=trimesh.load_mesh(R/'exports/view'/part['file']);printed=trimesh.load_mesh(R/f'exports/{v}_{name}.stl')
  require(abs(mesh.volume-printed.volume)/printed.volume<.001,v+': viewer housing differs from current print '+name)
 ribbon=parts[v+'_ribbon']['bounds_mm'];cx=(ribbon[0]+ribbon[3])/2
 require(abs(cx-(params['pcb']['width_'+v+'_mm']/2+10))<.01,v+': viewer ribbon uses wrong PCB frame')
files=public_files()
for p in files:
 if p.suffix!='.md':continue
 text=p.read_text()
 links=re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text)+re.findall(r'(?:src|href)="([^"]+)"',text)
 for link in links:
  link=link.split(' "')[0].strip('<>');u=urlsplit(link)
  if u.scheme or link.startswith(('#','/')):continue
  target=(p.parent/unquote(u.path)).resolve()
  require(target.exists(),str(p.relative_to(R))+': broken link '+link)
require(not (R/'.github/README.md').exists(),'.github/README.md overrides the intended root README')
for d in {p.parent for p in files if p.parent not in {R,R/'.github'}}:
 require((d/'README.md').is_file(),'Missing folder README '+str(d.relative_to(R)))
manifest=R/'releases/manifest.json'
exclude={'releases/manifest.json','releases/release-notes.md','releases/release-prerelease'}
hashes={p.relative_to(R).as_posix():digest(p) for p in files if p.relative_to(R).as_posix() not in exclude}
if '--record' in sys.argv:
 require(not errors,'Cannot record a failed release validation')
 if not errors:
  manifest.write_text(json.dumps({'schema_version':1,'toolchain':json.loads((R/'references/toolchain.json').read_text()),'revision':'A1','status':'engineering-prerelease','physical_fit_verified':False,'electrical_tested':False,'production_ready':False,'validation_scope':'Committed native reports, current source hashes, mesh/3MF and document checks. No physical qualification.','files':hashes},indent=2)+'\n')
else:
 data=json.loads(manifest.read_text());require(data.get('files')==hashes,'Release snapshot stale: regenerate reports, then validate_release.py --record')
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print(f'PASS: {len(geometry)} printable parts;2 electrical/mechanical variants;{len(hashes)} source/artifact hashes; local docs resolve. Physical qualification pending.')
