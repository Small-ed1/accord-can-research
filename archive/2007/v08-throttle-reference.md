# Sanitized historical source: 07-V08

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# CarStats 2007 Accord, throttle calibration v0.8

Source: `throttle_calibration.tar.gz`, CAN + OBD collected [date withheld].

## Verified input quality

- 57,251 passive CAN frames over 95.667 seconds, 10 IDs, including 9,569 frames from `0x0A6`.
- 245 timestamped OBD reference readings; PIDs `11` (absolute throttle), `45` (relative throttle), `0C` (RPM), and `0D` (speed).
- All 54,859 payload checksums in applicable messages passed. Every CAN ID showed zero modulo-four counter discontinuities. `0x1F4` does not use this checksum mapping.
- PID 11 and PID 45 each refresh about every 1.3 seconds because they are multiplexed with RPM and speed queries. Steady-state samples only were fitted.

## Conclusions

**High-confidence throttle feedback:** `0x0A6 B3` is the main feedback/actual-throttle channel. Relative PID 45 and absolute PID 11 both align with this byte. During engine-off, released-pedal periods, `B3=19` and `B2=9` provide the discriminating case: PID 45 reads 8.63%, matching `B3`, not `B2`. At warmed idle, `B3=8`, PID 45 reads 3.53%.

**Request candidate, not proven:** `0x0A6 B2` leads `B3` by approximately five 10-ms frame intervals during pedal transitions, consistent with a desired/commanded throttle value. The offset during key-ON engine-OFF behavior also supports this distinction, but factory-level semantics remain unverified.

**B4 is redundant, not measured pedal:** across all 9,569 captured 0x0A6 frames, `B2 - B4` is always 8, 9 or 10 raw units. That degree of agreement means `B4` cannot be treated as an independent pedal sensor. It is a pedal-responsive/request-like raw value, not a confirmed pedal percentage. No standard accelerator PIDs were supported by the user's ECU.

## Calibrated equivalent OBD percentages

Derived from 51 stable paired samples for PID 45 and 53 for PID 11:

```python
# B3 = frame_0a6[3]
relative_throttle_pct = max(0.0, min(100.0, 0.0980 + 0.44499 * B3))
absolute_throttle_pct = max(0.0, min(100.0, 11.5416 + 0.32213 * B3))
```

These are empirically fitted to ECU-reported OBD values and valid within tested `B3 = 8..208`.
Steady-state RMSE: PID 45 = 0.131 percentage points, PID 11 = 0.131 percentage points, approximately one-third of one OBD byte. Do not confuse display calibration with OEM physical angle calibration, full pedal travel, or an exact official formula.

## Stable stages

| Test phase | B2 | B3 | B4 | OBD absolute % | OBD relative % |
|---|---:|---:|---:|---:|---:|
| KOEO pedal released | 9 | 19 | 0 | 17.65 | 8.63 |
| Nominal 25% pedal | 44 | 44 | 35 | 25.88 | 19.61 |
| Nominal 50% pedal | 100 | 100 | 91 | 43.92 | 44.71 |
| Nominal 75% pedal | 122 | 122 | 113 | 50.98 | 54.51 |
| Pedal fully depressed | 208 | 208 | 198 | 78.43 | 92.55 |
| KOEO released again | 9 | 19 | 0 | 17.65 | 8.63 |
| Engine idling | 8 | 8 | 0 | 14.12 | 3.53 |

Note that "25%/50%/75%" are the operator's approximate pedal positions, not independently calibrated mechanical pedal travel.

## Development recommendation

- Use B3 (estimated relative throttle %) for the primary throttle position gauge.
- Use B2 as a separate experimental request/target overlay (raw units), only if needed.
- Do not build a `pedal_position_pct` feature from B4 without an independent pedal reference such as HDS or instrumented sensors.
- Fuel accumulator volume-per-count, fuel level in gallons, and fuel cut remain separate calibration tasks; this capture does not determine them.

## Files

- `calibration.json`: fitted model coefficients, data coverage, checksums and caveats
- `stage_summary.csv`: sustained-control intervals and values
- `paired_reference_samples.csv`: per-PID OBD + nearest CAN raw values + stability flag + model residual
- `decoder.py`: self-contained Python reference decoder; no changes made to the vehicle or running CarStats system

