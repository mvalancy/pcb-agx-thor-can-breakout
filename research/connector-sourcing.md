# Connector sourcing and footprint audit

Checked 2026-10-26. No board or footprint changes were made during this research. Prices and stock are snapshots, not reserved supply. Manufacturer drawings were visually inspected; distributor category text alone was not used to approve dimensions.

## Male right-angle DE9

**Preferred sourced alternative: Assmann WSW `A-DS 09 A/KG-T2S`.** It includes male contacts, board locks and installed #4-40 screwlocks. Order codes: [LCSC C3127392](https://www.lcsc.com/product-detail/C3127392.html), [JLC C3127392](https://jlcpcb.com/partdetail/Assmann_WSW_Components-A_DS_09_A_KGT2S/C3127392), or [DigiKey AE10968-ND](https://www.digikey.com/en/products/detail/assmann-wsw-components/A-DS-09-A-KG-T2S/1241804). DigiKey displayed 68,656 available and $0.75144 each at quantity 90. JLC lists wave soldering and Economic/Standard PCBA eligibility; a listing does not establish stock allocated to an assembly order or Basic-part pricing.

The manufacturer source is **ASS 4888 CO, rev10, dated 2023-10-27, sheet 1/2, Male**, linked from the [LCSC datasheet page](https://www.lcsc.com/datasheet/C3127392.pdf) and [JLC's copy](https://jlc-prod-smt.oss-eu-central-1.aliyuncs.com/smtDataManualFile/8590905312536969216-C3127392.pdf). Vendor reviewer copies are temporary and are not repository assets.

No exact, fully verified drop-in replacement for the generic footprint was established. The Assmann part has small but real differences, documented below.

### Coordinate convention and proposed changes

The audited file is `hardware/Thor.pretty/DSUB-9_Pins_Horizontal_P2.77x2.84mm_EdgePinOffset7.70mm_Housed_MountingHolesOffset9.12mm.kicad_mod`. Pin 1 is `(0,0)`, pins 1–5 run in +X, and +Y points toward the mating face. **The actual file's shell holes are at Y = +1.42, not −1.42.** Local front-face datum is Y = 10.94; the flange's rear datum is Y = 10.54.

| Item | Existing file | Assmann drawing / proposed result |
|---|---:|---:|
| Signal pitch / row spacing | 2.77 / 2.84 mm | Same; retain all nine signal centers |
| Signal drill | 1.00 mm | 1.00 mm; retain |
| Shell-hole X centers | −6.960, +18.040 mm | −6.955, +18.035 mm; 24.99 ±0.05 mm pitch |
| Shell drill | 3.20 mm | 3.05 mm recommended; change both drills |
| Face → near signal row | 8.10 mm | 8.10 mm; retain signal-to-face datum |
| Face → far row, containing pin 1 | 10.94 mm | 10.94 mm, derived as 8.10 + 2.84 |
| Face → shell-hole center | 9.52 mm | 9.5 mm printed dimension |
| Pin 1 → shell-hole Y | +1.42 mm | +1.44 mm from the printed dimensional chain; see rounding caveat |

The shell-hole drawing depicts the mounts between the signal rows, without an independent Y callout in the recommended PCB layout. The 9.5 mm dimension has the drawing's general one-decimal tolerance, ±0.25 mm. Thus +1.44 mm is the literal nominal chain, while +1.42 mm is the geometric midpoint; their 0.02 mm difference is a rounding ambiguity, not evidence of a substantial displacement. Use the documented nominal chain in a part-specific footprint and verify a sample. Retain 4 mm shell copper pads unless another layout constraint requires resizing. Do not shift the signal rows by 0.4 mm: the footprint's “7.70” name describes a different face datum from the 8.10 mm front-face dimension.

### Body and enclosure geometry

| Feature | Assmann drawing | Consequence relative to current generic geometry |
|---|---:|---|
| Flange width | 30.81 ±0.25 mm | Generic width 30.85 mm; new X envelope −9.865…20.945 |
| Flange height | 12.55 ±0.25 mm | Compare against the 14 mm case opening and tolerances |
| Front shell width / height | 16.92 / 8.36 mm | Generic plan width is 16.30 mm; widen by 0.62 mm |
| Front shell projection from face | 6.1 mm | Generic is 6.0 mm; new nose Y = 17.04 |
| Overall axial depth | 18.6 mm | Derived rear-body Y = −1.56, versus generic −1.80 |
| Screwlock hex across flats / head projection | 4.75 / 4.8 mm | Replace generic 5 × 5 mm depiction |
| Contact tail projection | 3.2 mm | Include under-board clearance |
| Connector axis above PCB | **Not independently dimensioned** | 6.275 mm is an inference only if the depicted seating plane is flush with the flange's lower edge; current CAD assumes 6.3 mm |

These dimensions support a better envelope, but do not specify all corner radii, flange thickness or seating tolerances. Keep physical-fit verification open and obtain the manufacturer's 3D model or measure a sample before treating the axis height and complete shell solid as exact. The drawing's “7.2mm Footprint” caption should not replace the individually dimensioned face/row distances.

## Inexpensive 2.54 mm vertical male headers

Keep the **order code together with the manufacturer name and complete description**: the short BOOMELE names also appear on female sockets and IDC products.

| Use | Exact part / order code | Manufacturer drawing and fit |
|---|---|---|
| 2 × 7, 14 contacts | BOOMELE `2.54-2*7P针` (JLC English `2.54-2*7PPin`), **C71397** | [JLC part](https://jlcpcb.com/partdetail/2.54-2%2A7P/C71397), [manufacturer sheet](https://www.lcsc.com/datasheet/C71397.pdf): 2.54 mm grid, 0.64 mm square pins, Ø1.00 mm holes; same land pattern as the existing 2×7 footprint |
| 2 × 3, 6 contacts | BOOMELE `2.54-2*3P针` (English `2.54-2*3P`), **C65114** | [LCSC part](https://www.lcsc.com/product-detail/C65114.html), [manufacturer sheet](https://www.lcsc.com/datasheet/C65114.pdf): same grid, pin size and Ø1.00 mm holes; same land pattern as the existing 2×3 footprint |
| 1 × 2, 2 contacts | XFCN `PZ254V-11-02P`, **C492401** | [LCSC part](https://www.lcsc.com/product-detail/C492401.html), [manufacturer sheet](https://www.lcsc.com/datasheet/C492401.pdf): 2.54 mm pitch, 0.64 mm square pins, **Ø1.02 mm recommended holes**; enlarge the existing 1.00 mm drills to follow the sheet exactly |

The BOOMELE sheet supplied for both SKUs is dated 2026-01-16, document `2.54-2*NP H2.54 L11.2`. It specifies 2.54 mm insulation height, 5.8 ±0.2 mm exposed mating pins, 2.8 ±0.2 mm tails, and 5.0 ±0.1 mm body width. This supersedes the coarse 6/3/2.5 mm figures still displayed on some product pages. Its generic `n` length notation is imprecisely described: use **columns per row** for length, giving 17.78 mm for 2×7 and 7.62 mm for 2×3, and confirm supplied count by SKU.

The XFCN sheet, rev A1 dated 2024-06-11, specifies a 5.08 × 2.50 mm body, 2.50 mm insulation height, 6.1 ±0.20 mm mating pins and 3.0 ±0.20 mm tails. Vendor PDFs are retained only in the ignored local reference cache.

All three are simple unshrouded headers and all have JLC wave-solder listings. The XFCN [LCSC catalog snapshot](https://lcsc.com/products/Pin-Headers_644.html) showed $0.0135 at quantity 50; obtain current BOM pricing for the complete set. For a 50-board run, confirm orderable quantity, assembly handling and the required separate shorting shunts before release. No parts were ordered.
