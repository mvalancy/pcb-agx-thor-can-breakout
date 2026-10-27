#!/usr/bin/env python3
"""Validate shared cad-agent lid slicing and draw actual first-layer toolpaths.

No printer connection or print submission. G-code and vendor presets stay outside
the public snapshot; only compact source-bound results and a toolpath SVG are public.
Run `cad-agent slice` first; cad-agent.yaml limits this project to the two lids.
"""
from pathlib import Path
import hashlib
import json
import re
import zipfile
import cadagent.slicer as slicer
from cadagent.project import load_project

R = Path(__file__).resolve().parents[1]
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def first_layers(gcode, target):
    """Draw actual extruding XY segments, from the bed-facing reading side."""
    paths = {1:[], 2:[]}
    x=y=e=0.;relative_e=False;layer=0;width=.5
    for raw in gcode.splitlines():
        if raw.startswith('; CHANGE_LAYER'):
            layer += 1
            if layer > 2: break
        if raw.startswith('; LINE_WIDTH:'):
            width=float(raw.split(':')[1])
        line=raw.split(';')[0].strip()
        if not line: continue
        op=line.split()[0]
        if layer and op=='G91':raise RuntimeError('Relative XY motion is unsupported in the toolpath proof')
        values={k:float(v) for k,v in re.findall(r'([XYE])([-+\d.]+)',line)}
        if op=='M83':relative_e=True
        if op=='M82':relative_e=False
        if op=='G92':
            x=values.get('X',x);y=values.get('Y',y);e=values.get('E',e)
        if op not in ['G0','G1','G2','G3']: continue
        xx,yy=values.get('X',x),values.get('Y',y)
        delta=values.get('E',0) if relative_e else values.get('E',e)-e
        if layer in paths and delta>0 and (xx!=x or yy!=y):
            if op not in ['G0','G1']:raise RuntimeError('Arc found in proof; require enable_arc_fitting=0')
            paths[layer].append((x,y,xx,yy,width))
        x,y=xx,yy
        if 'E' in values:e=e+values['E'] if relative_e else values['E']
    assert all(paths.values()), 'Missing first/second layer extrusion'
    pts=paths[1];xmin=min(min(p[0],p[2]) for p in pts);xmax=max(max(p[0],p[2]) for p in pts)
    ymin=min(min(p[1],p[3]) for p in pts);ymax=max(max(p[1],p[3]) for p in pts)
    width,height=xmax-xmin,ymax-ymin
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width+12:.3f} {height+24:.3f}" role="img" aria-label="Sliced lid first layer, viewed from its outside reading face">',
         '<rect width="100%" height="100%" fill="#edf2f5"/>',
         '<text x="6" y="6" font-family="sans-serif" font-size="2.6" fill="#203f4b">LID FIRST LAYER · 0.4 mm nozzle · 0.2 mm layer</text>',
         '<text x="6" y="10" font-family="sans-serif" font-size="2.3" fill="#203f4b">Outside reading face / roof-down · actual extrusion paths</text>',
         f'<g transform="translate({6-xmin:.4f},{14-ymin:.4f})" stroke="#234551" stroke-linecap="round" fill="none">']
    # Group by actual width to keep the SVG compact; no invented letter outlines.
    groups={}
    for a,b,c,d,w in pts:groups.setdefault(round(w,4),[]).append(f'M{a:.3f},{b:.3f}L{c:.3f},{d:.3f}')
    svg.extend(f'<path stroke-width="{w}" d="{"".join(p)}"/>' for w,p in groups.items())
    svg += ['</g>',f'<text x="6" y="{height+21:.3f}" font-family="sans-serif" font-size="2.3" fill="#203f4b">Toolpath evidence only · physical print and legibility test pending</text>','</svg>']
    target.write_text('\n'.join(svg)+'\n')
    return {f'layer_{k}_extruding_segments':len(v) for k,v in paths.items()}

def run():
    project=load_project(R)
    shared=slicer.current_report(project)
    assert shared and shared['pass'], 'Run cad-agent slice for current 3MF files/settings first'
    for v in ['2port','4port']:
        work=R/f'build/slicer/{v}_lid'
        out=work/'out'
        summary=json.loads((work/'result-summary.json').read_text())
        result=json.loads((out/'result.json').read_text())
        assert summary['exit_code']==0 and result['return_code']==0, (v,summary)
        with zipfile.ZipFile(out/'sliced.3mf') as z:
            settings_bytes=z.read('Metadata/project_settings.config')
            effective=json.loads(settings_bytes)
        expected={'printer_model':'Bambu Lab P1S','nozzle_diameter':['0.4'],'filament_type':['PETG'],
                  'layer_height':'0.2','initial_layer_print_height':'0.2','wall_loops':'4','sparse_infill_density':'30%',
                  'printable_area':['0x0','256x0','256x256','0x256'],'curr_bed_type':'Textured PEI Plate','enable_arc_fitting':'0'}
        for k,value in expected.items():assert effective.get(k)==value, (k,effective.get(k))
        assert float(effective['filament_density'][0])>1 and float(effective['nozzle_temperature'][0])>=230
        gcode=(out/'plate_1.gcode').read_text()
        proof=R/f'preview/{v}-lid-first-layer.svg'
        segment_counts=first_layers(gcode,proof)
        version=re.search(r'; BambuStudio (\S+)',gcode).group(1)
        layers=int(re.search(r'; total layer number: (\d+)',gcode).group(1))
        report={'pass':True,'scope':'Offline lid-only slicing by shared cad-agent; first two engraved layers contain extrusion paths. Does not certify every glyph, print adhesion, surface finish, other housing parts or physical readability.',
                'slicer':'BambuStudio '+version,'profile':expected,
                'profile_names':{k:shared[k] for k in ['printer','process','filament']},
                'source_sha256':{f:sha(R/f) for f in ['tools/check_lid_slicing.py','cad-agent.yaml']},
                'library_sha256':sha(Path(slicer.__file__)),
                'artifact_sha256':{f:sha(R/f) for f in [f'exports/{v}_lid.3mf',f'exports/{v}_lid.stl',str(proof.relative_to(R)),'exports/slice-report.json']},
                'gcode_sha256':sha(out/'plate_1.gcode'),'resolved_settings_sha256':hashlib.sha256(settings_bytes).hexdigest(),
                'return_code':result['return_code'],'layers':layers,**segment_counts,
                'warnings':result['sliced_plates'][0].get('warnings',[]),'physical_print_verified':False,'printer_submission':False}
        (R/f'exports/{v}/lid-slicing-review.json').write_text(json.dumps(report,indent=2)+'\n')
        print(v,'PASS',version,layers,'layers',segment_counts,flush=True)

if __name__=='__main__':
    run()
