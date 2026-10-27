# Manufacturing and 50-unit plan

A1 is an engineering review package. The files are organized for quoting and prototype preparation; unresolved release gates prevent a production-ready designation.

## PCB settings

| Setting | A1 |
|---|---|
| Board size | 93 × 90 mm two-port; 177 × 90 mm four-port |
| Stackup | Two layers, nominal 1.6 mm FR4, 1 oz copper |
| Minimum rules | 0.20 mm clearance/track; 0.60/0.30 mm via; 0.30 mm copper to edge |
| Solder mask / finish | Green; lead-free HASL baseline, ENIG optional quote |
| Assembly side | Top only; bottom ground plane |
| Fiducials / panel rails | Three board fiducials; supplier panel tooling review required before PCBA |

The current [JLCPCB fabrication capabilities](https://jlcpcb.com/capabilities/pcb-) were retrieved on 2026-10-26, hashed, and transcribed into [the project profile](../hardware/jlcpcb-profile.json). `apply_fab_rules.py` installs native KiCad constraints for clearance, tracks, drill size, hole spacing, annular rings, copper-to-edge spacing and silkscreen. Both native DRC reports must pass.

The separate fabrication-profile check measures actual features: minimum 0.25 mm track, 0.30 mm via drill, 0.15 mm via ring, 0.30 mm plated-pad annular ring and 1.0 mm / 0.15 mm silkscreen height/stroke. A temporary board with an intentionally impossible 0.8 mm minimum track rule must fail native DRC, proving the rule engine is active. It never replaces the design board.

**JLCDFM has not approved these files.** The current A1 two-port Gerber ZIP was selected on 2026-10-26 at [JLCDFM](https://jlcdfm.com/) redirected to the supplier sign-in before analysis. The attempt produced no vendor DFM report and no order. The downloaded capabilities and local checks are not a substitute for that review; upload the final A1 package through an authenticated session before ordering.

JLC's [assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities) include through-hole services. Confirm the selected service's stock, panel/rail and tooling requirements for a 90 mm-deep board. Ask JLC to retain the outline and mounting coordinates when panelizing.

JLC provides a browser workflow, not a connected project API in this session. Its [PCB ordering guide](https://jlcpcb.com/help/article/how-do-i-place-an-order) describes Gerber upload, layer/dimension detection and a **Review Before Payment** option. Its [PCBA guide](https://jlcpcb.com/help/article/how-do-i-place-a-pcba-order) adds BOM/CPL matching and placement review. Confirm the options available for the selected assembly service; a rendered preview is not supplier engineering approval. JLC’s [ordering instructions](https://jlcpcb.com/help/article/instructions-for-ordering) say not to rely on README/PDF files inside the Gerber archive for special requirements—put them in the order parameters or remarks. No checkout or payment is authorized or performed by this project.

## Files to upload

Each variant has a separate folder under `exports/`. Never mix the two variants.

1. Inspect `schematic.pdf`, `pcb-top.svg`, `pcb-bottom.svg`, `assembly.svg` and the ERC/DRC reports.
2. For a fabrication quote, upload `thor-<variant>-A1-fabrication-REVIEW.zip`. It contains two copper layers, masks, top/bottom silkscreen and top paste, outline, and separate plated/non-plated Excellon drills. The accompanying text explicitly says **DO NOT ORDER** until the release checklist is complete.
3. For an economical TVS-only PCBA quote, upload `jlc-bom.csv` and `jlc-cpl.csv`. All connectors are separately assembled/consigned in this route.
4. For a quote including sourced through-hole connectors, upload `jlc-full-bom.csv` and `jlc-full-cpl.csv`. These contain the Bourns TVS, Assmann DE9, BOOMELE auxiliary/reserved headers and XFCN jumper headers. **J1 Wieson still requires manual installation or an approved consignment/sourcing arrangement.** This is not an all-inclusive turnkey BOM.
5. Inspect every placement in JLC's assembly viewer. The CPL uses native KiCad coordinates, millimeters, top side and uncorrected KiCad rotation. Automated CSV checks cannot prove JLC's library zero-angle convention. Confirm Bourns pin 3, header pin 1 and DE9 orientation individually.
6. Obtain supplier DFM, stock, panel, setup, attrition and shipping quotes before authorizing manufacture. No order has been submitted. J10 pin14 has a deliberate solid ground-plane connection; include its thermal mass in solder-process/first-article review.

All currently sourced electronic components are exact manufacturer/SKU selections. They are not advertised as JLC Basic parts. Do not substitute a different manufacturer's SM712 based only on the shortened name. [Connector sourcing](../research/connector-sourcing.md) records drawings, drill changes and still-unverified mechanical assumptions.

## Quantity and budget

Build 3–5 engineering prototypes first. After the electrical/fit/pull-test results are accepted, quote 50 saleable assemblies plus the supplier's required attrition. Test every assembled unit before sale. Two separate 50-unit variants would mean 100 units; the current target is approximately 50 total, with the mix undecided.

Known price snapshots, 2026-10-26: the preferred [152.4 mm Samtec cable](https://www.digikey.com/en/products/detail/samtec-inc/FFSD-13-D-06-00-01-N/3190987) was listed at about $12.04 at 50 (about $602 for 50 cables); the Assmann DE9 snapshot was $0.75144 at 90 on DigiKey. These are distributor observations, not a landed quotation or guaranteed stock. Cable/header cost will dominate the passive circuit. Obtain current JLC pricing for all C-codes and quote assembly/panelization before choosing a sale price.

Budget worksheet items still needing quotes: boards and panel rails, exact Bourns suppressors, Wieson headers, assembly/setup/attrition, import/shipping, filament, silicone pads, screws/inserts/shunts, test labor, scrap and packaging. Do not infer a total unit cost from the few quoted components.

## Default assembly

All soldered headers are fitted. All removable shorting shunts ship OPEN: JP1–JP4 termination, JP5 3.3 V, JP6 5 V, and J12 shield bond. Include loose shunts only with clear instructions. No power appears on DE9 pin 9. Label each port CAN0/1 or RESERVED additional channels, and label the ribbon pin-1 stripe.

The prototype grids and power taps are **bare plated PCB features**, excluded from both assembly populations. Include the loose jumper caps listed in the [enclosure/accessory BOM](../exports/enclosure-bom.csv), with the [termination and I/O guide](termination-and-io.md).
