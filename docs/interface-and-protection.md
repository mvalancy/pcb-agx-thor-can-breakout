# Interface and protection review

This is a passive bus-side adapter, not a CAN controller or galvanic isolator. Both sizes use the same Thor ribbon interface. The two-port board exposes FSI CAN0/1. The four-port board also exposes the two older `AURIX`-named channels in the generic A02 schematic; those names do not prove hardware population or IGX compatibility.

## Evidence and connector

The local original NVIDIA P4071 A02 archive was inspected: schematic sheet 11 gives J47; sheets 47–50 contain the four bus circuits; the BOM names **Wieson AC2800-0011-022-H0**. The CAD symbol's Samtec-style name is not the BOM MPN. The native A02 ODB/Allegro land pattern was subsequently recovered:26pads0.74×3.00mm, rows±1.93mm,1.27mm pitch, mask+0.05mm. The default board now uses this Wieson footprint and MPN. [Full audit](../research/j47-footprint-audit.md). Current manufacturer drawing and procurement remain unresolved.

**Samtec SHF-113-01-L-D-SM** remains an alternative candidate documented to mate with FFSD. Its recommended pads differ from the recovered Wieson layout; it is not an approved drop-in and is not the default BOM. The cable candidate is **FFSD-13-D-06.00-01-N**, 152.4 mm, 30 AWG, two female connectors: [DigiKey SAM8785-ND](https://www.digikey.com/en/products/detail/samtec-inc/FFSD-13-D-06-00-01-N/3190987), [Samtec](https://www.samtec.com/products/ffsd-13-d-06.00-01-n). The [Samtec catalog](https://suddendocs.samtec.com/catalog_english/ffsd.pdf) specifies compatible families and wiring options. Confirm the ordered cable's pin-1 marking and all 26 conductors by continuity before connecting Thor.

NVIDIA also identifies J47 and the termination arrangement in its [developer support explanation](https://forums.developer.nvidia.com/t/how-can-i-identify-the-two-can-pins-on-a-2x13-pin-connector-a-diagram-or-picture-would-be-greatly-appreciated-thank-you/357562). Use [hardware/interface.json](../hardware/interface.json) as the machine-readable pin authority; the schematics show every pin explicitly.

## CAN connections

| Thor J47 | Function | External connector |
|---|---|---|
| 3 / 5 | FSI CAN0 H / L | J2 pins 7 / 2 |
| 7 / 9 | FSI CAN1 H / L | J3 pins 7 / 2 |
| 11 / 13 | Generic A02 additional CAN1 H / L | J4 pins 7 / 2 on four-port only |
| 15 / 17 | Generic A02 additional CAN2 H / L | J5 pins 7 / 2 on four-port only |
| 4 / 8 / 12 / 16 | Host termination taps | JP1–JP4, H to TERM |
| 10 / 21 / 26 | Host ground | DE9 pins 3 and 6 |

DE9 pin 5 and metal shells connect to SHIELD. J12 can bond SHIELD to signal ground; leave it open by default and decide grounding at system level. Pins 1, 4, 8 and 9 are unconnected. Pin 9 never exports host power. This follows the CAN assignment described by [CiA](https://www.can-cia.org/can-knowledge/cia-106-connector-pin-assignment) and [NI's CAN cable specification](https://www.ni.com/en/support/documentation/supplemental/18/specifications-for-the-can-obd-ii-cable.html). This connector is not RS232.

The host has 120 Ω from CAN-L to TERM in the examined schematic. A shunt H→TERM enables it; do not add another 120 Ω on this adapter. Fit shunts only at physical bus endpoints. Ship all shunts open.

## Transient protection

Each exposed CAN channel has a **Bourns CDSOT23-SM712**, exact supplier code **C404012**, with pins 1/2 to H/L and pin 3 to GND. The [Bourns datasheet](https://www.bourns.com/docs/product-datasheets/cdsot23-sm712.pdf) gives +12/−7 V working standoff, +20/−12 V maximum clamping at 5 A (8/20 µs), and 75 pF typical capacitance. The PCB places the TVS near the DE9 and places the TVS pads on the main signal path and adds two short ground vias into the bottom return plane.

The examined carrier uses [NXP TJA1463](https://www.nxp.com/docs/en/data-sheet/TJA1463.pdf) on FSI0 and additional CAN1, and [TI TCAN1462](https://www.ti.com/lit/gpn/tcan1462-q1) on FSI1 and additional CAN2. Their absolute bus limits differ: −36/+40 V for the NXP device versus ±58 V for TI. Selecting a generic 24 V suppressor with a 42–50 V clamp can exceed the weaker device's limit. The chosen part has better nominal voltage margin, but trace inductance, pulse waveform, temperature and tolerances still require system testing.

The original schematic's PESD1CAN/choke options are marked NO STUFF. That is evidence about this generic design, not proof of the populated board in hand.

**Scope:** no galvanic isolation, no sustained 24 V miswire protection, no system ESD/EFT/surge rating yet. The clamp narrows permitted sustained common-mode voltage to its −7/+12 V working range. Its capacitance, the ribbon and the PCB routes must be tested at the intended bitrates. Start bench evaluation at 500 kbit/s and 1 Mbit/s; then evaluate CAN FD 2/5/8 Mbit/s separately. No maximum bitrate is certified by this project.

## Auxiliary I/O

J10 breaks out all non-CAN pins and ground. JP5/JP6 separately enable 3.3 V/5 V; both ship open. The GPIO, I2C/UART, E-stop and wake names are schematic names, not a declaration that the AGX kit supports them. These are raw, unbuffered pins with no added surge protection. Keep them internal; establish actual voltage levels, direction, population and available current from the exact carrier revision before use. Never apply 24 V to J10. The two-port board also retains the six additional CAN bus pins on J11, for engineering access only.

## Isolation option

A bus-side isolated repeater needs transceivers on both bus segments, isolated power and arbitration-safe dominant/recessive logic. Directly cross-coupling RX/TX can latch the buses dominant. [TI TIDA-01487](https://www.ti.com/tool/TIDA-01487) is a useful reference, but its stated 2 Mbit/s CAN FD scope does not establish 8 Mbit/s operation. An isolated version is deferred pending a separate repeater architecture and timing budget.

## A1 pair routing evidence

The CAN H/L trunks use 0.25 mm traces and 0.25 mm straight-section edge spacing, with the same two layer transitions per conductor. The TVS lies on each measured main path; each local H-to-termination jumper branch is 1.75 mm. H/L path imbalance is 2.67–3.01 mm across the six channels, including nominal via barrels and connector fanouts.

Native bottom-layer routing keepouts preserve ground beneath the front-layer trunks while allowing the ground pour. Sampled trunk centerlines have no missing reference in the current reports. Connector/header fanouts are outside the coupling window. This is a geometric screening result, not a field simulation, controlled 120 Ω stackup or qualified maximum bitrate.

[Two-port routing diagram](../exports/2port/can-routing.svg) · [Four-port routing diagram](../exports/4port/can-routing.svg) · [Two-port measurements](../exports/2port/can-routing-review.json) · [Four-port measurements](../exports/4port/can-routing-review.json)
