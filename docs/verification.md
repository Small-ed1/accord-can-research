# Verification report

## Publication-time checks

The completed suite contains 34 tests. All 34 pass with cantools 45.0.0 on Python 3.14.7. A standard-library-only run passes 33 tests and explicitly skips the optional importer test. GitHub Actions checks Python 3.10 and 3.14 in both dependency configurations and verifies release hashes and manifest coverage.

The independent DBC declaration parser covers all 64 bits exactly once in each of the 16 year-specific message layouts, with no overlaps or out-of-bounds bits. Across 4,096 deterministic synthetic frame cases, 50,176 field-value comparisons agree with the separate JSON-based decoder. This checks layout/endian/scale consistency, not actual vehicle signal identities or compatibility with every third-party importer.

Strict import through cantools 45.0.0 also passes for both DBCs. Its decoder agrees with the JSON decoder across 4,144 synthetic frames (256 deterministic random payloads and three boundary/pattern payloads per message), comprising 50,764 field-value comparisons. This closes the original draft's missing-importer check for this importer version; it does not qualify every CAN application.

Tests also check current local documentation links, source-tag coverage, JSON/CSV agreement, all 46 historical 2003 signal rows, all 15 remaining 2007 research groups, raw/normalized fuel arithmetic, per-year distance and checksum conventions, state distinctions and published stationary-reference regression results.

Auditor/CLI tests use only synthetic input. They check checksum totals, unsupported IDs/lines, counter breaks, large/backward time gaps, year-specific checksum exemptions, absence of identifying source values in aggregate output, reliable file closure, empty-input rejection and input-error exit codes. Sequence and timing diagnostics remain separate from exact loss estimates.

Run the complete suite from repository root:

```sh
python -m unittest discover -s tests -v
```

For the full importer check:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -W error::ResourceWarning -m unittest discover -s tests -v
```

The release includes the [test transcript](../evidence/tests.txt). The tools were not installed or qualified on either car. The imported draft's unavailable-importer limitation is preserved in the initial Git commit; the current report describes the completed checks.

## Fresh recount of recovered 2007 recordings

| Anonymous source | Frames | Applicable checksum passes | Failures |
|---|---:|---:|---:|
| drive-a | 518,217 | 496,567 | 0 |
| drive-b | 319,681 | 306,330 | 0 |
| standing-a | 446,211 | 427,643 | 0 |
| body-a | 158,096 | 151,492 | 0 |
| startup-a | 7,794 | 7,472 | 0 |
| Total | **1,449,999** | **1,389,504** | **0** |

The other 60,495 frames are 1F4, for which this checksum rule is not applicable. There were no unparsed lines or unrecognized identifiers in this five-file recount. Counter discontinuities and time gaps are reported per source/ID and are not described as exact losses. See the [full aggregate audit](../evidence/independent_raw_audit.json).

The two focused 224 captures contained 4,735 and 7,378 packets. All 12,113 checksum checks passed, and their recorded B1/fuel-counter columns matched the raw payloads. B1 changed once from F3 to F4 in the first and stayed F4 throughout the second. See the [focused audit](../evidence/independent_224_audit.json).

## Fresh count-convention and reference checks

The two recovered drives recount to 1,681 and 856 fine-distance ticks, and 15,236 and 10,000 raw fuel increments. No odd raw fuel values or time gaps over half a second occur in those two counter streams; maximum adjacent raw-fuel increments were 18 and 16. This reproduces the integer count totals, not gallons, GPS distance or a full lifetime reset model. See [counter recount](../evidence/independent_counter_recount.json).

The published stationary throttle-reference table contains 123 pairs. Recomputing the original stable sets gives 53 absolute-throttle samples and 51 relative-throttle samples, matching the original affine coefficients within the CSV's rounding precision. Stable RMSE is approximately 0.130826 and 0.130923 percentage points. See the [refit](../evidence/independent_throttle_refit.json) and [reference pairs](../evidence/throttle-reference-pairs.csv).

## Checks not performed

The original 2003 raw recording set was not recovered/recounted for this preparation; its figures remain attributed historical results. The selected 2007 speed/sender/filter/dynamics fits were not all recomputed during publication preparation. No new physical fuel-volume, sender-voltage, GPS, pedal-position, compressor/clutch or instrument-lamp test was performed. Repository completion reruns the distributable tests, not the unavailable private captures. No new vehicle installation or active CAN transmission was performed.

Privacy review covers the generated release contents, not any earlier public copies, private originals or future commits. Original raw captures/media are not distributed, so readers cannot fully reconstruct the source-level observations from the public bundle alone. The [privacy report](../evidence/privacy-review.json) states the scan scope and remaining identifiability caveats.

## Release integrity

MANIFEST.sha256 hashes every tracked release file other than the manifest itself. The imported ZIP had fixed neutral archive timestamps and no Git history, raw inputs, binary document/media metadata, Python bytecode or private builder scripts. The repository adds a fresh history with a project display name and GitHub no-reply email; virtual environments and bytecode are ignored. CI verifies hashes and complete manifest coverage. GitHub-generated source archives may carry GitHub's archive timestamps. Hash checks protect consistency of an artifact, not truth of every research claim or authenticity of an OEM specification.
