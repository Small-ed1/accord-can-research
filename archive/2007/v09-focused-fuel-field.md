# Sanitized historical source: 07-V09

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# Honda Accord 2007 CAN 0x224 B1: continuous comparison v0.9

## Evidence
- Session: [date withheld] to [date withheld], 473.302 seconds (7m 53s).
- Frames: 4735 from CAN ID `0x224`, 10.0 Hz; 4735/4735 valid Honda payload checksums, 0 observed modulo-four counter discontinuities.
- OBD: 1024 PID measurements (MAP 0B, RPM 0C, ECT 05, LTFT 07, STFT 06), about one measurement per PID every 2.27 seconds. All OBD samples align to preceding CAN message within 0.2 seconds.

## Exact transition
- One and only one change in `0x224 B1`: `F3` (243) → `F4` (244), 276.642 seconds from first CAN packet, at [date withheld].
- `F3`: 2,767 frames; `F4`: 1,968 frames, with no reversals.
- Counter `0x224 B2:B3` was 6894 at transition; no wrap or reset at the transition.
- OBD MAP was 26 kPa in measurements bracketing transition; LTFT was −6.25% on both sides. Coolant was 86°C before, 85°C after; RPM approximately 1920 before, 1813 after. No synchronous OBD signal transition identifies this byte.

## Independent ranges
- With `B1=F3`, OBD MAP ranged 19–99 kPa; with `B1=F4`, 21–94 kPa. Thus `B1` is **not direct MAP**.
- With `B1=F3`, OBD LTFT changed between −5.46875% and −6.25%; with `B1=F4`, all measurements were −6.25%. Thus `B1` is **not a direct copy of LTFT PID07**.
- Coolant ranges overlap (81–87°C for F3 and 84–88°C for F4), ruling out any obvious direct temperature-byte equivalence.
- RPM ranged from 693 to 5112 throughout OBD measurements; there were **no recorded engine-off/KOEO OBD reference readings in this session**, despite the test suggestion.

## Working hypotheses
- A slowly changing atmospheric-pressure/BARO representation **remains plausible**. Hypothetical `0.4 kPa/count` means F3=97.2 kPa and F4=97.6 kPa. That scaling was proposed based on plausibility, **not estimated from paired pressure measurements**. Running MAP cannot provide direct barometric reference.
- A delayed/adaptive fuel-control value also remains plausible but no direct mapping to OBD fuel trims is supported.

## Best next discriminating evidence
Acquire PCM BARO live-data values via a compatible Honda HDS-capable diagnostic interface, and compare with raw CAN `0x224 B1`, ideally across two different ambient-pressure/elevation conditions. Alternatively, log synchronized KOEO MAP and B1 at two substantially different known elevations (KOEO MAP approximates ambient pressure). There is **no need to repeat the same ordinary drive**.

