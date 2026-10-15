# Sanitized historical source: 07-V10

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# Accord 2007: CAN ID 0x224 B1 two-drive comparison (v1.0)

## Verified findings

- [date withheld] first capture [wall-clock time withheld]–[wall-clock time withheld]: **4,735 frames, 1,024 OBD samples** in 473.302s. `B1` starts `F3` (243), changes once to `F4` (244) after **276.642251 seconds**, and remains `F4` for the final 1,968 frames.
- [date withheld] second capture [wall-clock time withheld]–[wall-clock time withheld]: **7,378 frames, 1,603 OBD samples** in 737.571s. **Every frame is `F4`**; there are **no hidden transitions between terminal progress updates**.
- All **12,113/12,113 frames** satisfy the known `224` nibble checksum; zero observed modulo-four rolling-counter discontinuities.
- Between the two recordings the observed byte remains `F4`, but recording was not continuous. No assertion of persistence during the gap is justified.

## OBD ranges during the second drive

| OBD signal | Range | Start -> End |
|---|---|---|
| MAP PID 0B | 18–99 kPa | 49 -> 70 kPa |
| RPM PID 0C | 653–4263 RPM | 1569 -> 1961 |
| Coolant PID 05 | 81–92 C | 88 -> 90 C |
| LTFT PID 07 | −10.15625 to −7.8125% | −10.15625 -> −7.8125% |
| STFT PID 06 | −25 to 10.15625% | 0.78125 -> −7.03125% |

At the same time, `224 B1` was `F4` throughout. These eliminate **direct, instantaneously proportional or identical** interpretations of MAP, RPM, coolant and generic OBD fuel trims. They do **not** rule out a separate filtered or learned compensation value.

## BARO hypothesis

The second drive's Apple Maps screenshot suggests **204 ft climb, 307 ft descent, net 103 ft downhill** over an approximately 5.2-mile suggested route. Under typical conditions a net 103 ft descent gives around **+0.37 kPa**. If the *unverified* scaling `B1 * 0.4 kPa` were correct, this is just below one putative code step: an unchanged byte would be possible because of quantization, offset within code bins, sensor hysteresis/filtering, weather, or mismatch between routed and actual GPS elevation. The climb/descent during the route could generate larger transient swings, but the screenshot lacks synchronized elevations. It therefore **weakens an unsmoothed exact 0.4 kPa-per-count interpretation** without proving BARO false.

Neither session includes **engine stopped** OBD samples (first min RPM 693; second min 653); MAP at high throttle **is not a validated BARO reading**. No OBD PID 33 or Honda HDS BARO reference was recorded. Therefore, physical meaning and units are still **unknown**.

## Highest-value next evidence

Acquire Honda HDS **BARO sensor** actual data alongside `0x224 B1` at the same timestamps, ideally at substantially different calibrated ambient pressures. Alternatively, KOEO MAP at *two reliably different* pressures/elevations while logging B1 is informative, though indirect. Another unannotated normal drive with the same OBD PIDs is unlikely to identify this slow field.

## Files

- `summary.json`: stats, transitions, all observed OBD ranges and integrity checks.
- `obd_with_nearest_can_b1.csv`: every OBD row tagged with the closest CAN B1 sample within 200 ms (not simultaneous ECU measurements). This is for cross-checking and future analysis; the complete user-supplied raw archives are unchanged.

