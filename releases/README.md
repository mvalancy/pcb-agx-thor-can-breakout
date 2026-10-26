# Release packages

[Project](../README.md) · [Assembly](../ASSEMBLY.md) · [JLCPCB instructions](../docs/manufacturing.md)

Use the matching assets from [GitHub Releases](https://github.com/mvalancy/pcb-agx-thor-can-breakout/releases). A0 is an engineering **pre-release**, not permission to order production quantities.

| Asset | Contents |
|---|---|
| `thor-A0-2port-pcb.zip` | Native KiCad project/library, Gerber/drill review ZIP, schematic, layers, BOM/CPL options, reports and instructions |
| `thor-A0-4port-pcb.zip` | Same structure for the four-port engineering variant; IGX compatibility remains open |
| `thor-A0-housings.zip` | Both base/lid pairs, universal clamp, fit coupons, STL/STEP/3MF, illustrated assembly and hardware list |
| `SHA256SUMS` | Hashes of each downloadable ZIP |
| `manifest.json` | Source and artifact hashes, tool versions and qualification status |
| `release-notes.md` | What changed, which checks ran and remaining gates |

`python tools/package_release.py` creates the ZIPs locally after validation. ZIPs are release assets, not recursively checked-in copies. Each archive retains repository-relative paths and contains a root README with the upload/assembly route. Inner `SHA256SUMS` lists every payload member except the checksum file itself. Physical fit, cable retention, supplier assembly and electrical protection remain explicit pending fields.

To publish a later version: rebuild, check, record the manifest, commit and push; then tag `revA0` (or the next revision). CI validates committed evidence and builds assets, and the tag workflow publishes a prerelease. A final production release needs recorded hardware qualification and review of every open gate.
