# Funded no-mutation inheritance gate

37 ReleaseSafe tests pass, including 3 new gates and 34 imported core regressions. Ten controlled same-cell/adjacent-cell cases cover allocations (0,0), (.25,.25), (.75,.25), (1,0), (0,1). Child allocations exactly copy the parent; RNG unchanged; support, biomass, credit and water match existing donor-funded arithmetic. Five refused cases preserve both cells and stats exactly: invalid slot, insufficient biomass, insufficient credit, full destination, over-capacity destination.

**Not exact real-number tissue closure:** the selected ordinary birth yields +1.862645149230957e-9 carbon and +4.656612873077393e-10 support summed represented residual. Tests verify existing subtraction/funding operations, not a repaired accounting law. No resource top-ups or tolerance relaxation introduced. Water totals tested within1e-16 for these cases.

Prescribed storage-capacity shrink returns existing water to the old experimental liquid_return pool. This proves only the existing ownership helper, not an approved physical destination, soil integration, hydrology, death/grazing/motility lifecycle or mutated birth. Invalid allocation sums are rejected by validCell; reproduce itself assumes validated input. No mutation, production or schema changes.

Command: Zig0.13.0 `zig test src/qa_root_inheritance.zig -O ReleaseSafe`.
