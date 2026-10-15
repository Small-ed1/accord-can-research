# Accord CAN Research
## Observed F-CAN findings for 2003 and 2007 Honda Accord four-cylinder automatics

**Research publication 0.1.0 | 15 October 2026 | Passive observation and offline analysis**

[Repository](https://github.com/Small-ed1/accord-can-research) · [Validation runs](https://github.com/Small-ed1/accord-can-research/actions/workflows/validate.yml)

[![Validate research publication](https://github.com/Small-ed1/accord-can-research/actions/workflows/validate.yml/badge.svg)](https://github.com/Small-ed1/accord-can-research/actions/workflows/validate.yml)

This repository documents the CAN signals recovered while developing CarStats on two seventh-generation Accords. It includes the useful decodes, the evidence behind them, the interpretations that were corrected, and the fields that remain unknown.

These are observations from one 2003 and one 2007 research vehicle. They are **not a Honda OEM DBC, a complete vehicle-network specification, or a claim that every Accord of either year uses these messages.** Extra IDs seen in the 2007 sample are not proven exclusive to that model year.

### Start here

| Question | Document |
|---|---|
| What is mapped on the 2003? | [2003 findings](docs/2003-findings.md) |
| What is mapped on the 2007? | [2007 findings](docs/2007-findings.md) |
| What differs between the samples? | [Cross-year comparison](docs/comparison.md) |
| How do counters, checksums and byte numbering work? | [Protocol](docs/protocol.md) |
| Which speed, distance, throttle and fuel scales are justified? | [Calibration](docs/calibration.md) |
| What still needs an independent reference? | [Unresolved register](docs/unresolved.md) |
| What changed from the earlier reports? | [Corrections](docs/corrections.md) and [research archive](archive/README.md) |
| What evidence can a reader reproduce? | [Methodology](docs/methodology.md), [source register](docs/provenance.md), [verification](docs/verification.md) |
| What was removed before sharing? | [Privacy and exclusions](docs/privacy.md) |
| How is this maintained and released on GitHub? | [Publishing guide](PUBLISHING.md) |

### Machine-readable material

[2003 JSON](data/accord_2003.json) and [CSV](data/accord_2003_signals.csv), [2007 JSON](data/accord_2007.json) and [CSV](data/accord_2007_signals.csv), and separate [2003](dbc/accord_2003_research.dbc) / [2007](dbc/accord_2007_research.dbc) research DBC files.

The 196 non-overlapping layout entries cover every payload bit in the six observed 2003 and ten observed 2007 message layouts. They include 76 named semantic fields, some explicitly experimental, plus protocol fields and raw remainders. **These counts are not counts of independently confirmed physical sensors.** Mirrors, derived representations and candidates remain marked as such.

### Findings worth getting right

Engine RPM is `0x12C B4:B5` as a big-endian integer, without division by four. Primary motion lives in `0x0C8`; the 2007 adds a lower speed representation that better follows the factory-odometer-relative distance. The later odometer convention is `BE24(0x1F4 B3:B5)/1.61` miles. The 2007 fine counter has 164 ticks per factory odometer mile; this is separate from the older 2003 approximate 10 m/tick convention.

Fuel raw counts and normalized counts differ by two. The working volume factor is provisional on the 2007. The accessory bit can remain asserted at zero RPM, so it does not prove compressor rotation. Throttle feedback is calibrated to OBD-equivalent throttle position; neither request-like channel is a validated pedal-percentage measurement. `0x224 B1` still has no defensible physical identity.

### Evidence scope

The 2003 v3 handoff reports 968,238 frames across its baseline and four labeled follow-up captures. This publication freshly recounts **1,449,999 recovered 2007 full-CAN frames**, with **1,389,504 applicable checksum passes and zero failures**. It separately checks **12,113 later fuel-message packets**. Historical study totals overlap and must not be added as independent evidence. Historical fits are attributed to their reports; not every original experiment was repeated during publication preparation.

### Use the offline tools

Python 3.10 or newer, standard library only:

```sh
python -m unittest discover -s tests -v
python tools/accord_can.py audit --year 2007 /path/to/private-capture.log
python tools/accord_can.py decode --year 2007 --id 12C --data 805A00000BB810CE
```

The decode example is synthetic. The tools open local files only and contain no vehicle-transmit path. DBCs expose locations and linear transforms; they do not enforce checksums, freshness, counter continuity, calibration confidence or safe display behavior.

For third-party DBC qualification, create a virtual environment, install `requirements-dev.txt`, and run the same suite with that environment's Python. GitHub Actions runs both the standard-library suite and cantools qualification on Python 3.10 and 3.14, and verifies the release manifest. See [verification](docs/verification.md) for commands and scope.

The CLI returns 0 on a successful decode or an audit with known frames and no checksum, parsing or unknown-ID failures; 1 on those audit failures or an empty audit; and 2 on rejected arguments or unreadable input. Sequence discontinuities and time gaps are reported for review and do not independently change the exit code.

### Safety, privacy and license

Retain the factory cluster and safety warnings. Use properly configured listen-only hardware for observation. This material contains no control-message injection, ECU firmware, immobilizer bypass, or instructions to create faults.

Raw trip recordings, absolute odometer readings, wall-clock capture times, route labels, device identities and photographs/videos are excluded from the public bundle. Sanitized excerpts and aggregate results retain experimental meaning. Sanitization reduces identifying detail; it cannot guarantee anonymity, particularly when the publishing account identifies its owner.

**No reuse license is applied.** See [licensing](LICENSING.md). This repository and its research prerelease are publicly available. Public visibility does not apply an open-source or Creative Commons license. The [unresolved register](docs/unresolved.md) identifies research that requires new independent measurements.
