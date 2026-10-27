# PINOUT proof

The electrical mapping is checked against two NVIDIA sources: the **P4071 A02 concept schematic, sheet 11**, and the **Jetson Linux Developer Guide r38.2**. These establish the documented J47 interface; they do not establish the population of every AGX or IGX carrier revision.

## Original J47 connector

![NVIDIA P4071 A02 sheet 11: J47 connector, pins and Wieson part number](proof/nvidia-p4071-a02-j47.png)

© NVIDIA. Direct crop of `P4071_A02_Concept_schematics.pdf`, sheet 11, reviewed 2026-10-26. The complete design archive is available through [NVIDIA Embedded Downloads](https://developer.nvidia.com/embedded/downloads). Original PDF SHA-256: `b3b8547259a62ff21d061c111f31a39a7183bc9989aee130e411bf05b6d4f722`.

Read the **external contact numbers beside each wire**, not the sequential symbol text inside the rectangle. J47 identifies **AC2800-0011-022-H0**. The header's physical pad numbering was separately cross-checked against NVIDIA's native layout in the [footprint audit](../research/j47-footprint-audit.md).

## Supported AGX Thor CAN pins

<img src="proof/nvidia-r38-2-thor-can.png" alt="NVIDIA r38.2 table: Jetson Thor has two controllers and uses J47 pins 3, 5, 7 and 9" width="290">

© NVIDIA. Unmodified screenshot crop of the Thor column in the [r38.2 CAN guide](https://docs.nvidia.com/jetson/archives/r38.2/DeveloperGuide/HR/ControllerAreaNetworkCan.html), captured 2026-10-26. The rows show controller count, controller addresses and the J47 bus pins. The guide also specifies enabling the onboard termination by bridging **3–4** for CAN0 or **7–8** for CAN1.

| Function | Carrier J47 → adapter J1 | Adapter destination |
|---|---|---|
| FSI CAN0 H / L | 3 / 5 | J2 DE9 7 / 2 |
| FSI CAN1 H / L | 7 / 9 | J3 DE9 7 / 2 |
| CAN0 / CAN1 termination tap | 4 / 8 | JP1 / JP2; shunt to the corresponding H net |
| Ground | 10, 21, 26 | DE9 3 and 6; internal ground |
| Generic A02 extra CAN1 H / L | 11 / 13 | Four-port J4 DE9 7 / 2; reserved |
| Generic A02 extra CAN2 H / L | 15 / 17 | Four-port J5 DE9 7 / 2; reserved |
| Extra termination taps | 12 / 16 | Four-port JP3 / JP4; reserved |

The full 26-pin map, including raw I/O, is in [hardware/interface.json](../hardware/interface.json). An independent transcription in [check_electronics.py](../tools/check_electronics.py) checks the exported native netlist. It also verifies DE9 ground/shield/NC pins, TVS pins and the open power-link boundaries.

## What this proves—and what still needs a sample

The two sources agree on FSI CAN0/1 polarity and numbering. The generic A02 drawing additionally supplies the auxiliary and reserved-channel names. It does **not** prove that the additional transceivers or AURIX-related signals are populated, supported, or compatible with an IGX carrier. See [IGX research](../research/igx-compatibility.md).

Before connection, verify all 26 conductors of the actual Samtec cable, the stripe/key orientation and the exact Wieson mating stack while disconnected from Thor. The cable order code and 1.27 mm pitch alone are insufficient proof. No project hardware continuity test has been performed.

[Capture provenance](proof/provenance.json) · [Interface and protection](interface-and-protection.md) · [Native schematics](../hardware/README.md)
