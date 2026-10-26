# Iterations and validation evidence

All entries are CAD/software evidence from 2026-10-26. There has been no physical prototype test.

| Round | Finding | Change and recheck |
|---|---|---|
| Electrical1 | KiCad library tables not recognized | Corrected table syntax; ERC passed |
| Electrical2 | All tracks connected, but schematic root-net names and NC nets differed from PCB | Netlist-based naming/NC synchronization, fields and board-only mounts; parity reached zero |
| Electrical3 | Short TVS ground-via trials intersected existing routes | Moved each direct ground via to the free inner side; reran full DRC |
| Electrical4 | Generic DE9 had no approved MPN | Selected AssmannC3127392; audited manufacturer dimensions; updated shell-hole centers/drills and XFCN jumper drill |
| Electrical5 | Exact shell-hole update reduced clearance to redundant bottom ground tracks | Removed redundant ground segments in favor of filled bottom plane; rerun connectivity/parity/DRC |
| Mechanical1 | Early lid/board retention assumptions conflicted | Shared fourM3x25 screws and sleeves stopping at PCB top; checked overlap and penetration |
| Mechanical2 | Board-only proxy insufficient | Imported native KiCad STEP; corrected STEP Z datum; zero nativePCB/plastic collision |
| Mechanical3 | Ribbon needed real load relief | Added rear chamber, separate clamp, captiveM3 nuts, hard stops and silicone pads |
| Mechanical4 | Round clamp supports intruded3.068445mm³ into ribbon envelope | Opened central18.4mm channel; both variants now zero modeled hard-part/ribbon overlap |
| Tooling | Generic progress links did not show drawings in page | Added reusable cad-agent embedded review workbench, source freshness and PCB evidence adapter |

Latest numeric results are in each variant's `erc.json`, `drc.json`, `pcb-evidence.json` and `mechanical-checks.json`, plus `geometry-checks.json`. The final release manifest binds exported artifacts to source hashes. Regenerating geometry or rerouting requires new reports before packaging.

## Wider ports, heat-set hardware and enclosure identity

The 42 mm connector pitch increases the front rib to 9.8 mm and maximum-width A-FT09 hood gap to 7.7 mm. Moving the connector pin row to Y7.5 mm puts the male flange at Y−3.44 beside the case front Y−3.6. The near-flush placement avoids requiring the hood itself to enter the front opening.

The first mesh rebuild failed despite valid one-solid CAD: Ø9.2 mm corner bosses touched inner walls exactly along vertical lines, leaving six non-manifold mesh edges. Increasing those bosses to Ø9.6 mm gives a 0.2 mm overlap. Clamp bosses remain Ø9.2 mm with separate cable clearance. This is a geometry correction, not a mesh repair. Recessed-head axial checks report nominal engagement and bottom clearance; they do not establish allowable torque.

The enlarged lower lid sleeves initially overlapped the base sidewalls by 11.89683 mm³. Lower sleeve radii were reduced to 4.3 mm while retaining the larger upper boss; the groove is cut after all upper supports are fused. Both variants then reported zero unintended intersections for board, native populated PCB, base/lid, clamp, ribbon and screws.

Final review renders read the exported STEP files back before each scene. A direct in-memory repeated text-compound render placed a port legend incorrectly even though the STEP solid coordinates were correct. The readback view preserves the downloadable model's placements and makes the discrepancy visible. The exact underlying triangulation cause is not established; avoid claiming a general CAD kernel defect from this observation.
