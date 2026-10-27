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

Clean-checkout packaging found local `.kicad_prl` UI state in locally generated PCB ZIPs. CI's clean checkout did not contain those files, so the published A0 assets excluded them. Packaging now selects only files in the validated public manifest, and compares local versus clean-checkout package hashes. This changes packaging only; the A0 electrical and mechanical design is unchanged.

## A1 independent design audit

| Round | Finding | Correction and validation |
|---|---|---|
| Routing 1 | General autorouting passed connectivity while H/L wandered apart | Explicit paired trunks and symmetric layer transitions; native pair-geometry measurements |
| Routing 2 | Auxiliary routing interrupted ground below CAN | Bottom routing keepouts allow ground pour; sampled trunk reference has no gaps |
| Routing 3 | Four-port J1 ground sat on isolated front and bottom islands | Added two stitching locations joining the header region to the main plane; native DRC now has zero unconnected items |
| Fabrication | Conservative settings had not been checked against current supplier data | Retrieved dated JLC capabilities; native limits, actual feature metrics and deliberate failing-rule control pass |
| Mechanics | Mirroring the PCB STEP reversed connector handedness | Proper rotation; clamp, port windows, labels and mating references use the corrected frame |
| Identity | Lid was a dense block of text | Shared vector engraving with numbered DE9, leaders, port badges and revision identity |
| Documentation | GitHub prioritized `.github/README.md`; folder indexes lacked guidance | Removed overriding index, guarded against recurrence, and created curated guides at every public content level |

JLCDFM upload reached sign-in without a report. No supplier approval or physical test has occurred. A0 results above describe prior iterations and do not establish current compatibility.

## Prototype access and mounting iteration

| Round | Finding | Correction and validation |
|---|---|---|
| Prototype routing | Router export left one AUX_3V3 branch disconnected; direct detours crossed raw I/O or host 5 V | Explicit layer transition and clearance-preserving route; final native DRC/connectivity/parity all zero |
| Prototype function | Raw net names can imply unsupported GPIO functions | Trace J47 pin 6 to J39 / FSI_GPIO06; cite NVIDIA FSI firmware ownership; retain raw access and label its limit |
| Enclosure supports | Nominal walls hid 1.35 mm seam and 1.8 mm clamp edge webs | Wider clamp and wall, two 3.2 mm ribs with R1.6 roots, recessed M3 side ears with R2 roots |
| Mesh export | Two kerned bold letters overlapped in the new lid label, producing non-manifold STL edges | Reproduced on a flat coupon, then fixed bounded text union in shared cad-agent; regression and full suite pass |
| Final thickness audit | Lid bosses left 1.6 mm around the recessed screw heads | Increase bosses to Ø10.6, measure the 2.1 mm radial web, and rebuild both variants |
| Exploded view | Renderer omitted the six assembly screws | Include four M3×20 and two M3×6 screws at separate exploded heights with all six inserts |
| Publication | Validated A1 remained only on the development branch | Merge PR #1 into main, verify GitHub root README/images, and continue new work on a separate development branch |

| Evidence completeness | Merged cad-agent rejected default-filtered KiCad reports and unexamined disabled checks | Enabled all checks, added four bare-pad courtyards per board, centered a 1 nm termination-track offset and reran all severities with no waivers |

The larger PCB uses a 152.4 mm cable candidate to retain useful external reach after the longer internal run. Physical cable fit, current budget and qualification remain open.

## Four corner mounts — 2026-10-27

The user found the two central side ears too small. Both bases now use four corner mounts with 26 mm ear widths, R4 roots and 34 mm nominal wall attachments. The 7 mm thickness and recessed M3 hardware stay unchanged. Updated checks measure the actual fused root sections and test driver/head/shank clearance at all four locations. Both housings, printable files, rendered views and interactive scenes are regenerated together. Physical strength remains untested.
