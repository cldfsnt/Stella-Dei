# Paid offspring routing: negative progression result

## Decision
Do not ship a scheduling change from these results. Larger paid offspring and reserved credit change demographics, but neither policy consistently improves descendants establishing or reproducing. Nothing here demonstrates stronger late successors, new adaptation, or better mobile play.

## Existing evidence and the actual gap
- `../reciprocal-transplant/README.md`: naturally evolved wet/shallow phenotypes reverse competitive outcomes across habitats, but paired assays do not reproduce and exported daughters are inert accounting mass.
- `../../moist-film/evidence/FILM-V28-QA.md`: five specifically traced shallow-earned offspring were all absent at day100. Natural film production is supported; those offspring's establishment is not.
- `../establishment/README.md`: production scheduler shows severe rare-daughter losses despite empty cohort slots. Earlier grazing-encounter candidate was rejected.
- Existing paid support consumes carbon and oxygen, reduces frond tissue, changes shared light allocation and permits conditional moist-film performance. Structure is not grazing armor or fire resistance. No new low-demand trait is needed to expose these existing contrasts.

This assay tests the remaining credit-routing hypothesis rather than repeating equal-abundance transplant viability.

## Method
Three seeds (42,1337,2027), two habitats (uniform1m/303K and six of19 patches at8cm/303K), three policies,180days at1440s. Actual copied `Planet.simulateMicrobes` including physiology, movement, mutation, donor-funded births, finite shared gases, original light and space competition. Only reproduction routing is changed in the copy; no production file changed.

- **0 current:** exploratory .004 offspring first; successful attempt skips the larger route.
- **1 large-first:** if existing .04 credit threshold is met, try the original .01 local/neighbor birth route first; otherwise exploratory fallback remains.
- **2 accumulate:** large-first, and exploratory fallback is withheld until .04 credit, allowing accumulation rather than repeated spending at .01.

Existing costs and thresholds remain: exploratory .004 mass/.01 credit, larger .01 mass/.04 credit. These are NOT equal cost per daughter or per transferred biomass. `PAID` counters sum successful API transfer amounts and earned-credit debits, not an independent bit-exact measurement of represented f32 subtraction. Actual cell/global inventories are checked each tick. Changed random draw order and accepted births diverge later genomes; same seeds are not paired identical phenotypes.

The original large-neighbor route requires aquatic `habitable()` and excludes film below20cm; tiny exploration has no favorable-habitat gate. Local large births remain possible in film. This preserved asymmetry is part of the policy comparison, not silently changed biology.

Fates track globally unique lineage IDs after day30, including relocation. Sampled peak mass is a lower bound; parent mass may already be debited at observation. Late survivors are right-censored. Becoming a parent proves funded reproduction, not long-term evolutionary fitness. Initial nursery, resource pools and controlled topology follow the existing establishment assay. No automatic hydrology or rendered-game test is claimed.

## Day180 outcomes
Entries are seed42 /1337 /2027. Counts are post-day30 daughters observed becoming parents.

| Habitat | Current | Large-first | Accumulate |
|---|---|---|---|
| Stable wet |15 /14 /0 |22 /24 /0 |1 /7 /2 |
| Depth mosaic |37 /34 /16 |36 /19 /13 |9 /10 /21 |

The accumulation policy does produce many larger offspring: stable late larger births5383 /5918 /5624, versus current4 /7 /0. Nevertheless99.72% /99.26% /99.80% of its late stable daughters die within one day. Current losses are99.89% /99.83% /100%. Making daughters larger did not reliably translate into more established reproductive descendants.

Accumulation reduces stable total births from36548 /33360 /34835 to7035 /7574 /7327. Successful transferred mass sums fall from150.326 /138.816 /144.338 to70.266 /75.608 /73.222 (summed patch densities, not global mass); credit spending and grazing also change. This is a demographic/resource-routing tradeoff, not automatically an adaptation. In stable seed42, occupied patches fall19→18 and late parents15→1 despite many more large offspring.

Large-first has modest stable gains in two seeds but none in the third, and lower late-parent counts in all three mosaics. Maximum generation is mixed, not a consistent progression benefit. No winner was selected or tuned for. Given the lack of consistent improvement, no additional timestep sweep or production recommendation was made.

## Verification and numerical limits
All18 runs complete with per-tick valid-cell, nonnegative-gas and original absolute carbon/nutrient tolerance0.001 checks; build exit0. This tolerance is inherited from the Planet assay, not raised after observing results. Largest logged checkpoint errors are3.5741e-4 carbon and7.1302e-5 nutrient; these are NOT exact conservation and may not be full-time maxima. Known f32 drift remains, separately investigated in `../energy-nutrient-diagnosis/`.

Six additional untouched-production reference runs yield all30 policy0 checkpoint rows exactly, including masses, resources, births and fate counts. This is logged-observable parity, NOT full serialized state bitwise proof. Reference build exit0. Initial test-only compiler failure (research globals placed before container doc comments) is preserved and corrected; no biology executed in that failed attempt.

## Next useful gameplay step
Surface actual existing paid tissue, water depth, light share, growth/loss and child fate through the current patch-observation work, without promising film compatibility guarantees. The useful ecological question remains whether particular naturally evolved descendants persist and reproduce in accessible niches, not how many births are emitted. A future instrumented experiment could attribute immediate daughter losses to actual grazing, exposure and maintenance before trying another policy. Do not add immunity or tune credit solely to increase generation counters.

## Reproduction and provenance
New files: `src/qa_routing_establishment.zig`, `web/tests/prepare-routing-assay.py`, this evidence directory. Preparer requires a fresh destination and copies source before altering only copied scheduling/telemetry:

```
python3 web/tests/prepare-routing-assay.py /absolute/new/copied-src
zig build --build-file web/tests/lifecycle-build.zig -Dsource=/absolute/new/copied-src/qa_routing_establishment.zig --cache-dir /absolute/cache --global-cache-dir /absolute/global-cache
```

Use Zig0.13.0. Source baseline planet SHA256 `a713a241c224d5da5f353a03dc887bb041ea29cf3c55bdc3a443879dc1dfa9e8`; microbes `844f077e8a6112fc37261e23ebbc4497af6ccd9bc48d04255ec4a6c045b6d485`. Exact baseline files and full copied reference manifest are archived with deterministic gzip; `copied-source.patch` records experimental edits. For the reference, use the original establishment harness, replace its final test with the same three seeds and kinds0/3 at1440s, and change mosaic temperature293→303. No scheduling changes. Raw logs and parsed results are losslessly gzipped with mtime0. `RAW-SHA256SUMS` records original log bytes; all evidence is covered by `SHA256SUMS`.

No commit, deployment, source-schema change or user-visible feature was performed by this worker.
