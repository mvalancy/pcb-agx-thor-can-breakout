# Thor J47 authority

The generic P4071 A02 J47 BOM part is **Wieson AC2800-0011-022-H0**. A Samtec-style schematic symbol name is not the installed MPN. The native lands are independently measured in the [header audit](../../research/j47-footprint-audit.md).

NVIDIA r38.2 documents FSI CAN0 at J47 H3/L5 and CAN1 at H7/L9, with termination bridges 3–4 and 7–8. The [source excerpts](../../docs/pinout-proof.md) and [interface map](../../hardware/interface.json) retain all 26 contacts. The semantic checker independently transcribes these pins rather than importing the generator mapping.

SHF/FFSD is a documented Samtec pairing. Physical FFSD mating to the exact Wieson header remains open. AURIX net names in the generic schematic do not establish actual AGX population or IGX support. Require exact carrier revision evidence and physical cable continuity before connection.

J47 pin 6 `FSI_EXT_GPIO1` traces to module J39 / FSI_GPIO06 (P4071 A02 sheet 7). It reaches J10 pin 3; the shortened silk is `FSI6`. NVIDIA staff's [September 2026 clarification](https://forums.developer.nvidia.com/t/question-about-can-stb-control-using-fsi-gpio05-06-in-the-jetson-thor-reference-design/383203) establishes FSI firmware ownership, not ordinary Linux GPIO support. The raw ESTOP/AURIX net names likewise do not establish usable Linux peripheral functions or carrier population.

P1/P2 free pads are unconnected plated holes. TP1/TP2 rows are GND, AUX_3V3 and AUX_5V_AO; both supply rows stay behind JP5/JP6. Prototype pads and taps are excluded from factory assembly files. See [controls and prototyping](../../docs/termination-and-io.md) and the independent native prototype reports.
