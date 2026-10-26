# Verify exact footprints and real cable clearance after every design substitution

2026-10-26 command evidence (private paths omitted): `kicad-cli pcb drc --format json --schematic-parity` initially reported0 unconnected items but100/131 parity warnings. Native netlist synchronization resolved root-net names, NC nets, footprint fields and board-only mounts. Exact Assmann shell-hole positions then produced0.1841/0.1959mm clearances against a0.2mm rule; removing redundant bottom ground tracks and refilling the plane required another complete check. One pad then had only one thermal spoke; that ground pad was changed to a deliberate solid-plane connection; no DRC exclusion was used.

`python cad/build.py` found3.068445mm³ ribbon/support overlap in the first clamp. Opening an18.4mm central channel brought both variants' modeled ribbon/hard-part overlap to0. Native PCB, base/lid, clamp and nut collision checks also returned0. These results are CAD-only; cable pull, creepage, electrical transient and printed fit claims remain untested.

Cause: generic connector geometry and a round support envelope were treated too optimistically. Corrective rule: inspect exact manufacturer datums, check component and cable volumes, then rerun all affected electrical/mechanical checks after changes.

KiCad10 legacy SWIG note: mutating/removing board objects then loading a second board in the same interpreter produced `SwigPyObject`/ownership errors. `tools/finalize_board.py` now isolates each variant in its own process. Limits: this is an observed workaround, not a general diagnosis of every KiCad version. FreeRouting2.5 native failed to serialize component outlines in this environment; FreeRouting1.9 under Xvfb with single-thread optimization produced usable SES output. Pin tool versions and rerun native KiCad validation after importing routes.

Regression/evidence harness: `tools/check_electronics.py`, `cad/build.py`, cad-agent's `tests/test_pcb.py`, `tests/test_site.py` and `tests/test_review.py`. Vendor PDFs remain outside version control.
