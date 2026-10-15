# Sanitized historical source: 07-V04

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# Calder / CarStats: 2007 Accord four-capture follow-up (revision 0.4)

**Evidence:** four separate passive `candump -L can0` captures from [date withheld]; byte indexing is zero-based. Source files are referenced by exact filename and SHA-256 in `updated_signal_map.json`.

## Capture inventory

| Capture | Duration | Frames | Checksummed frames valid | Rolling-counter discontinuities |
|---|---:|---:|---:|---:|
| `drive-b.log` | 536.75s | 319,681 | 306,330 / 306,330 | 1 |
| `doors-a.log` | 47.08s | 28,180 | 27,003 / 27,003 | 0 |
| `startup-a.log` | 15.23s | 7,794 | 7,472 / 7,472 | 1 |
| `hvac-a.log` | 73.56s | 44,023 | 42,184 / 42,184 | 0 |

No malformed frames or failed Honda payload checksums in these captures. The two one-off rolling-counter discontinuities occur in recordings containing startup events; do not infer data loss from these counts without inspecting the key transition.

## Definitive new practical mapping: four independent doors

All doors are reported by **CAN ID `0x405`**, approximately **3.33 Hz**. Interpret each signal as a separate Boolean and treat stale packets as unavailable rather than closed.

| Door | Mask | Open intervals, seconds from start |
|---|---|---|
| FL | `B4 & 0x20` | 3.432-5.232, 6.432-9.732, 41.832-45.733 |
| FR | `B4 & 0x40` | 16.032-18.132, 19.632-21.732 |
| RR | `B5 & 0x01` | 24.132-26.232, 27.432-29.532 |
| RL | `B4 & 0x80` | 34.933-37.032, 38.232-40.032 |

User explicitly says they **exited through driver door at the start and re-entered at the end**, while testing FL→FR→RR→RL twice. There are *three* FL assertions (the first two early and the final re-entry), exactly two for each other door, and no cross-activation under single-door testing. Do not presume simultaneous multi-door OR behavior until that case is tested.

**Compact decoder:**
```python
front_left_open  = bool(can405[4] & 0x20)
front_right_open = bool(can405[4] & 0x40)
rear_right_open  = bool(can405[5] & 0x01)
rear_left_open   = bool(can405[4] & 0x80)
```

## A/C compressor signal: strengthened but still candidate

`0x0D4 B2 & 0x40` stays **asserted during all 73.564 seconds** of the MAXAC capture, while engine idles 779–816 RPM. During the drive-b drive it is present 89.2% of the frames and drops for nine intervals:

`5.84s, 6.03s, 5.99s, 6.32s, 6.25s, 6.04s, 6.43s, 6.50s, 6.59s`.

Mean dropout duration: **6.221s** (range 5.84–6.59). This controlled-looking cycling is consistent with an ECU compressor clutch *request/permission/command*. The prior A/C OFF/ON/OFF standing sequence did not directly control this field. The bit is also present with engine zero-RPM at startups. Therefore **do not equate it with proven clutch engagement or A/C-cold output**. A synchronized actual clutch observation or magnetic-clutch relay measurement in a safe, qualified setup is the remaining discriminator.

## Speed and odometer inference: independent repeat

`0x0C8 B6` advances **856 ticks** in the drive-b file. The coarse `0x1F4 B3:B5` raw field changes as shown in `odometer_checkpoints.csv`, with tick totals at 5,169,333,497,661,825 after the first source-frame boundary; all five successive differences are exactly **164 ticks per update**.

If each coarse update means **one dashboard mile**, derived distance is **5.219512 miles = 8.399991 km**. Integrating `0x0C8 B0:B1 /100` gives **8.392988 km** (−0.083% vs derived); `B4:B5 /100` gives **8.565633 km** (+1.972%). The higher speed channel is approximately 2.06% above the lower one. The 164-tick sequence repeats the earlier drive-a result. This independently favors channel A for the odometer-relative estimate, but a GPS/dashboard anchor remains required for physical absolute calibration.

