# Thor CAN carrier compatibility

Research checked 2026-10-26. This records the evidence behind the two- and four-port variants; it is not a hardware qualification report.

The user's distinction is substantially correct: Jetson AGX Thor does not expose a supported external safety MCU configuration, while IGX Thor Mini includes a safety MCU. The MCU name needs correction: NVIDIA identifies the Mini's device as **Renesas RH850/U2A16**, not Infineon AURIX. The older **IGX Orin** specification lists an **Infineon Aurix TC397**. Historical `AURIX_*` net names in the generic Thor schematic do not identify the populated production MCU. Sources: [IGX Thor Mini datasheet, page 3](https://developer.download.nvidia.com/assets/igx/robotics-datasheet-igx-thor-developer-kit-mini-nvidia-us-web1.pdf), [IGX Thor SMCU guide](https://docs.nvidia.com/igx/user-guide/latest/SMCU/smcu.html), [IGX Orin specification](https://docs.nvidia.com/igx/developer-kit-product-brief/latest/specifications.html).

| Host / carrier | Verified evidence | Adapter status |
|---|---|---|
| Jetson AGX Thor, P4071 A02 reference | NVIDIA documents two FSI CAN channels on J47. The supplied generic schematic labels its safety MCU pages unsupported. | Two-port design target; assembly, cable and protection qualification remain required. |
| IGX Thor Developer Kit Mini / T5000, A04 design collateral | Mini has a Renesas safety MCU and a CAN header described as 2 × 13 pins. Exact A04 pin assignment and channel availability have not been verified. | Four-port compatibility candidate only. |
| IGX Thor Developer Kit / T7000 boardkit | Separate carrier platform with BMC, ConnectX-7 and safety MCU. Published I/O summary differs from T5000. | No J47 compatibility claim. |
| IGX Orin | Aurix TC397 documented; different platform. | Out of scope. |

NVIDIA distinguishes the [Mini/T5000 system](https://docs.nvidia.com/igx/user-guide/latest/OV/thor/system-overview-t5000.html) from the [T7000 system](https://docs.nvidia.com/igx/user-guide/latest/OV/thor/system-overview-t7000.html). The [module and boardkit datasheet, page 3](https://developer.download.nvidia.com/assets/igx/robotics-datasheet-igx-thor-module-board-kit-nvidia-us-4845700-web.pdf) lists a 2 × 13-pin CAN header for T5000 and separate CAN/GPIO I/O entries for T7000. These summaries do not establish matching connector wiring or four usable CAN channels.

## Verified AGX signals and limits of the generic schematic

The [Jetson Linux r39.2 CAN guide](https://docs.nvidia.com/jetson/archives/r39.2/DeveloperGuide/HR/ControllerAreaNetworkCan.html) specifies J47 pin 3 = FSI CAN0 H, pin 5 = FSI CAN0 L, pin 7 = FSI CAN1 H, and pin 9 = FSI CAN1 L. It documents two controllers and onboard transceivers. Its termination jumpers connect pins 3–4 and 7–8.

The locally supplied vendor file `P4071_A02_Concept_schematics.pdf` labels pages 8–9 `SMCU(Not supported)`. Its CAN sheet includes additional `AURIX_CAN1_*` and `AURIX_CAN2_*` signals, but also identifies itself as a generic base schematic with assembly/BOM limitations. The additional channels are therefore a useful **P4071 A02 full-header engineering reference**, not evidence that the AGX production board provides four working CAN ports. Vendor files remain outside the public repository.

## A04 evidence still required

The official [IGX download center](https://developer.nvidia.com/igx-downloads), through its [download catalog](https://developer.nvidia.com/search-data/igx_downloads.json), lists these documents under “IGX Thor Hardware Documents”:

- [IGX T5000 Carrier Board Design Files A04](https://developer.nvidia.com/downloads/assets/embedded/secure/jetson/thor/docs/igx/nvidia_igx_t5000_carrier_board_design_files_a04.zip).
- [IGX Thor Developer Kit Mini Product Specification v1.1, SP-12695-001](https://developer.nvidia.com/downloads/assets/embedded/secure/jetson/thor/docs/igx/igx_thor_developer_kit_mini_spec_sp-12695-001_v1.1.pdf).
- [Jetson Thor to IGX T5000 Carrier Board Comparison and Safety Migration Note v1.0, DA-12303-001](https://developer.nvidia.com/downloads/assets/embedded/secure/jetson/thor/docs/igx/jetson_thor_to_igx_t5000_migration_guide_da-12303-001_v1.0.pdf).

Fetch evidence on 2026-10-26: ordinary HTTPS requests using Python `urllib.request.urlopen` returned HTTP 200 with `text/html`, approximately 11 kB of NVIDIA login HTML, for each link. Neither PDF nor ZIP signatures were present. Their contents have **not** been inspected, and HTTP success must not be treated as a successful document download.

Before labeling the four-port adapter IGX-compatible, obtain the authorized A04 documents and audit all 26 contacts against `hardware/interface.json`: connector part/key orientation; CAN H/L and termination paths; grounds and supply voltage/current limits; GPIO direction, voltage and boot state; safety-control signals; fitted transceivers and assembly options. Separately establish which MCU CAN channels the supported firmware exposes. Confirm the actual carrier revision and test cable continuity, host fit and CAN operation on that hardware. A matching header size or legacy signal name is insufficient.
