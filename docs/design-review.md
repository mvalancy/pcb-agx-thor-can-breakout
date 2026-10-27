# Design review — 2026-10-26

The GitHub landing-page defect is fixed: `.github/README.md` took precedence over the root README. The generator now omits that one special directory index, and release validation rejects its return. All other public content directories remain indexed.

A1 replaces the earlier routing and enclosure frame. Both boards now pass native ERC, DRC, connectivity and schematic parity; independent pin-map, paired-path and fabrication-profile checks also pass. Previously published A0 packages are historical and superseded. A1 remains subject to PR review and the physical/supplier gates below.

## Findings and corrective work

- **CAN routing:** the initial general autoroute connected the correct nets but separated several H/L paths and interrupted their return plane. Replaced with explicit paired trunks, documented header fanouts, TVS pads on the main paths and short termination branches. Added native keepout corridors under the trunks to preserve the return plane. Source-bound route measurements now pass on both variants.
- **Protection placement:** TVS devices rotated and moved toward the DE-9 solder pins; two local return vias replace the single-via arrangement. This follows the [TI TCAN1462 layout guidance](https://www.ti.com/lit/ds/symlink/tcan1462-q1.pdf). It does not establish a system surge rating.
- **JLC checks:** retrieved the manufacturer's current [fabrication capabilities](https://jlcpcb.com/capabilities/pcb-) and recorded the source hash in the project rule profile. Expanded native checks for annular rings, holes, copper/edge clearance, and readable silkscreen. A vendor DFM upload redirected to sign-in before analysis; **no JLCDFM analysis report exists yet**.
- **Lid:** replaced text rows with a numbered male mating-face diagram, H/L/GND/shield callouts, aligned port badges, paired-line motif and revision identity. The same reusable cad-agent drawing drives the engraved CAD and the SVG proof.

## Electrical authority and remaining proof

NVIDIA's P4071 A02 concept drawing identifies J47 and the four physical channels. The [AGX Thor software guide](https://docs.nvidia.com/jetson/archives/r38.2/DeveloperGuide/HR/ControllerAreaNetworkCan.html) identifies the two supported FSI ports and specifies termination shunts at J47 pins 3–4 and 7–8. The four-port variant's extra channels remain carrier/population dependent; IGX compatibility is unverified.

The adapter is passive: it carries bus-side CAN and adds shunt TVS protection. It has no transceiver, repeater, galvanic isolation, or sustained overvoltage disconnection. The Bourns CDSOT23-SM712 is the exact selected part; a generic SM712 substitution is not approved. No data rate or system immunity rating is claimed.

Before connecting a Thor, establish all 26 cable conductors and pin-1 orientation with the host disconnected; inspect the exact Wieson mating stack; confirm open power/termination/shield shunts and DE-9 pin 9 isolation; then check communication on a low-risk bench setup. Physical fit, cable retention, actual populated carrier behavior, CAN waveforms, EMC/transient tests and supplier assembly approval remain open. See the [release checklist](release-checklist.md).

## Mechanical frame correction

The old PCB STEP import reflected the board across a plane, reversing handedness while leaving its symmetric outline plausible. A1 uses a proper 180° Z rotation and translates by board width. Port labels, mating models and the ribbon clamp follow that same frame. Both housings and all viewer assets are rebuilt from the corrected native board. A0 enclosures are superseded.

## Review workflow

The project changes are on `dev/a1-routing-lid-review` and submitted into `main` in [PR #1](https://github.com/mvalancy/pcb-agx-thor-can-breakout/pull/1). Shared cad-agent code is pinned to its reviewed branch commit and proposed in [PR1](https://github.com/Valpatel/cad-agent/pull/1); connector resources remain in [KiCAD_Libs PR4](https://github.com/mvalancy/KiCAD_Libs/pull/4). No new release tag or production order is created by this review.

Final validation: both native electrical variants, independent routing/fabrication checks, both mechanical collision/path screens, seven STL/3MF parts and both current 13-part viewer scenes pass. Browser checks found no JavaScript exceptions, broken review assets or mobile page overflow. All three package ZIPs reproduce byte-for-byte from a clean checkout; project PR CI passes.
