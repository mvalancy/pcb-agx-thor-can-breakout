# Manufacturing and 50-unit plan

A0 is an engineering review package. The files are organized for quoting and prototype preparation; unresolved release gates prevent a production-ready designation.

## PCB settings

| Setting | A0 |
|---|---|
| Board size | 93 × 65 mm two-port; 177 × 65 mm four-port |
| Stackup | Two layers, nominal 1.6 mm FR4, 1 oz copper |
| Minimum rules | 0.20 mm clearance/track; 0.60/0.30 mm via; 0.30 mm copper to edge |
| Solder mask / finish | Green; lead-free HASL baseline, ENIG optional quote |
| Assembly side | Top only; bottom ground plane |
| Fiducials / panel rails | Three board fiducials; supplier panel tooling review required before PCBA |

Rules are conservative relative to the published [JLCPCB PCB capabilities](https://jlcpcb.com/capabilities/Capabilities). Service-specific limits still apply. JLC's [assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities) include through-hole services; do not assume that only SMT is available. Standard service's minimum dimensions may require a panel/rails for a 65 mm deep board. Ask JLC to retain the board outline and mount coordinates when panelizing.

## Files to upload

Each variant has a separate folder under `exports/`. Never mix the two variants.

1. Inspect `schematic.pdf`, `pcb-top.svg`, `pcb-bottom.svg`, `assembly.svg` and the ERC/DRC reports.
2. For a fabrication quote, upload `thor-<variant>-A0-fabrication-REVIEW.zip`. It contains two copper layers, masks, top silkscreen/paste, outline, and separate plated/non-plated Excellon drills. The accompanying text explicitly says **DO NOT ORDER** until the release checklist is complete.
3. For an economical TVS-only PCBA quote, upload `jlc-bom.csv` and `jlc-cpl.csv`. All connectors are separately assembled/consigned in this route.
4. For a quote including sourced through-hole connectors, upload `jlc-full-bom.csv` and `jlc-full-cpl.csv`. These contain the Bourns TVS, Assmann DE9, BOOMELE auxiliary/reserved headers and XFCN jumper headers. **J1 Wieson still requires manual installation or an approved consignment/sourcing arrangement.** This is not an all-inclusive turnkey BOM.
5. Inspect every placement in JLC's assembly viewer. The CPL uses native KiCad coordinates, millimeters, top side and uncorrected KiCad rotation. Automated CSV checks cannot prove JLC's library zero-angle convention. Confirm Bourns pin 3, header pin 1 and DE9 orientation individually.
6. Obtain supplier DFM, stock, panel, setup, attrition and shipping quotes before authorizing manufacture. No order has been submitted. J10 pin14 has a deliberate solid ground-plane connection; include its thermal mass in solder-process/first-article review.

All currently sourced electronic components are exact manufacturer/SKU selections. They are not advertised as JLC Basic parts. Do not substitute a different manufacturer's SM712 based only on the shortened name. [Connector sourcing](../research/connector-sourcing.md) records drawings, drill changes and still-unverified mechanical assumptions.

## Quantity and budget

Build 3–5 engineering prototypes first. After the electrical/fit/pull-test results are accepted, quote 50 saleable assemblies plus the supplier's required attrition. Test every assembled unit before sale. Two separate 50-unit variants would mean 100 units; the current target is approximately 50 total, with the mix undecided.

Known price snapshots, 2026-10-26: the 101.6 mm Samtec cable was listed at about $11.52 at 50 (about $576 for 50 cables); the Assmann DE9 snapshot was $0.75144 at 90 on DigiKey. These are distributor observations, not a landed quotation or guaranteed stock. Cable/header cost will dominate the passive circuit. Obtain current JLC pricing for all C-codes and quote assembly/panelization before choosing a sale price.

Budget worksheet items still needing quotes: boards and panel rails, exact Bourns suppressors, Wieson headers, assembly/setup/attrition, import/shipping, filament, silicone pads, screws/inserts/shunts, test labor, scrap and packaging. Do not infer a total unit cost from the few quoted components.

## Default assembly

All soldered headers are fitted. All removable shorting shunts ship OPEN: JP1–JP4 termination, JP5 3.3 V, JP6 5 V, and J12 shield bond. Include loose shunts only with clear instructions. No power appears on DE9 pin 9. Label each port CAN0/1 or RESERVED additional channels, and label the ribbon pin-1 stripe.
