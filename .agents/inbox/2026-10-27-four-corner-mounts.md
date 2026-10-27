# Spread mounting loads with broad roots at the corners, not thickness alone

2026-10-27: the user judged the two 13 mm-wide central side ears too small despite acceptable 7 mm thickness. Both bases now use four 26 mm-wide ears at Y14/Y90, R4 roots spreading to 34 mm at the wall, and the same 7 mm thickness. Their screw centers move from 8 to 10 mm outside the side wall; counterbores remain Ø6.4 × 3.3 over Ø3.4 M3 clearance holes.

Cause: the original check enforced minimum remaining webs but did not address the user's mounting footprint or distribute attachment points near all four corners. The revised build measures plastic in a 0.2 mm section 0.5 mm outside each wall, away from the wall itself, and requires at least 28 mm effective root width. Assembly checks cover driver and socket-head/shank clearance at every mounting position. Current numerical results are bound to source in the mechanical reports.

Corrective rule: assess plan-view width, wall attachment and mounting-point placement separately from thickness. Use positive wall overlap and filleted roots, and inspect all mounts in the delivered STEP, printable mesh, product renders and interactive scene. Do not infer printed strength or torque limits from these geometry checks.

Workflow evidence: `git switch -c dev/chunky-corner-mounts origin/main` failed because the retained `dev` branch occupies that ref path. Use `feat/chunky-corner-mounts`, PR into main, delete the feature branch after merging, and fast-forward plain dev.

Final dated evidence: both mechanical reports pass, with `mount_tab_quantity: 4`, `mount_tab_width_mm: 26`, `mount_tab_root_radius_mm: 4` and four measured root-section widths of `30.1344`. `check_mechanics.py` reports `2 True []` and `4 True []` with 29 trials each. The shared mesh exporters report seven watertight STL/3MF pairs. The viewer reports the updated 149 / 233 mm assembly widths and no JavaScript exceptions.
