# J47 Wieson land-pattern audit

Verified 2026-10-26 against the local NVIDIA P4071 A02 design archive. The archive supports a **reference-layout-derived footprint for Wieson AC2800-0011-022-H0**, including all 26 lands and their numbering. It does **not** prove that the proposed ribbon cable mates or that a current Wieson production part matches this archive. Those remain sample/procurement gates.

## Identity and evidence

The original archive directory is `Downloads/Jetson_Thor_Devkit_Carrier_Baord_Design_Files_A02`. Source files remain outside the repository. Line numbers below refer to the unmodified extracted text, not this report.

| Reference | Evidence |
|---|---|
| `P4071_A02_BOM.xlsx`, worksheet `NvidiaMultiLevelBOMWithAML`, row 1382 | J47, quantity 1, **AC2800-0011-022-H0**, Wieson America Inc.; description is a vertical male SMD 2×13 header at 1.27 mm pitch. |
| `P4071_A02_Allegro_layout_ascii_extract.zip` → `P4071_A02_Allegro_layout.brd.alg` | Actual placed pad/mask/paste records; dimensioned alternative outlines. Referred to as **ALG** below. |
| `P4071_A02_ValorODB_database.zip` → `616-14071-1000-A02.tgz` → `142-14071-1000-a02/steps/cad/` | Independent package pin table, component placement, and bottom-copper features. Referred to as **ODB** below. |

The package name is `CON_HDR_002X013_SMD_ST_M_P127`. Its legacy device metadata mentions **FTSH-113-01-F-DV-K**, but this is not the BOM choice: ALG line 529435 explicitly labels the `MECH_DIMENSION_ASTRON` drawing **AC2800-0011-022-H0**. The separate `MECH_DIMENSION` alternative is labeled FTSH at line 529436. Their body dimensions must not be mixed.

## Lands, numbering, and board-side normalization

Use the geometric center between the rows and columns as footprint origin. In a **top-side KiCad footprint, viewed from the component side, with X right and Y down**, the derived pad coordinates are:

```text
             X increases →
Y = -1.93    2   4   6   8  10  12  14  16  18  20  22  24  26
Y = +1.93    1   3   5   7   9  11  13  15  17  19  21  23  25
X endpoints -7.62                                               +7.62
```

For column `j = 0…12`, `x = -7.62 + 1.27*j`; odd pin `2*j+1` is at `y=+1.93`, and even pin `2*j+2` is at `y=-1.93`. Pad 1 is therefore at the lower left in this top-view convention. This preserves the existing project's odd/even row assignment while changing the land geometry.

The native ODB package table has odd pins at `y=-1.93` and even pins at `y=+1.93` (`eda/data`, lines 122115–122166). Convert package Cartesian Y to KiCad screen Y with **`(x_kicad,y_kicad)=(x_odb,-y_odb)`**. Do not additionally mirror this top footprint.

J47 itself is on the NVIDIA board's **bottom**, mirrored and rotated 180° in ALG line 1136853; origin is `(61.700,-3.400)`, not the reported bounding-box center `(61.700,-2.795)`. ODB `layers/comp_+_bot/components` line 2082 independently places package 49 there at 180°. All 26 placed coordinates satisfy `x_board=61.7+x_odb`, `y_board=-3.4-y_odb`; this was checked numerically against both records. Thus the convenient translation `(x_board-61.7,y_board+3.4)` yields the KiCad coordinates above **for this particular placement**. Do not copy the source board rotation/mirror flags into the new footprint. ODB `TOP` records at lines 2094–2119 are toeprint records; that keyword does not mean top board side.

| Feature | Verified dimensions |
|---|---|
| Copper | 26 rectangular SMD pads, **0.740 × 3.000 mm**; row-center spacing **3.860 mm**. |
| Paste | Same 0.740 × 3.000 mm rectangles. |
| Solder mask | 0.840 × 3.100 mm; **0.050 mm expansion per edge**. |
| Holes / extra pads | No J47 drill values, mounting holes, or additional pads in these records. |
| Copper outer / inner edges | `abs(y)=3.430` / `0.430 mm`. |

