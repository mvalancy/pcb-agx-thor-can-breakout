# Progress log

## 2026-10-26 — Interface investigation

The original NVIDIA Thor P4071 A02 carrier design archive is available locally. J47 carries bus-side CAN signals; protection will be designed around the onboard transceivers. Samtec FFSD-13-D-04.00-01-N is a 101.6 mm, 26-position socket-to-socket ribbon candidate listed by DigiKey; the Wieson mating dimensions and cable pin mapping still need verification.

The local review site uses cad-agent's existing template. Reusable PCB support will be developed in a clean worktree because the existing cad-agent checkout contains unrelated FEA edits.

## Two variants and protection selection

Both two-port and four-port versions are now in scope. The four-port version will not be labeled IGX compatible until the specific IGX carrier pinout is checked. IGX product names cover different carriers, and the AURIX net labels in an older generic schematic do not establish the installed MCU.

Bourns CDSOT23-SM712 is the provisional suppressor: +12/-7 V working range and +20/-12 V maximum clamp at 5 A (8/20 µs), 75 pF typical. It has more voltage margin against the TJA1463 than generic 24 V CAN TVS parts. This narrows allowable sustained bus voltages and still needs waveform tests. A direct sustained 24 V miswire is not covered. JLC/LCSC identifier C404012 is manufacturer-specific; lookalike MPNs from other manufacturers are not approved substitutions.

Samtec SHF-113-01-L-D-SM provides a documented FFSD-compatible prototype header footprint. The requested exact Wieson part remains a release gate until its drawing/procurement is resolved. The interface uses the same 26-position male 1.27 mm arrangement; this does not yet prove physical mating to Thor.

## Iteration rounds: sourced connectors and cable retention

Both layouts were fully routed and reached zero ERC/DRC/parity before the sourcing refinement. Assmann A-DS09A/KG-T2S / C3127392 now replaces the generic DE9 placeholder, with exact shell-hole corrections. That change triggered fresh clearance and thermal checks; fixes and reruns are tracked in the iteration register.

The enclosure now has a dedicated rear chamber, separate replaceable clamp, captive M3 nuts, hard compression stops and silicone-pad space. The first clamp collision screen caught3.068445mm³ of ribbon/support overlap; the channel was widened and both variants then passed the modeled collision checks. Native PCB STEP, cable path, nuts, base/lid and clamp are checked together. Physical pull testing remains pending.

The status page now embeds schematics, PCB layers, assembly drawings and housing views through a new reusable cad-agent workbench. PCB report freshness, qualification gates and JLC CSV validation are toolkit features, with regression coverage. The J501 repository's prerelease/package/readme pattern is the reference for this project's release structure.

## Exact Wieson J47 recovered

The native NVIDIA A02 ODB/Allegro archive resolves the actual J47 lands and pin numbering. All26pads were cross-checked between the ASCII extraction, ODB package and placed copper. The default board now uses Wieson AC2800-0011-022-H0 with0.74×3.00mm pads at rows±1.93mm; the old Samtec candidate used shorter pads. Both boards are being rerouted and fully rechecked. The source CAP feature is not treated as proof of a polarizing key. Procurement, current manufacturer height and physical FFSD cable mating remain open.

## Recessed hardware and labeled lid iteration

Ports now have 42 mm pitch; PCB widths are 93 and 177 mm. The housing uses six heat-set inserts, M3×20 lid screws, M3×6 clamp screws and recessed socket heads. A perimeter tongue-and-groove joint replaces the short side keys. The top carries port labels, complete CAN pin mapping, A1 development revision and github.com/mvalancy.

Original Assmann drawing-based mating models include female connectors, backshells, thumbscrews and representative cables. Their seating assumptions remain visible. Maximum-width hoods leave 7.7 mm between adjacent ports. Manufacturer STEP downloads were unavailable through normal access; no access gate was bypassed. McMaster's browser session requires login for CAD. Current public catalog data supports the selected insert's 4.3 mm length and maximum 4 mm pilot; received-part fit remains a coupon test.

The first rebuild exposed crossed ground vias after rerouting and a tangent boss/wall contact that produced non-watertight STL edges. The via positions were corrected, and bosses now overlap the walls rather than just touching. Fresh electrical and mesh checks follow each correction.

## Validation and publication packaging

Both widened boards pass native ERC/DRC with no unconnected items or schematic-parity findings. Both mechanical variants pass modeled zero-intersection checks after the lower lid sleeve correction. Final images are rendered from exported STEP readbacks. Seven printable parts include the base/lid pairs, common clamp, insert/counterbore coupon and port coupon. Physical print, insert pull-out, cable pull/creep, actual mating and CAN protection tests remain open.

