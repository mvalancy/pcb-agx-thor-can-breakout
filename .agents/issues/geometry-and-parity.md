# CAD can look correct while its interface is wrong

Symptoms: parity warnings with no unrouted nets; clearances fail after connector substitution; cable overlaps a support; board STEP appears to collide only at the PCB itself; SWIG object failures on a second board.

See [dated incident](../inbox/2026-10-26-thor-hardware-validation.md), [interface authority](../domains/thor-interface.md) and [release procedure](../playbooks/release.md).

A passing continuity DRC does not establish paired routing or an uninterrupted return plane. Use the [CAN route audit](../inbox/2026-10-26-can-routing-is-not-connectivity.md). A zone-to-zone ratsnest may indicate vias joining two isolated islands; inspect [actual connected regions](../inbox/2026-10-26-ground-islands-need-a-real-bridge.md).

A mirrored PCB STEP can pass symmetric outline collision checks. Preserve handedness and inspect asymmetric features as described in the [proper transform lesson](../inbox/2026-10-26-preserve-pcb-handedness.md).
