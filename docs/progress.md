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

Ports now have 42 mm pitch; PCB widths are 93 and 177 mm. The housing uses six heat-set inserts, M3×20 lid screws, M3×6 clamp screws and recessed socket heads. A perimeter tongue-and-groove joint replaces the short side keys. The top carries port labels, complete CAN pin mapping, A0 development revision and github.com/mvalancy.

Original Assmann drawing-based mating models include female connectors, backshells, thumbscrews and representative cables. Their seating assumptions remain visible. Maximum-width hoods leave 7.7 mm between adjacent ports. Manufacturer STEP downloads were unavailable through normal access; no access gate was bypassed. McMaster's browser session requires login for CAD. Current public catalog data supports the selected insert's 4.3 mm length and maximum 4 mm pilot; received-part fit remains a coupon test.

The first rebuild exposed crossed ground vias after rerouting and a tangent boss/wall contact that produced non-watertight STL edges. The via positions were corrected, and bosses now overlap the walls rather than just touching. Fresh electrical and mesh checks follow each correction.

## Validation and publication packaging

Both widened boards pass native ERC/DRC with no unconnected items or schematic-parity findings. Both mechanical variants pass modeled zero-intersection checks after the lower lid sleeve correction. Final images are rendered from exported STEP readbacks. Seven printable parts include the base/lid pairs, common clamp, insert/counterbore coupon and port coupon. Physical print, insert pull-out, cable pull/creep, actual mating and CAN protection tests remain open.

The reusable cad-agent changes are public in [PR1](https://github.com/Valpatel/cad-agent/pull/1), with 139 tests passed and five skipped. The exact connector resources and Wieson audit are in [KiCAD_Libs PR4](https://github.com/mvalancy/KiCAD_Libs/pull/4). Project packaging separates both PCB variants from the printable housing bundle; automated CI will validate the committed evidence and release bytes.
