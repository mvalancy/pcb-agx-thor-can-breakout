# Release checklist

**Current designation: A0 engineering pre-release, not production ready.** Source code and design exports can be published now. Ordering the 50-unit run requires the evidence below.

| Gate | Current evidence | Required closure |
|---|---|---|
| AGX interface | A02 original schematic/BOM inspected; J47 map recorded | Confirm actual carrier revision/population |
| Exact requested header | Wieson MPN and native26pad layout cross-checked; defaultJ1 updated | Current Wieson drawing/procurement and physical key/height/pin1 proof |
| Ribbon cable | Exact orderable candidate and manufacturer family data | All26 pin continuity, fit, route and strain test on sample |
| Four-port/IGX | Generic A02 extra channels; IGX MCU research | Exact IGX A04 carrier documents and population; no inferred compatibility |
| Electrical CAD | Native KiCad ERC/DRC/net parity and hashes | Latest source-bound reports clean, independent pinout review |
| Protection | Exact Bourns TVS and nominal voltage comparison | Defined ESD/EFT/surge setup, waveforms, survival and communication results |
| Signal integrity | Routed two-layer board; no maximum rate qualified | Intended CAN/CAN-FD rates, bus lengths, ribbon, capacitance and error measurements |
| Auxiliary I/O | Raw pins retained, power links open | Voltage/direction/current limits and any needed protection established |
| PCB assembly | JLC-format SMT and full-BOM paths, exact sourced connectors | Supplier stock, Wieson consignmentJ1, DFM/panel, placement rotation, first article approval |
| Housing | Valid solids/meshes, native PCB collision and cable envelope checks | Slicer review, actual print, flange/plug/header fit, lid fasteners, hot/creep checks |
| Strain relief | Heat-set inserts, recessed heads, hard stops, replaceable pads and clamp | Actual ribbon thickness;10N/60s pull and continuity before/after dwell |
| Saleable units | Proposed50-unit target | Every-unit continuity/functional test, serial/revision tracking and documented ratings |

Reports may pass CAD checks while these gates remain open. No automated tool is allowed to turn an unmeasured field into a passed physical gate. Prerelease packaging remains enabled until all applicable gates have recorded, reviewable test results.
