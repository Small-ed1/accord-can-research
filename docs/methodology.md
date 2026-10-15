# Evidence method and reproducibility limits

## What this publication did

The publication preparation recovered the two-vehicle research reports, the 2003 workbook and implementation references, 2007 revisions through v1.3, and five full 2007 raw recordings plus two focused `224` captures. It consolidated revisions, exported year-specific maps/DBCs, added an offline decoder, tested synthetic regression vectors, freshly recounted the recovered raw integrity totals, and removed identifying content from the public outputs.

It did not install software on either vehicle, send CAN messages, measure new physical reference values, perform an ECU dump, or independently rerun every historical statistical study. Historical frame totals, fits and event counts are labeled by source. A fresh integrity check verifies the recovered recording's parsing and stated checksum rule, not every semantic interpretation.

## Confidence vocabulary

**OBD-validated / OBD-calibrated:** compared with separately decoded diagnostic values, within the recorded reference range and timing limitations. An OBD percentage can still differ from a directly measured mechanical quantity.

**High / vehicle-action-correlated:** repeated trace behavior or a labeled physical action supports the identity. This does not make the mapping universal or safety-qualified.

**Maintainer-confirmed:** a reported dashboard/reference observation, or later clarification in project history. Where the identifying example is withheld, public readers cannot independently reconstruct that particular observation.

**Strong inference / candidate / experimental:** observed relationships support a hypothesis but a discriminating independent reference is missing. Correlation is not a physical label or calibration.

**Raw / unknown / unexcited:** extraction is retained without semantic claims. A constant bit may encode a mode never exercised. A copied/mirrored field is not another independent sensor.

Historical OBD-reference sessions used diagnostic reads during acquisition. “Passive” here describes observation of the broadcast traffic, not a claim that no diagnostic requests were used to collect reference values. No vehicle requests were sent during this publication preparation.

## How the studies reached useful conclusions

Labeled stationary actions identify controls more reliably than unlabeled correlations. OBD comparisons anchor RPM, temperatures and throttle-feedback equivalents. Counter differences reveal incremental behavior, but need continuity and reset handling. Held-out recordings test whether fitted speed/sender relationships generalize beyond their training capture. Source-age gating prevents a stale RPM or lamp reference from becoming false event evidence.

Negative findings matter. Completed tests that did not expose a clean standalone field are preserved rather than silently omitted. Body/HVAC controls may be local, diagnostic-only, on another bus, or absent from the sampled segment. No decode does not prove no signal anywhere.

## Public evidence and private source boundary

The public evidence includes aggregate integrity reports, selected raw-value relationships, relative-time stationary reference pairs, current and historical registers, byte-variability masks with odometer slots redacted, and sanitized narrative appendices. No complete driving timeline or raw vehicle recording is distributed. Complete source-level payload reanalysis therefore requires access to the separately held original captures; the public aggregate report is not a substitute for them.

Some source filenames, source hashes, event payloads and identifying timestamps are removed. Hashes of unpublished originals can link this publication back to earlier private copies, so the release manifest hashes only the files actually published. Within-document relative durations and experiment counts are retained where useful. References to omitted historical companion files are inventory/history, not claims those companions are present in this release.

## Running the checks

From repository root, run `python -m unittest discover -s tests -v`. The dependency-free tests cover parsing, year-specific checksum applicability, checksum failure handling, endian extraction, gear/selector distinctions, non-backported cruise fields, dimmer bit separation, guarded counter arithmetic, fuel scale conventions, distance conventions and unknown/stale state.

The DBC structural tests independently parse the generated signal declarations, verify all 64 bits are covered exactly once per message, and compare deterministic synthetic payload decodes against the JSON-based decoder. This does not replace third-party importer qualification. The optional cantools test performs strict import and comparison when that package is installed; the publication environment could not install it and reports that limitation.

The stationary throttle reference pairs are included with the original stable/transition tags. A separate regression test recomputes the stable fits from the published pairs. This is a reproducible data check rather than a new vehicle experiment.

The offline audit accepts compact or spaced eight-byte standard candump records. It reports unsupported lines instead of silently claiming full coverage, and emits no original path, wall-clock time, payload, odometer or source hash. It does not automatically anonymize arbitrary files or grant permission to publish a raw capture.
