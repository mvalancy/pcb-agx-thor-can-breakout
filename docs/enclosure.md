# Enclosure design

A keyed, screw-fastened housing with a separate padded ribbon clamp and enough port spacing for mating DE9 backshells. Both variants share the same seam, hardware and graphical lid language.

![Assembled two-port housing with mating connectors](../preview/2port-assembled.png)

## Lid and port identity

![Engraved male DE9 pinout and port badges](../preview/2port-lid.png)

The roof carries a numbered **male mating-face** DE9 diagram, CAN-H/L, ground and shield callouts, unconnected pins, port badges, revision and `github.com/mvalancy`. Recessed markings are 0.4 mm deep in a 2.4 mm roof. Light paint fill is optional. The same shared cad-agent vector primitive generates the engraving, paint reference and [SVG proof](../preview/2port-lid-artwork.svg).

Port badges follow the physical PCB orientation. CAN0 is at the right in the housing's top/front coordinate view; the native KiCad PCB view has the opposite X direction after a proper assembly rotation. The four-port model labels its extra channels **RES2 / RES3**.

## Serviceable mechanical details

![Exploded housing](../preview/2port-exploded.png)

| Feature | Nominal design |
|---|---|
| Port spacing | 42 mm centers; 9.8 mm plastic rib between openings |
| Mating clearance | 7.7 mm between maximum-width modeled backshells |
| Keyed seam | 1.4 mm tongue width, 1.6 mm height, 0.25 mm clearance |
| Lid hardware | Four M3 × 20 screws, heat-set inserts, Ø6.4 × 3.3 mm counterbores |
| Ribbon clamp | Replaceable bar, two M3 × 6 screws and heat-set inserts |
| Cable contact | Two 0.8 mm silicone pads; 1.8 mm hard-stop gap |
| Pilot selection | Print the 3.8 / 3.9 / 4.0 mm insert coupon first |

![Open assembly and ribbon retention](../preview/2port-open.png)

The mating references include Assmann A-DF 09 LL/Z female connectors, A-FT 09 backshells, #4-40 thumbscrews and cable envelopes. Their dimensions come from drawings; hood capture and screw engagement require physical samples. [Mating audit](../research/mating-dsub-clearance.md).

## Build and inspect

Use the matching base/lid pair plus one common clamp. [Downloads](../exports/README.md) include STL, STEP and 3MF; [ASSEMBLY.md](../ASSEMBLY.md) gives print orientation, hardware, pads and installation. Print the port and insert coupons first. Target a 10 N / 60 s ribbon pull test with continuity checked before and after; this test has not been performed.

CAD checks cover solid validity, meshes, fastener axial stacks, native PCB collisions and assembly paths. They do not establish plastic creep, insert pull-out, cable retention, exact connector fit or allowable screw torque. A0 housings used an improper mirrored PCB frame and are superseded by A1's proper rotation.

[Two-port dimensions](../exports/2port/enclosure-plan.svg) · [Four-port dimensions](../exports/4port/enclosure-plan.svg) · [Local interactive viewer](http://localhost:8765/_cadagent/kit/viewer.html)