`0x1F4 B3:B5` raw jumped from [absolute reading withheld] to [absolute reading withheld] during this drive; each coarse update increments raw by 1 or 2. **Do not use the raw number directly as miles**, nor assume every new raw integer equals a mile. Carry persistent mileage across ignition key cycles independently of the raw fine counter.

## Decel fuel cutoff and cruise

Eight `0x0A6 B0 & 0x02` fuel-cut-candidate intervals total **13.708s**. In all eight intervals, the observed `0x224 B2:B3` raw counter is constant at available 10-Hz samples. A 0.07-second interval contains only one fuel sample and is therefore weak alone; three sustained intervals (>3 seconds) are strong corroboration. The capture advances the fuel accumulator by **10,000 raw ticks** overall; *do not compute gallons or MPG without a 2007-specific calibration*.

Cruise engagement is independently clear in `0x12C B6 & 0x08`, with three recorded runs:

| Start | End | Duration |
|---:|---:|---:|
| 151.753s | 264.446s | 112.692s |
| 309.599s | 349.493s | 39.894s |
| 389.026s | 419.882s | 30.855s |

`0x0D4 B0 & 0xC0` supports `0x40=SET/COAST`, `0x80=RESUME/ACCEL`, `0xC0=CANCEL`. Two CANCEL presses at 264.404s and 419.838s are followed by cruise deactivation about 42–44ms later, strongly corroborating this mapping.

## DRL-off / starting / parking-brake capture

At 2.427s into the `alDRL` recording, `0x20C B0` changes `00→02` while other ECU frames resume, agreeing with the **ignition-ON candidate** even before engine RPM rises. Startup status `0x1F4 B0 & 0x02` clears around 4.532s. This does **not** establish a DRL output bit; no individual daytime-running-lamp physical reference was recorded.

At 10.832s, `0x0D4 B0` changes `24→20` (parking-brake bit clears); `0x405 B2` catches up from `24→04` at 11.073s. The handbrake status cross-check is therefore consistent with existing standing/drive results.

## Immediate CarStats engineering recommendations

1. Add the **four-door status decoder** to a 2007 profile, reading `405` as four independent door-open masks. Display stale/unavailable after a bounded receive timeout; do not silently report closed after missing packets.
2. Preserve `0D4 B2 &0x40` as `ac_compressor_command_candidate` behind an experimental label until relay/clutch observation. Add a timestamped trend to Diagnostics.
3. Use `0C8 B6` modulo-256 deltas for provisional **164 ticks per dashboard mile**; compare the lower speed channel to GPS and one synchronized dashboard odometer increment.
4. Interpret cruise SET/RESUME/CANCEL as an enum, never independent two flags. Use `12C B6` for actual engagement and `20C B0 &2` for tentative ignition-ON availability, both freshness-gated.
5. Never treat fuel resets, dropped messages or key transitions as ordinary counter rollovers. 2007 mL-per-count fuel calibration remains open.

## Remaining focused tests

- **Door simultaneous-open:** open FL+FR together, then FL+RR, to confirm status bits combine (parked).
- **A/C clutch correlation:** record actual clutch on/off alongside `0D4 B2&40`, including button OFF and MAX A/C ON; parked, safely away from moving belts/fans.
- **Dashboard/GPS distance:** measure at least 2–3 known mile increments and compare lower and higher speed channels.
- **Power-state:** independently powered Pi and labeled OFF/ACC/ON, observe how long `20C` survives OFF.
- **Fuel gallons:** uninterrupted full-to-full calibration, explicit ignition-reset handling.

## Artifacts

- `updated_signal_map.json`: source filenames/hashes, integrity metrics, calibrated-vs-candidate labels and calculations.
- `door_events.csv`: all 9 open events in temporal order, including the last FL re-entry.
- `compressor_candidate_off_windows.csv`: nine quantified 5.8–6.6s OFF periods.
- `fuel_cut_intervals.csv`: eight raw-counter comparisons.
- `cruise_engaged_intervals.csv`: three confirmed engaged intervals.
- `odometer_checkpoints.csv`: raw checkpoint values and fine counter totals.

**Boundary:** this is passive, offline analysis. No CAN injection, car control, CarStats software installation or physical clutch verification took place.

