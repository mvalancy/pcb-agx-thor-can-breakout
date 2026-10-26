# Engineering contract

Use KiCad for electrical source and CadQuery for enclosure geometry. `cad/parameters.json` owns dimensions; `hardware/interface.json` owns connector maps and variant definitions. Rebuild both two- and four-port versions after shared changes. Never infer a populated production board from a generic NVIDIA base schematic. Never advertise IGX compatibility without the specific carrier revision pinout.

Do not order or claim production readiness from ERC/DRC alone. Record unresolved header mating, assembly sourcing, hardware fit and protection tests in the release checklist. Do not commit vendor PDFs, private machine details, or credentials. Follow `.agents/WRITING-IT-DOWN.md`. Preserve unrelated edits in sibling repositories.
