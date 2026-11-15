# Hybrid boundary / abiotic coupling: pre-outcome contract for review

Isolated pure local-column prototype only. No full Planet, save schema, organism physiology, new climatic rate, biological outcome or production change. Read7e159a4/c9256b3. The local-f64 seven-day gate does NOT validate a nativef32 bridge. Surface/vapor are authoritativef32 in10^9kg/patch; physical soil is authoritativef64 kg/m²; actual positive finite meanarea is an explicit input. No hidden/residual hydrating pool.

## One atmospheric request, not another evaporation budget

Use actual production AtmosphereWater.PhaseStep.init(dt), its evaporation/condensation/rain-memory coefficients and saturation input. Caller supplies existing saturation calculation; prototype does not change it or invent a root vapor limit. At T<=273.15K, NEW soil evaporation iszero. Biological root demand/habitat is outside this assay; no implicit transpiration saturation gate.

Enabled candidate replaces ONE phase exchange; it is not called after a completed original phase and cannot consume a second full deficit. Compute original potential evaporation J=max(0,saturation−initialvapor)*existing_relaxation once in native mass units. Standing liquid has first claim, using actual represented f32 source debit bounded by J. If any standing liquid remains, soil evaporation iszero, even when rounding left an unspent atmospheric request. A still-submerged soil cannot exploit leftover nominal demand.

If standing liquid is alreadyzero, soil may supply remaining J. If finite standing liquid is actually depleted, remaining budget is J−actual standing debit, never a recalculated full deficit. Record depletion time from existing exponential law `−86400*log1p(−initial_liquid/initial_deficit)`, clamped to[0,dt] only for rounding at boundary; exposure is the remaining part of this tick. This assumes constant temperature/saturation and continuous availability of moist soil once uncovered; it is an explicit time-splitting approximation, not calibrated pore physics. For an undepleted pool exposuretime0. Demand remaining after depletion already accounts for the exponential time, so do not multiply it a second time by exposure fraction.

Actual soil debit is limited by finite soil and converted remaining atmospheric request. Vapor receives the represented bridge addition once. Condensation then runs ONCE from resulting actual vapor using existing condensation coefficient and saturation; actual represented vapor debit funds standing liquid. Rain diagnostic uses existing memory equation with actual condensed amount, explicitly not exact original enabled-path parity.

## Fixed order and cold policy

Order: standing evaporation → exposed-soil share of SAME request → condensation/rain → infiltration → drainage. Warm infiltration/drainage may operate with standing water (soil is then submerged, not evaporating). For this narrow prototype new infiltration and drainage are disabled at T<=273.15K as a conservative frozen-substrate assumption; no ice storage/melting physics is added. Existing atmospheric condensation still follows original law. This policy must be reviewed, not silently extrapolated to global climate.

Infiltration uses caller capacity/rate and actual represented f32 standing debit; only that mass may credit soil. Drainage uses caller rate and actual soil debit into standing pool. No laboratory constant evaporation_rate is used. dt0 is identity. Negative/nonfinite/derived-overflow inputs refuse atomically. Feature-disabled branch directly calls original PhaseStep and casts outputs exactly as current production, leaving soil untouched; verify exact result bits, not 'close'.

## Receipt and precision observations

Source removals are bounded by requested physical amount; actual f32→f64 source debit and area conversion fund soil. Downward conversion/receiver credit must never grant more soil than exact physical source debit. Any unavoidable uncredited difference is explicitly numerical physical loss, not a drinkable escrow. For f64soil→f32vapor, record actual source debit and actual receiver increment separately; receiver rounding may erase/create a fraction of a quantum. This is NOT automatically acceptable merely because the source funded it.

Offline Fraction recomputes every physical receipt in common kg/m² using exact native inputs and exact1e9/area. Report signed and SUMABS errors, per-operation nativeULP×conversion envelope, zero/subresolution requests, actual source-funded soil, actual evaporation vs single atmospheric request, exposuretime and rain. No arbitrary totals correction or refill. Root h is absent; do not use a generous atmospheric error budget to grant biological water.

## Bounded fixed test set, before engine/biology

Use dt360/720/1440 and frozen temperatures270/273.15/300K. Pure columns: initiallydry wetsoil; persistentlywet standing pool; exactly depleted finitepool; nearlydepleted but represented residualpool; saturated/supersaturated vapor; zero soil; zero request; capacityfull; invalid/extremearea. Capacity1, caller infiltration1/day and drainage.01/day are inherited laboratory fixture values for bridge tests, not climate defaults. Existing PhaseStep alone determines evaporation. Include actual native surface/vapor values from root478 and actual preserved stage operands, with explicitly declared saturation multipliers(0.5,1,2×initialvapor) as controlled request probes, not claimed recorded weather.

Acceptance for this DESIGN gate: exact disabled-path parity; no soil evaporation frozen/under standing water; aggregate actual evaporation≤single requested budget within declared conversion rounding; no soil credit beyond exact source debit; all finite/atomic/refusal conditions; error within derived endpoint/conversion envelope. QUANTIFY practical boundary error and missed fractions before choosing a full-engine absolute/relative tolerance. The existing1e-9local-f64 gate is reported as a comparison only and may fail here. No biological rerun or production integration even if these structural gates pass. Save all failed cases and seek review before selecting a coupled budget or changing representation.

## Pre-code reviewed cold policy

Suspend ONLY new soil infiltration/drainage/evaporation when snapshotT<=273.15K; existing condensation and disabled legacy path unchanged. Physical water stays owned in its original pools. Warm transition resumes normal perstep bounded rates, no accumulated catch-up, thaw bonus or capacity reset. Test exact273.15f64, adjacent representable f32 temperatures, and cold→warm→cold water accounting. This is a declared substrate-availability assumption, not ice or latent heat physics. Independent fire review approved before implementation.