The reusable cad-agent changes are public in [PR1](https://github.com/Valpatel/cad-agent/pull/1), with 139 tests passed and five skipped. The exact connector resources and Wieson audit are in [KiCAD_Libs PR4](https://github.com/mvalancy/KiCAD_Libs/pull/4). Project packaging separates both PCB variants from the printable housing bundle; automated CI will validate the committed evidence and release bytes.

The public MIT repository is now available at [pcb-agx-thor-can-breakout](https://github.com/mvalancy/pcb-agx-thor-can-breakout). Headless Chrome verified embedded lid drawings and a 13-part interactive assembly with no JavaScript exceptions. Both variants' 13-part scene assets return HTTP 200. Clean-checkout artifact validation and GitHub CI verify the publication package separately from the working directory.

## A1 review — current state

The paired routes, TVS positions and ground return have been redesigned and rechecked. Both native boards have zero ERC/DRC, unconnected and parity findings. The 26-pin independent transcription, DE9/TVS/link semantics, JLC-format assembly checks, pair routing and native fabrication profile pass. JLCDFM itself still requires sign-in and has not issued a report.

The enclosure rebuild corrects an improper mirrored PCB frame, replaces the lid with a graphical DE9 pinout and retains the keyed seam, recessed insert hardware and padded clamp. All product renders and shared viewer assets are regenerated from exported solids. NVIDIA source screenshots and provenance are linked from the root README. Curated folder guides replace generic file tables.

Shared cad-agent now provides panel markings, routing analysis and consistent navigation in addition to PCB evidence, reports and the interactive viewer. Its combined suite passed 153 tests with five skips. A1 changes follow the requested development-branch and PR-into-main workflow; historical A0 releases are superseded. Physical and supplier qualification remain open.

A1 is published for review in [project PR #1](https://github.com/mvalancy/pcb-agx-thor-can-breakout/pull/1), targeting `main`. Its GitHub validation job passed and built the three engineering packages. A separate clean checkout reproduced the local ZIP checksums exactly. Browser review confirmed both 13-part scenes, the new lid, all report badges current, working navigation and no JavaScript exceptions.

## Prototype-area and mounting iteration — in progress

The PCB is extended to 90 mm depth, with 120 / 324 isolated prototype pads, gated power taps and clearer controls. Two recessed M3 side ears and filleted rear insert supports are being added. Electrical and mechanical checks, render/viewer regeneration and final PR merge are in progress; earlier results above describe the previous geometry.

The extended native boards now pass ERC/DRC, connectivity, parity, CAN pair/return-plane, fabrication and isolated-pad checks. A lid mesh failure from overlapping bold letters was reproduced by a small cad-agent regression, then corrected by fusing each text label before engraving. The shared suite now reports 155 passed and five skipped; both housings are rebuilding with that correction. PR #1 is merged into main, and GitHub browser review confirmed the root README and all five existing product/proof images load.

The old `dev/a1-routing-lid-review` branch has been deleted locally and remotely after its merge. The final thickness audit extended the structural checks to the lid counterbore rings, roof engraving, sleeves and blind-hole floors; corner boss diameter increased to 10.6 mm. A third native housing build is underway. The exploded-layout review now visibly shows all six enclosure screws; the clamp is offset to the side for clarity.

## Prototype and mounting iteration — validation complete

Both 90 mm-deep boards pass ERC/DRC, connectivity/parity, independent pin/power/prototype checks, paired CAN/reference-plane checks and the native fabrication-rule probe. Both reinforced housings pass collision checks and all 23 assembly-path/clearance trials per variant. Seven printable parts export as watertight STL/3MF and fit a 256 mm bed. The minimum audited structural web is 2 mm; the lid counterbore ring is 2.1 mm.

Final renders, both 13-part viewer scenes, drawings and folder guides are refreshed. Desktop/mobile browser checks found no broken images or JavaScript exceptions, and all 78 review/scene assets returned HTTP 200. The engineering packages pass source/artifact validation. JLCDFM still requires sign-in; no physical qualification or production order has occurred.

## Merged shared tooling and complete native checks

The project now pins merged cad-agent v0.3.0, including upstream PR1 and PR14. Its stricter evidence review exposed KiCad default-disabled checks and filtered severities. Both native projects now enable those checks, and the export command uses `--severity-all`. Four bare-pad courtyard outlines were added per board; a two-port termination endpoint was centered by 1 nm. Both ERC/DRC reports have zero findings, zero ignored checks and zero exclusions; no waivers are used. The relevant merged-toolkit evidence, marking and fastener tests pass (22 tests).

Fresh KiCad STEP exports had different presentation ordering, but CadQuery BREP readbacks were byte-identical to the previously verified solids for both variants. Those verified STEP bytes were retained, so the current mechanical screens, renders and viewer geometry remain applicable. The previous shared-toolkit counts above describe earlier snapshots.

Merged project feature branches are deleted locally and remotely. GitHub automatic branch deletion is enabled, and a plain `dev` follows `main` after integration.

## 2026-10-27 — Four broad corner mounts and finer viewer zoom

Rebuilding both bases with four 26 mm-wide mounting ears near the corners, R4 roots and the existing 7 mm thickness. Drawings, assembly checks, meshes and viewer assets are being regenerated; older renders remain visible until that completes. The shared viewer is being updated to use one-quarter zoom sensitivity, with browser measurement and independent upstream review before integration.

Both four-mount housings are rebuilt and pass collision checks. Measured wall-root sections are 30.1344 mm wide; all four M3 heads, shanks and driver paths clear the assembled housing. Each variant passes 29 assembly-path/clearance trials. Seven printable parts are watertight and their 3MF files read back correctly. All assembly/part renders, dedicated mounting-detail views, dimensions and the two 13-part interactive scenes are refreshed. The new overall widths are 149.2 and 233.2 mm; thickness remains 7 mm at the mounting ears.

Shared zoom [PR18](https://github.com/Valpatel/cad-agent/pull/18) is merged after independent review and passing CI. The project pins its merged commit. Browser measurement confirms a 100-pixel wheel event changes camera distance by 1.29059% (previously 5.26316%), with continuous small deltas and reversible movement. Both current assembly scenes load without JavaScript exceptions. The shared local suite passed 388 tests with 14 optional skips. Physical strength and installation torque remain unqualified.
