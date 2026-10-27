# Check engraving at nozzle scale, not only in a paint-filled render

## Evidence — 2026-10-27

The earlier lid used 1.9–2.25 mm body font sizes, 2.2 mm pin numbers and 0.45 mm leaders/rings. The enlarged layout uses bold 4 mm body size, 4.2 mm pin numbers, 5.2 mm badges and 1 mm graphic strokes. Font sizes are em sizes, not minimum strokes or actual capital heights.

`.venv/bin/python tools/check_lid_markings.py` measured native shared-toolkit solids:

```text
2port: pass=True; text gap=0.6055 mm; edge=6.1127 mm; bore=2.1523 mm
4port: pass=True; text gap=0.6055 mm; edge=6.4 mm; bore=2.1523 mm
```

`cad-agent slice` followed by `check_lid_slicing.py` generated 85 layers and first-layer/second-layer extrusion proofs using Bambu Studio 02.08.04.57, P1S 0.4 mm nozzle, PETG, 0.2 mm layers, four walls and 30% infill. No printer was contacted. The committed per-variant reports bind the checker, exported STL and toolpath SVG.

During setup, loading unexpanded installed preset JSON returned a successful slice but used default values: the output had filament density zero and omitted the inherited printer area. The existing `cadagent.slicer` already resolves the inherited profiles, so the final integration uses that shared workflow. Effective output checks confirm the 256 mm bed, PETG density 1.27 and 255 °C nozzle setting instead of trusting the preset filename. Bambu's option is `enable_arc_fitting`, not `arc_fitting`; the proof parser rejects unsupported arcs rather than drawing chords silently.

## Cause

High-resolution artwork and optional contrasting paint make small cosmetic features look easier to print than they are. Enlarging text without reorganizing the layout can instead merge characters into the diagram or counterbores. A slicer exit code alone does not prove that intended inherited settings were applied.

## Corrective rule

Search the existing shared toolkit before writing a new slicer driver; reuse `cadagent.slicer` and its standard report. Use shared `PanelMarkings` for one source of engraving, proof and paint geometry. Increase both font size and graphic width, then measure real glyph bounds and clearances. Keep engraving depth tied to the roof-web calculation. Review exported solids, meshes and actual first-layer paths with verified effective nozzle/material/layer settings. Record reports in the local review page and bind their source/artifact hashes in release validation.

## Limits

The 1 mm width applies to graphic strokes, not every font stem. Spacing checks exclude within-glyph counters. Slicing covers the lids only, and does not certify letter-island adhesion, finish, physical legibility, other parts, insert strength or complete housing qualification. A physical sample remains required.
