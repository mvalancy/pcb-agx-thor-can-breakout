#!/usr/bin/env python3
"""Measure the actual shared-toolkit glyphs, roof edges and counterbore clearances.

This is a CAD layout check, not a minimum glyph-stroke or physical print test.
Native font sizes are em sizes; measured glyph bounds are reported separately.
"""
from pathlib import Path
import hashlib
import json
import math
import sys
import cadquery as cq
import cadagent.markings as library

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'cad'))
from markings import lid_markings

P = json.loads((R / 'cad/parameters.json').read_text())
C, B, style = P['case'], P['pcb'], P['lid_markings']
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check(n):
    w, d = B[f'width_{n}port_mm'], B['depth_mm']
    outer = C['wall_mm'] + C['board_clearance_mm']
    rear = d + C['rear_extension_mm']
    roof = cq.Solid.makeBox(w + 2*outer, rear + 2*outer, .2, cq.Vector(-outer, -outer, 0))
    roof = cq.Workplane(obj=roof).edges('|Z').fillet(C['corner_radius_mm']).val()
    surrounding = cq.Solid.makeBox(w + 2*outer + 20, rear + 2*outer + 20, .2, cq.Vector(-outer-10, -outer-10, 0)).cut(roof)
    bores = [cq.Solid.makeCylinder(C['counterbore_diameter_mm']/2, .2, cq.Vector(x, y, 0))
             for x,y in [(4,4), (w-4,4), (4,d-4), (w-4,d-4)]]
    drawing = lid_markings(n, w, style)
    pieces = []
    for item in drawing.items:
        one = library.PanelMarkings()
        one.items = [item]
        pieces.append(one.solids(0, .2))
    rows, failures = [], []
    for i, (item, shape) in enumerate(zip(drawing.items, pieces)):
        bounds = shape.BoundingBox()
        edge = shape.distance(surrounding)
        bore = min(shape.distance(hole) for hole in bores)
        row = {'item': i, 'kind': item[0], 'roof_edge_clearance_mm': round(edge, 4),
               'counterbore_clearance_mm': round(bore, 4)}
        if shape.cut(roof).Volume() > 1e-7 or min(edge, bore) < style['minimum_text_clearance_mm']-1e-6:
            failures.append(f'item {i}: engraving too close to roof edge/counterbore')
        if item[0] == 'text':
            nearest, index = math.inf, None
            for j, other in enumerate(pieces):
                if i == j:
                    continue
                b = other.BoundingBox()
                lower = math.hypot(max(bounds.xmin-b.xmax, b.xmin-bounds.xmax, 0),
                                   max(bounds.ymin-b.ymax, b.ymin-bounds.ymax, 0))
                if lower >= nearest:
                    continue
                distance = shape.distance(other)
                if distance < nearest:
                    nearest, index = distance, j
            row.update(text=item[1], measured_bounds_mm=[round(x,4) for x in
                       [bounds.xmin, bounds.ymin, bounds.xmax, bounds.ymax]],
                       nearest_item=index, artwork_clearance_mm=round(nearest,4))
            if nearest < style['minimum_text_clearance_mm']-1e-6:
                failures.append(f'item {i}: text touches/approaches another engraving')
        rows.append(row)
    report = {'pass': not failures, 'failures': failures,
              'scope': 'Native DejaVu Sans bold glyph solids and shared vector tools; actual text-to-artwork, roof edge and counterbore distances. Does not establish minimum glyph stroke, slicer survival or printed legibility.',
              'source_sha256': {f:digest(R/f) for f in ['cad/parameters.json','cad/markings.py','tools/check_lid_markings.py']},
              'library_sha256': digest(Path(library.__file__)),
              'minimum_required_clearance_mm': style['minimum_text_clearance_mm'],
              'minimum_text_artwork_clearance_mm': min(r['artwork_clearance_mm'] for r in rows if 'text' in r),
              'minimum_roof_edge_clearance_mm': min(r['roof_edge_clearance_mm'] for r in rows),
              'minimum_counterbore_clearance_mm': min(r['counterbore_clearance_mm'] for r in rows),
              'engraved_roof_remaining_mm': C['lid_mm']-style['engraving_depth_mm'],
              'physical_print_verified': False, 'items': rows}
    (R/f'exports/{n}port/lid-markings-review.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'{n}port: pass={report["pass"]}; text gap={report["minimum_text_artwork_clearance_mm"]} mm; edge={report["minimum_roof_edge_clearance_mm"]} mm; bore={report["minimum_counterbore_clearance_mm"]} mm', flush=True)
    return report['pass']

if __name__ == '__main__':
    results = [check(n) for n in [2,4]]
    raise SystemExit(0 if all(results) else 1)
