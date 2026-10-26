# Enclosure hardware evidence

Checked 2026-10-26. [McMaster 94459A130](https://www.mcmaster.com/products/94459A130/) lists a brass M3×0.5 heat-set insert, 4.3 mm installed length and maximum 4 mm hole diameter. The 4.7 mm OD and 5.1 mm minimum material reference comes from cad-agent's vendored bd_warehouse heatset_nut_parameters.csv, not a newly downloaded manufacturer CAD model. Validate the received part in the supplied 3.8/3.9/4.0 mm coupon.

The scoped headless Chrome session reached a McMaster login request before CAD access. No credentials were requested, no download was acquired and no access control was bypassed. Models are original envelopes imported from cad-agent.fasteners; they are not manufacturer STEP files. M3 socket-head screw envelopes use Ø5.5 × 3 mm heads, 20 mm length for the lid and 6 mm for the clamp. Purchase screws matching those dimensions; exact stocked supplier SKU is not yet locked.

The lid counterbore is Ø6.4 × 3.3 mm; clamp uses the same bore. Four lid inserts sit 0.1 mm below the Z7.4 supports, and two clamp inserts sit 0.1 mm below Z16.2 stops. The reports calculate tip clearance and threaded axial overlap. Heat-set knurl interference with the printed pilot is intentional and separately reported. Physical installation, torque, pull-out and service-life tests remain open.
