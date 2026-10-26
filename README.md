<h1 align="center">Thor CAN breakout</h1>
<p align="center">Protected CAN adapters and printable ribbon-clamp housings for NVIDIA Thor.<br><b>A0 engineering prototype · two- and four-port variants · MIT licensed</b></p>

<p align="center"><img src="preview/2port-open.png" alt="Two-port housing with DB9 connectors and replaceable ribbon clamp" width="850"></p>

**Local design workspace:** [localhost:8765/site/](http://localhost:8765/site/) embeds the schematics, PCB layers, assembly drawings, enclosure views, reports and downloads. It uses the reusable [cad-agent](https://github.com/Valpatel/cad-agent) review workbench.

**Status:** routed KiCad prototypes and printable CAD, undergoing repeated software/geometry validation. No hardware has been fabricated, printed, fit-tested or electrically qualified. Read the [release gates](docs/release-checklist.md) before ordering. The four-port version is an engineering extension of the generic P4071 A02 header; **IGX compatibility remains unverified**.

## Choose a variant

| | Two-port | Four-port engineering variant |
|---|---|---|
| Target | AGX Thor FSI CAN0/1 | All four generic A02 CAN channels; exact host audit pending |
| PCB | 93 × 65 mm | 177 × 65 mm |
| Housing | 100.2 × 86.2 × 26.8 mm | 184.2 × 86.2 × 26.8 mm |
| Schematic | [PDF](exports/2port/schematic.pdf) | [PDF](exports/4port/schematic.pdf) |
| Layers | [Top](exports/2port/pcb-top.svg) · [Bottom](exports/2port/pcb-bottom.svg) | [Top](exports/4port/pcb-top.svg) · [Bottom](exports/4port/pcb-bottom.svg) |
| Native project | [KiCad](hardware/2port/thor-2port.kicad_pro) | [KiCad](hardware/4port/thor-4port.kicad_pro) |
| Assembly | [Drawing](exports/2port/assembly.svg) · [BOM](exports/2port/bom-review.csv) | [Drawing](exports/4port/assembly.svg) · [BOM](exports/4port/bom-review.csv) |
| Evidence | [Electrical](exports/2port/pcb-evidence.json) · [Mechanical](exports/2port/mechanical-checks.json) | [Electrical](exports/4port/pcb-evidence.json) · [Mechanical](exports/4port/mechanical-checks.json) |

The board uses standard CAN DE9 pins2=L,7=H,3/6=GND,5/shell=shield; pin9 is unpowered. Termination shunts enable the carrier's own120Ω resistor. Auxiliary I/O is raw, with power links open by default. Each CAN channel has a Bourns CDSOT23-SM712 suppressor. It is **not isolated, sustained24V-miswire protected, or system surge-rated**. See [interface/protection](docs/interface-and-protection.md).

## Header and cable

Thor's J47 BOM identifies **Wieson AC2800-0011-022-H0**, male2×13 at1.27mm. J1 now uses the **same Wieson MPN**, with its26pad land pattern recovered and cross-checked from NVIDIA's native ODB/Allegro layout. [Audit and dimensions](research/j47-footprint-audit.md). Current manufacturer drawing, procurement, exact height and cable mating still require confirmation. Samtec SHF is retained only as a separately documented candidate, not an approved drop-in.

Ribbon candidate: **Samtec FFSD-13-D-04.00-01-N**,101.6mm, two female connectors; [DigiKey SAM10480-ND](https://www.digikey.com/en/products/detail/samtec-inc/FFSD-13-D-04-00-01-N/6561558). Verify all26 conductors and key orientation before connecting Thor. [Sourcing audit](research/connector-sourcing.md) covers the AssmannC3127392 DE9 and exact auxiliary headers.

## Print and assemble

Use one matching base/lid pair and one universal ribbon clamp. Test the fastener and port coupons first. [Assembly instructions](ASSEMBLY.md) specify recessed screws, heat-set inserts, silicone pads, termination and bench checks.

| Printed part | Download | Quantity |
|---|---|---:|
| Two-port base/lid | [BaseSTL](exports/2port_base.stl) · [LidSTL](exports/2port_lid.stl) | One each if selected |
| Four-port base/lid | [BaseSTL](exports/4port_base.stl) · [LidSTL](exports/4port_lid.stl) | One each if selected |
| Universal ribbon clamp | [STL](exports/ribbon_clamp.stl) | 1 |
| Fastener coupon | [STL](exports/fastener_coupon.stl) | Test first |
| DE9 opening coupon | [STL](exports/port_coupon.stl) | Test first |

STEP and verified bed-oriented3MF files are in [exports](exports/README.md). The clamp has M3 heat-set inserts, a 1.8 mm hard gap and replaceable pads; the proposed10N/60s pull test has not been performed. Rounded shells include a perimeter tongue-and-groove seam, recessed screw heads and shared PCB/lid fasteners. The lid carries port names, CAN pinout, A0 revision and github.com/mvalancy. Ports have 42 mm pitch, leaving a 9.8 mm housing rib and 7.7 mm between maximum-width Assmann A-FT09 backshells. [Mating reference audit](research/mating-dsub-clearance.md). The rear clamp chamber keeps its screws away from PCB conductors.

## Manufacturing and releases

See [JLCPCB upload instructions](docs/manufacturing.md). Each variant supplies Gerbers/drills, a fabrication-review ZIP, schematic PDF, assembly drawing, exact-part BOM, and separate SMT-only/full-sourced BOM/CPL options. J1 still requires an approved Wieson sourcing/consignment arrangement. No order has been placed.

[Release packages](releases/README.md) separate two-port PCB, four-port PCB and printable housings, with checksums and source/artifact hashes. GitHub releases remain marked **pre-release** until physical and electrical gates are closed. Start with3–5 engineering prototypes before the approximately50-unit target batch.

## Reproduce

Use Python3.11, KiCad10.0.1 and the pinned cad-agent revision in `requirements.txt`. KiCad's Python must provide `pcbnew`; mechanical Python uses the local venv. Vendor reference archives are not redistributed.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python tools/export_review.py
.venv/bin/python tools/check_electronics.py
.venv/bin/python cad/build.py
.venv/bin/python tools/check_mechanics.py
.venv/bin/python tools/render_review.py
.venv/bin/python tools/draw_mechanics.py
.venv/bin/cad-agent export-3mf
.venv/bin/cad-agent view
.venv/bin/python tools/update_evidence.py
.venv/bin/python tools/validate_release.py --record
.venv/bin/python tools/package_release.py
.venv/bin/cad-agent site --serve --port 8765
```

The committed boards are already routed. `tools/build_electronics.py` regenerates native sources from `hardware/interface.json`; it overwrites layouts unless invoked with `--schematic-only`. A full electrical regeneration requires route-session import/finalization and all checks again. See [tools](tools/README.md). `cad/parameters.json` owns mechanical dimensions. [Iteration history](docs/iterations.md) records checks that caught actual errors.

## Project folders

| Folder | Contents |
|---|---|
| [hardware](hardware/README.md) | Native KiCad projects, exact pin map, pinned footprints |
| [cad](cad/README.md) | Parametric enclosure source and dimensions |
| [exports](exports/README.md) | Check reports, PCB fabrication review, drawings and print files |
| [preview](preview/README.md) | Current assembly and housing renders |
| [docs](docs/README.md) | Manufacturing, protection, qualification and progress |
| [research](research/README.md) | IGX compatibility and connector evidence |
| [references](references/README.md) | Source identifiers/URLs/hashes; no vendor archives |
| [tools](tools/README.md) | Rebuild, validation, release and README helpers |
| [releases](releases/README.md) | Download/package structure and release notes |
| [.agents](.agents/README.md) | Canonical lessons, evidence and review procedures |
| [.github](.github/README.md) | CI and prerelease publication workflow |

## License

Original work is [MIT licensed](LICENSE). Redistributed KiCad library files retain their own CC BY-SA4.0 terms with the design exception; see [third-party notices](THIRD_PARTY.md). Vendor PDFs and logos are not relicensed or redistributed. This project is not affiliated with NVIDIA, Samtec or JLCPCB.
