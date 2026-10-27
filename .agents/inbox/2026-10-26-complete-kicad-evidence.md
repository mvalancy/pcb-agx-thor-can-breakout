# Run every KiCad severity and enable default-disabled checks before accepting a clean report

2026-10-26: upstream cad-agent review required `included_severities` to include error, warning and exclusion, and made ignored checks explicit. The old default command reported only error/warning. Inspecting both report JSONs found four default-disabled ERC checks and five default-disabled DRC checks. This was a completeness gap in the earlier zero-finding result.

Command evidence: `kicad-cli pcb drc --format json --schematic-parity --severity-all` after setting the default-disabled keys to warning found four missing courtyards on each board (P1/P2/TP1/TP2), plus one two-port termination-track endpoint displaced 0.000001 mm from its via. Native readback showed X33.325 versus X33.324999 mm on the same FSI_CAN1_TERM net. ERC found zero violations with every check enabled.

Correction: add native courtyard outlines to the bare-pad footprints and center the same-net endpoint on its via. The finalizer only snaps offsets within 10 nm; larger offsets require review. Apply all check severities explicitly in `apply_fab_rules.py` and export ERC/DRC with `--severity-all`. Both boards require no ignored checks, excluded findings or waivers. Pin the merged toolkit, rather than continuing to rely on a superseded branch's permissive checker.

Limits: these are CAD completeness and quantization corrections, not physical qualification. Courtyard graphics and the 1 nm copper endpoint do not change the solid PCB/component model. Fresh KiCad STEP exports changed presentation ordering and timestamps, but importing each old/new STEP and exporting CadQuery BREP produced byte-identical BREP files for both variants. The previous verified STEP bytes were retained only after that equality check. Any solid-geometry difference requires renewed mechanical review.

Final command/output: `tools/export_review.py` followed by the merged `tools/update_evidence.py` reports both bundles passing, zero errors/warnings/unconnected/parity/exclusions and no ignored checks or waivers. The merged toolkit evidence, marking and fastener tests report `22 passed`.
