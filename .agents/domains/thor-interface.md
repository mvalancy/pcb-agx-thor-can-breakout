# Thor J47 authority

The generic P4071 A02 J47 BOM part is **Wieson AC2800-0011-022-H0**. A Samtec-style schematic symbol name is not the installed MPN. The native lands are independently measured in the [header audit](../../research/j47-footprint-audit.md).

NVIDIA r38.2 documents FSI CAN0 at J47 H3/L5 and CAN1 at H7/L9, with termination bridges 3–4 and 7–8. The [source excerpts](../../docs/pinout-proof.md) and [interface map](../../hardware/interface.json) retain all 26 contacts. The semantic checker independently transcribes these pins rather than importing the generator mapping.

SHF/FFSD is a documented Samtec pairing. Physical FFSD mating to the exact Wieson header remains open. AURIX net names in the generic schematic do not establish actual AGX population or IGX support. Require exact carrier revision evidence and physical cable continuity before connection.
