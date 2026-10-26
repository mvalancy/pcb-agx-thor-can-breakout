# Mating DE9 connector, hood and screw clearances

Checked 2026-10-26. Use **42 mm port pitch** for the reference assembly below. This establishes real orderable hardware and drawing-based clearance inputs; **full mating and screw engagement remain unverified** because the drawings omit two essential assembly datums. Do not turn a nonintersecting CAD view into a hardware-fit approval.

## Orderable reference pair

| Item | Manufacturer part | Order code / snapshot |
|---|---|---|
| Female DE9, solder cups, unthreaded flange | Assmann **A-DF 09 LL/Z** | [DigiKey AE11063-ND](https://www.digikey.com/en/products/detail/assmann-wsw-components/A-DF-09-LL-Z/5051922), 26,570 shown; $0.39060 each at 50 |
| Black hinged hood, clamp and two #4-40 thumbscrews | Assmann **A-FT 09** | [DigiKey AE11002-ND](https://www.digikey.com/en/products/detail/assmann-wsw-components/A-FT-09/1241834), 18,288 shown; $1.01940 each at 50 |

The female is size E/1 with a 24.99 mm screw pitch; the hood is specified for 9-position DE9/size E and includes its mating hardware. Combined snapshot is **$1.41 per cable end**, excluding cable, labor, shipping and tax. No parts were ordered. The female's current drawing recommends **28–30 AWG** conductors: this is a mechanical fit reference, not approval for a selected CAN cable gauge. See the [manufacturer product page](https://www.assmann-wsw.com/us/product/a-df-09-llz/).

## Exact drawing basis

All dimensions are mm. Vendor files are ignored under `references/vendor/mating-dsub/`; hashes and machine-readable measurements are in [mating-dsub-measurements.json](mating-dsub-measurements.json).

| Feature | Nominal / tolerance | Primary source |
|---|---|---|
| Hood width × height × axial depth | **33.8 ±0.5 ×14.8 ±0.5 ×33.3 ±0.5** | [ASS3205 CO rev02, 2018-07-30](https://www.assmann-wsw.com/uploads/datasheets/ASS_3205_CO.pdf), sheet **1/5**; local `ASS_3205_CO_A-FT09.pdf` |
| Hood screw pitch; cable aperture | **24.99 ±0.5**; **8.0** opening | Same sheet |
| Thumbscrew head diameter / axial length | **7.0 / 9.7** | Same sheet, separate screw detail; one-decimal dimensions default ±0.25 |
| Screw shaft diameter; total length | **2.6; 48.5** | Same detail |
| Screw axial chain, head rear → tip | **9.7 head +28.6 shaft +1.5 collar +8.7 threaded tip** | Same detail; #4-40 UNC |
| Female flange width / height / hole pitch | **30.81 ±0.25 /12.55 ±0.25 /24.99** | [ASS4884 CO rev12, 2024-01-16](https://www.assmann-wsw.com/uploads/datasheets/ASS_4884_CO.pdf), sheet **2/2**; local `ASS_4884_CO_A-DF09_LLZ.pdf` |
| Female front shell width / height / projection | **16.33 /7.9 /5.8** from front flange plane | Same sheet; keystone walls 10°; do not substitute flange width for shell width |
| Female rear insulator width / height | **19.20 /10.72** | Same sheet |
| Female flange → rear body / cup extension | **4.1 /3.1 ±0.38** | Same sheet; flange thickness itself is not separately dimensioned |

General female drawing tolerances are ±0.25 for one decimal and ±0.13 for two decimals unless locally overridden. The hood's rear taper, corner radii, connector capture groove, screw collar seat and screwdriver recess dimensions are **not fully dimensioned**. Their visual appearance can be approximated in an original model, but clearance calculations should retain the conservative full hood envelope. Local visual-review renders: `/tmp/aft09.png` and `/tmp/adf09.png`.

## Adjacent port and service access

Calculated gaps for two identical hoods, without PCB placement error:

| Port pitch | Hood gap, nominal / maximum hood width | Adjacent inner screw-head edge gap, nominal / conservative tolerance stack |
|---:|---:|---:|
| 35 | 1.2 /0.7 | 3.01 /2.26 |
| 40 | 6.2 /5.7 | 8.01 /7.26 |
| **42** | **8.2 /7.7** | **10.01 /9.26** |

Hood gap is `pitch−width`; inner screw-head gap is `pitch−24.99−7.0`, using 25.49 screw pitch and 7.25 head diameter for the conservative column. The actual mated screw centers are also constrained by the board connector's mounting pitch, so the latter is deliberately conservative. Add board/print/assembly position tolerances separately.

For review, show a **12 mm diameter finger-access cylinder** around each head and a **6 mm diameter straight tool shaft** extending 25 mm behind it. These are explicit project test gauges, not manufacturer requirements or proof that every hand/tool fits. Check each against its own hood, neighboring hoods, cables, lid and mounting surface; rotating only a screw's 7 mm physical envelope does not test finger access. The screw drawing does not specify a driver bit standard/size. Test actual tooling before setting tightening instructions.

The 8 mm aperture is not a validated cable-clamp range or a bend-radius specification. Show a representative 6 mm cable and retain an 8 mm cylindrical exit envelope; use the chosen cable's real minimum bend radius and strain-relief behavior before enclosing a cable bend.

## Mating depth and the housing wall

The Assmann drawings do not give the **mated flange separation** for this exact pair. A bounded **comparison case** is `g=6.73 ±0.38` (6.35…7.11): [TE 114-40010 revG §3.4, figure 4, sheet 4/12](https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocFormat=pdf&DocLang=English&DocNm=114-40010&DocType=Specification+Or+Standard&PartCntxt=5-747905-2) specifies this for its 9/15-position connectors. The [Positronic C005 revC1 catalog](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/8882/C005RevC1_HighPerfDsub_FA.pdf), **PDF page 14 / printed page 7**, independently draws the same facing-flange separation for shell sizes 1/2; local `Positronic_C005RevC1.pdf`, render `/tmp/positronic-p14.png`. **This is an engineering proxy, not an Assmann-certified mating range.**

Using the revised board male front-flange position `Y=−3.44`, housing outer wall `Y=−3.60`, outward direction toward negative Y (parent's planned Y=7.5 pin-row placement):

| Surface | Formula | Proxy-case range |
|---|---|---:|
| Female facing flange | `−3.44−g` | −9.79…−10.55 |
| Female shell nose, nominal projection | `−3.44−g+5.8` | −3.99…−4.75 |
| Female flange clearance outside wall | `g−0.16` | **6.19…6.95** |

The revised nearly flush male flange keeps the **female shell nose nominally outside the wall by 0.39…1.15 mm**; its flange and hood are farther outside. Including the female projection's ±0.25 mm tolerance reduces the minimum nose clearance to **0.14 mm**, before PCB/case/assembly tolerance. Distinguish this from the earlier recessed layout, which required the female shell to enter the window. If the hood has a front lip extending toward the board by `l` beyond the female facing flange, its wall clearance is `g−0.16−l`; `l` is not established by the hood drawing. At the deepest proxy case, requiring 0.5 mm wall clearance permits at most **5.69 mm lip projection**. Do not invent `l=0` and report a proven fit. Check the insertion path and all exposed screw shoulders, not merely the final pose.

## Screw engagement is an explicit open gate

The board connector's [ASS4888 CO rev10 drawing](https://www.assmann-wsw.com/uploads/datasheets/ASS_4888_CO.pdf), sheet 1/2, gives its installed #4-40 screwlock a **4.8 mm head height**; the 5.8 mm alternative belongs to **T2A**, not this T2S part. Its usable internal threaded depth is unspecified.

Define `c` as the cable thumbscrew's **thread-start/collar-front plane setback behind the female facing flange**, positive outward. Its nominal insertion beyond the board screwlock mouth is:

```text
e = 8.7 − (g + c − 4.8) = 13.5 − g − c
```

Over the proxy mating range, `e = 6.39…7.15 − c`. Including ±0.25 screw-tip and screwlock-height tolerances gives `e_min=5.89−c_max`, `e_max=7.65−c_min`. The source does **not** establish `c`, usable internal thread depth, lead-in loss, or the hood's collar retention travel. Therefore a numerical full-engagement or non-bottoming pass is currently impossible. In particular, assuming `c=0` would imply 6.4–7.2 mm insertion, longer than the 4.8 mm hex body; that assumption must not silently enter CAD.

For a dimensioned screw model, use thread-start plane `u=0`, with outward-positive local axis: collar `u=0…1.5`, shaft `1.5…30.1`, head `30.1…39.8`, and threaded tip `−8.7…0`. Translate this model by the measured `c` after assembly; until then expose `c` as an unresolved parameter. A sample check must establish seating, collar location, available turns and bottoming clearance with **both screws installed**. A visible overlap of simplified cylinders is only a reach illustration.

## CAD provenance and publication

No manufacturer STEP was successfully acquired. Assmann's female product page links its manufacturer catalog on TraceParts; that route presented bot verification, and it was not bypassed. TE publishes STEP links for an alternative hood **5748676-1**, jackscrew **747784-3**, and female **5-747905-2**, but direct downloads returned HTTP 403 here. Those files were not used and their dimensions must not be mixed into the Assmann assembly.

Use an **original parameterized Assmann reference model** based on the dimensioned values above, with unspecified details labeled as assumptions. Do not label it an official CAD model. No open redistribution license was found for the vendor documents; [Assmann's imprint §3](https://www.assmann-wsw.com/us/imprint/) reserves content rights. Keep downloaded drawings, catalog pages and their renders outside published assets; retain source links, factual measurements and provenance with the project's own model. This research does not grant or infer a vendor CAD license.