ALG examples: pin 1 mask/paste/copper lines 383598–383600; pin 2 lines 382248–382250; pin 25 lines 337926–337928; pin 26 lines 408601–408603. All 26 were checked for identical sizes and empty drill fields. ODB `layers/bottom/features` defines `$91 rect740x3000 M` at line 102 and independently places pins 1/2/25/26 at lines 24803/24071/4895/45684. Electrical sanity checks agree with the schematic: pin 1 `VDD_3V3`, pin 2 `5V_AO`, pin 3 `FSI_CAN0_H`, pin 4 `FSI_CAN0_TERM`, pin 5 `FSI_CAN0_L`.

## Body, pin-1 marker, and clearance

The companion [measurement JSON](j47-footprint-measurements.json) supplies normalized polygons and source line ranges, all using the same KiCad coordinate convention above.

- **Wieson nominal outline:** ALG `MECH_DIMENSION_ASTRON` lines 529150–529161. Main rectangular core is **16.810 × 3.450 mm**, `x=±8.405`, `y=±1.725`; central extensions occupy `x=±2.550` and reach `y=±2.555`. Dimension annotations confirm 16.81, 3.45, 1.27 pitch, 15.24 contact span, 0.40 square contacts, and 5.80 terminal span (lines 529421–529428).
- **Separate CAP graphic:** lines 529138–529149, called out as `CAP` at line 529420. It is 6.00 mm wide, extends from `y=-2.11` to `+4.49`, and has a 2.40 mm-wide neck. **The archive does not establish this as a polarizing key, a shroud, or an installed feature after assembly.** Do not make a keyed cable or enclosure claim from it.
- **Source clearance envelope:** `DFA_BOUND_BOTTOM` lines 529394–529409, also reproduced as the ODB package contour at `eda/data` lines 122093–122112. Bounds are `x=±8.555`, `y=-3.430…+4.640`, overall **17.110 × 8.070 mm**. This includes pads and the expanded CAP feature; it is not the nominal body. `PLACE_BOUND_BOTTOM` is a different composite polygon, lines 529370–529393. Preserve these distinctions. A KiCad courtyard margin is a separate design choice; do not describe this source DFA boundary as an IPC courtyard.
- **Pin-1 marker:** source silk triangle lines 529280–529282 is on the odd-row/negative-X side, with vertices `(-8.592,+3.147)`, `(-8.309,+3.430)`, `(-8.592,+3.713)`. Source triangle line widths are zero, so use a printable silk width in a new footprint. Source silk end bars are at `x=±8.620`, `y=-1…+1` (lines 529082–529083).
- **Height unresolved:** ODB component properties say 6.38 mm maximum (lines 2085–2086), while its component attribute is 6.456 mm (line 2082). Shared-library metadata and CAP graphics are insufficient to assert the exact purchased Wieson part's 3D height. Obtain the current drawing/sample before freezing the enclosure.

For local visual review only, rendered vendor layers are at `/tmp/thor-j47-audit/MECH_DIMENSION_ASTRON.png`, `ASSEMBLY_BOTTOM.png`, and `PLACE_BOUND_BOTTOM.png`. These are temporary plots of the source lines, not manufacturer datasheet pages; the first plot uses board-global Cartesian Y up, so compare it through the normalization above. The plots and vendor source files must not be committed.

## Difference from the Samtec SHF candidate

The audited project file is `hardware/Thor.pretty/Samtec_SHF-113-01-L-D-SM.kicad_mod`, lines 5–33. It has the same 1.27 mm X pitch and numbering, but **0.740 × 2.540 mm pads at y=±2.160**. Switching to NVIDIA's lands moves each row center **0.230 mm inward** and extends each land **0.460 mm inward**, preserving the outer copper toes at `abs(y)=3.430`. Its 22.86 × 5.08 mm body drawing and 23.86 × 7.86 mm courtyard are unrelated to the Wieson body/envelope above. The two footprints are not equivalent.

Use an explicitly named Wieson footprint with provenance to this A02 reference layout. Keep Samtec as a separate, unapproved substitution. Before release: obtain the exact Wieson MPN and current drawing, check sample pin-1 orientation and ribbon continuity, verify both mating ends and retention, verify stencil/assembly requirements, and fit the real cable/housing. This audit resolves reference land geometry; it does not close those manufacturing or mating gates.
