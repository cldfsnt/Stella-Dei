# Bounded wind target kernel (before execution)

Parent-authorized game abstraction, not calibrated spore aerodynamics. Radius is kilometres (Planet radius5000); point vectors are used only as directions. Actual donor atmospheric wind is projected into its tangent plane; magnitude is not a flight-speed model. Calm/invalid/unroutable attempts fall back to ordinary local opportunity before any paid release.

Fixed conditional truncated Pareto: minimum100km, maximum min(5000km,0.9*pi*radius), alpha1.5; d=100/[1-u*(1-(100/dmax)^1.5)]^(2/3), u in[0,1). No cap atom. Target direction cos(d/R)*normal+sin(d/R)*wind_unit. Actual source-to-destination great-circle distance determines survival exp(-distance/1000km).

Greedy angular-score ascent from donor on actual immutable topology: six slots, ignore self/duplicate neighbors, deterministic lower-index ties among equally improving neighbors, strictly positive improvement only. Maximum256 hops; no full-world scan, no allocation, no habitat suitability search. Validate traversed geometry/indices; cap/invalid/self endpoint refuses before launch. This is bounded approximate targeting, not guaranteed globally nearest location. Local ordinary opportunity remains scheduler fallback. Paid packet mortality/resource accounting is owned separately and not implemented here.

Tests fixed in advance: deterministic ties and neighbor order, pentagon padding, polar and longitude-wrap routes, calm/nonfinite/invalid inputs, hard cap, near/far distance and survival, purity; actual existing 40962-cell exported graph across deterministic donor/quantile choices, report achieved distances/hops/refusals without parameter adjustment. No ecology run or production edits. Test-only all-world nearest comparison, if used, is not runtime target selection.
