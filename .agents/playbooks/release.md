# Validate before packaging

Run native ERC/DRC with parity, semantic connector checks, both mechanical builds, 3MF readback and the CI artifact checks. Update evidence only after reports are regenerated. Package each PCB variant separately and keep manual/consigned parts explicit. Keep prerelease status until sourcing, physical and electrical qualification gates are actually closed. Read every failed report; do not weaken a rule just to turn it green.

After prototype-area changes, also run `check_prototype.py` with KiCad Python, then regenerate `draw_controls.py`. Require zero assigned nets on the free grid, correct gated rail mapping, both-layer copper exclusion and no bare-pad BOM/CPL entries. Mechanical path checks consume that grid report to check the documented component and trimmed-lead envelopes. Inspect exploded renders for every assembly screw and mounting ears; a six-screw source compound is not sufficient if the renderer omits it.

Use the merged cad-agent evidence checker and run KiCad ERC/DRC with `--severity-all`. Enable the checks KiCad disables by default, using `apply_fab_rules.py`; current boards require no ignored checks, exclusions or waivers. Do not hide a new finding with a blanket waiver. After merging the validated feature PR, delete its local and remote branches. Keep only a plain `dev` following `main` when ongoing development needs one.

A retained branch named `dev` prevents Git refs named `dev/<topic>`. Use `feat/<topic>` for project work and delete it after merging. For mounting changes, check actual fused root sections, every mounting screw/driver path, both variant meshes and the 3D scene-to-print comparison. Refresh all rendered views and mechanical dimensions before publishing.

After lid-artwork changes, run `check_lid_markings.py` and shared `cad-agent slice` followed by `check_lid_slicing.py` for both current STLs before recording the release manifest. Verify effective printer/nozzle/material/layer settings and inspect the actual toolpath proofs. Refresh both lids, paint references, viewer scenes and renders; do not claim physical print qualification from layout or slicing reports.
