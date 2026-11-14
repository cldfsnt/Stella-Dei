# Rare inherited mutation tail candidate

Only production change is mutation distribution in `src/simulation/microbes.zig`. Existing six ordinary mutation draws and pre-admission checks retained. Tail reuses previously unused low40 bits of sixth draw; top24 bits still give identical ordinary organization delta. It never advances RNG additionally.

## Distribution
Low9 bits all zero => probability1/512 per successful mutating birth. Next16 bits select one of six traits using multiply-and-shift (bins differ by at most1/65536). Nextbit chooses sign. Remaining14 bits choose magnitude in[1,3) times ordinary halfwidth. Replace the selected ordinary delta from the original parent's trait, not compound it. Existing bounds unchanged.

Temperature step3–<9K; efficiency.06–<.18; structure/feeding/mobility.1–<.3; organization.06–<.18, either sign. Bound clamping may make an event small or invisible, especially at zero. No guaranteed beneficial direction, habitat targeting, trait unlock, new taxonomy, biomass/tissue/credit grant. Rare probability counts mutation events, not survival or expressed novelty. Distribution is a gameplay choice, not a claim about biological mutation rates.

## Reproducible validation
`zig test src/simulation/microbes.zig --cache-dir <absolute-cache> --global-cache-dir <absolute-global-cache>` (Zig0.13).

All31 tests pass:29 existing regressions unchanged,2 new tests.
262144 successive funded births from midpoint fixtures with seed20261114 yielded524 tail events (expected512),250positive and274negative. Trait counts in temperature,efficiency,structure,feeding,mobility,organization order:88,92,87,100,77,80. Positive counts46,46,38,47,36,37; negative42,46,49,53,41,43. All six traits and both signs sampled. Midpoint traits avoid bounds so tail magnitudes are expressed without clamping; endpoints tested separately. Statistical acceptance bounds are broad deterministic smoke checks, not a proof of ideal randomness.

Every sampled actual reproduction checks exact RNG state after six draws against old-reference mutation; all nonrare trait values exactly match old behavior, and only selected trait differs on rare births. Full reproduction replay from same state is exactly equal. Every sampled birth checks valid cells, conserved donor+child carbon/nutrients/support, credit debit and zero child credit. Nonmutating grandchildren preserve inherited traits and RNG state (separate funded-size fixture, not ecological growth). Boundary cases test all trait/sign/extreme combinations, finite clamping, no mass/support change, and insufficient-parent failed reproduction leaves donor/destination/RNG unchanged. No save fields added.

## Limits / release gate
Parent is independently running save-schema, actual-world scheduler and native/WebAssembly playtests. These are not claimed by this report. Individual nonrare births preserve old output, but rare descendants can change later ecological trajectories and random branching; whole-world historical outcomes are not guaranteed identical. Rare mutations must not be presented as guaranteed strong successors. Existing headless ecology evidence remains immutable and describes the previous distribution.

## Additional environmental sign test
Full suite now32/32 passes; see thermal-and-regressions.log. Reproducibly search actual funded rare thermal offspring with step magnitude3–<5K from parent300K. Compare each offspring against an identical copy with only optimum reset300K, matched resources and physiology for one lit day. Both share all other mutated traits, paid tissue, mass and credit; no fitness is consulted during mutation.

Actual positive tail seed14176 optimum304.54175K: in297K mass.06366 vs thermal-reset.09158 (harmful), in303K .10269 vs.09158 (helpful). Actual negative tail seed17598 optimum295.20410K: in297K .09121 vs.08310 (helpful), in303K .05701 vs.08310 (harmful). Carbon/nutrient/gas/validity checks pass each step. Controlled sign demonstration, not a claim every rare mutation improves somewhere or fixes long-term succession. No runtime implementation changed by this added test.
