# Hash the module that holds the code, not the shim left at its old import path

## Evidence — 2026-11-03

Moving the pin from cad-agent `29cc541` (v0.3.0) to v0.18.2 (`8e244f0`) and running `.venv/bin/python tools/validate_release.py` before regenerating anything reported:

```text
DeprecationWarning: cadagent.pcb moved to cadagent.electrical.pcb: import it from there ...
2port: slicer helper changed since measurement
2port: geometry helper changed cadagent.geometry
4port: slicer helper changed since measurement
Release snapshot stale: regenerate reports, then validate_release.py --record
```

cad-agent v0.5.0 to v0.9.0 moved seven modules this project imports (`pcb`, `pcb_routing`, `fasteners`, `render`, `markings`, `slicer`, `mesh3mf`) into domain packages. The old paths still import, through a one-line shim that warns. The evidence code hashed `Path(importlib.import_module('cadagent.markings').__file__)` (and the same for `slicer` and `fasteners`), which after the move is the shim's file.

## Cause

A shim's bytes do not change when the code it re-exports changes. Evidence bound to it would stay "current" across a real change to the marking, slicer or fastener helpers, which is the opposite of what the hash is for. The staleness reported above came from `cadagent.geometry`, which did not move.

## Corrective rule

Import and hash cad-agent modules by their current paths: `cadagent.electrical.pcb`, `cadagent.electrical.pcb_routing`, `cadagent.mechanical.fasteners`, `cadagent.mechanical.markings`, `cadagent.manufacturing.slicer`, `cadagent.manufacturing.mesh3mf` and `cadagent.publish.render`. After a cad-agent upgrade, run the project's imports with `-W error::DeprecationWarning`; any warning means an old path is still in use. Regenerate every report that records a library hash, then re-record the release manifest.

## Limits

This is about evidence binding only. Moving the import paths changes no geometry or check result. A hash still says only which helper bytes produced a report, not that the helper is correct.
