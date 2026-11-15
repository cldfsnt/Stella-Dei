# Exact legacy scatter operation ledger

Independent NumPy scalar-f32 reproduction of the frozen natural60 single liquid pass, NOT machine-SIMD or concurrent scheduling equivalence. No replacement solver. Actual input hash retained; independently verified ALL40962 neighbor rows map raw getNeighbours slots into sendWater order[0,3,1,4,2,5]. Each arithmetic operation rounds explicitly to f32; exact accounting uses integer units2^-149, not approximate subtraction of whole-world totals.

For every width4/16 and forward/reverse case the following identity holds EXACTLY as integers:

`world_change = receiver_add_rounding − six_edge_sum_rounding + donor_subtraction_rounding`.

Width16 forward (native units, each10^9kg): receiver additions lose57796.8298105134; donor subtraction rounds upward by19901.6930562705; six-edge accumulator error .00109336409 is subtracted. Net exact loss37895.1378476070. Other rational numerators/denominators and output hashes are preserved in results.json. Ordinary f64 aggregate totals from the sibling witness differ slightly from these exact sums, as expected.

The cause does not require a race: sequential small receiver additions and donor subtraction round separately. Additionally22805 source cells already contain earlier receipts when their block executes, so the pass can re-send previously received water while target heights still use old immutable masses.30475 positive same-lane proposals are suppressed and two remainder cells cannot donate. Reverse blocks change22719 endpoint values. Width4 forward/reverse changes24767, matching the independently compiled sibling witness.

These are demonstrated defects/order dependencies of copied legacy semantics on this frozen pass. They do not quantify a whole-day correction, prove concurrency safety or justify a new solver's physics. No rates, budgets or production code changed. A future immutable budget/gather candidate remains separately owned and reviewed.
