# Third-party material

The original electronics, enclosure, scripts, documentation and generated design files in this project use the [MIT license](LICENSE).

`hardware/Thor.pretty` includes a small pinned subset of the KiCad 10.0.1 standard footprint library, plus two derivatives. Those standalone library files remain © KiCad library contributors, **CC BY-SA 4.0 with the KiCad design exception**. The Assmann and XFCN files are derivatives of the standard D-sub and pin-header footprints respectively. Their source geometry was changed only as documented in the connector audit. The Samtec SHF footprint is original project work, available under MIT; it is also offered to KiCAD_Libs under that repository's CC BY-SA terms.

See the [KiCad library license](https://www.kicad.org/libraries/license/) and the accompanying license documents in `hardware/Thor.pretty/`. The library exception permits designs and their generated files to use a different license; it does not relicense redistributed library collections.

STEP exports include standard KiCad 3D geometry under the same library design exception. These are nominal mechanical models, not manufacturer-certified models for substituted parts. `cad-agent` is separately MIT licensed. Dependency packages keep their own licenses.

Full NVIDIA, Samtec, Bourns, Assmann and distributor PDFs/archives are referenced by URL and hash, not redistributed or relicensed here. Small NVIDIA pinout excerpts in `docs/proof/` are included for engineering review at the project owner’s request. They remain © NVIDIA, are excluded from the MIT grant, and have source/capture provenance in `docs/proof/provenance.json`. No vendor endorsement is implied.
