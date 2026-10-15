# Sanitized historical source: 07-V01

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# 2007 Accord CAN decode and validation plan

Source: `drive-a.log`
Analysis revision: 0.1, 13 October 2026. This is an offline evidence map, not an installed CarStats build or a complete Honda DBC.

## What is established, and what remains provisional

The full capture contains 518,217 valid eight-byte frames from 10 standard CAN identifiers, covering 865.988745 seconds on `can0`. Its recorded local times are [wall-clock time withheld] to [wall-clock time withheld] on 13 October 2026. All calculations here use the complete file, not its chat preview.

The strongest reusable signals are engine RPM and temperatures, forward gear/target gear/selector, brake and cruise status, turn requests and wiper modes. Speed-like fields and distance/fuel counters are clearly located, but their physical calibration must stay separate from identifying their bytes.

Three corrections to the earlier summary matter:
1. `0x188 B0` is the steady forward-gear field. `B1` is the target/commanded gear field. `B0=7` is also present throughout Reverse, so it must not unconditionally mean “shifting.”
2. The previous 10.45-mile estimate assumed exactly 10 metres per fine-distance tick. This capture exposes a different, testable cluster-relative calibration: 164 ticks per coarse odometer update. Do not silently carry over the old 256-ticks-per-mile setting.
3. The previously quoted gallons and MPG are not validated measurements of this 2007. The counter is confirmed; millilitres per count are not. A factor-of-two error is easy if raw 16-bit values and right-shifted half-counts are mixed.

The comparison with the 2003 is based on prior decoder notes, not a second, contemporaneous raw 2003 capture. The four other identifiers cannot be called unique to the 2007 on this evidence alone.

## Conventions and confidence

Bytes are zero-indexed: B0 is the first payload byte. BE16(B4,B5) means `256*B4+B5`. BE24(B3,B4,B5) means `65536*B3+256*B4+B5`.

**High:** strong trace evidence and/or a prior 2003 decoding supported by this trace. A labeled 2007 sensor/control check remains appropriate.
**Strong candidate:** several internally consistent correlations or events, but no independent labeled ground truth.
**Candidate/unknown:** retain raw data; do not assign production labels or physical units yet.

## Message inventory

| ID | Frames | Nominal rate | Main observations |
|---|---:|---:|---|
| 0x0A6 | 86,614 | 100 Hz | Throttle-related channels and fuel-cut candidate |
| 0x0C8 | 86,613 | 100 Hz | Two speed channels and an 8-bit fine-distance counter |
| 0x0D4 | 86,599 | 100 Hz | Cruise-button candidates, status, fuel-sender candidates, filtered speed |
| 0x12C | 86,613 | 100 Hz | RPM, coolant, intake air, brake, cruise |
| 0x188 | 86,613 | 100 Hz | Forward gear, target gear and selector |
| 0x1F4 | 21,650 | 25 Hz | Wiper/turn requests, illumination level, odometer-like value |
| 0x20C | 43,307 | 50 Hz | Duplicate RPM |
| 0x224 | 8,662 | 10 Hz | Fuel accumulator and one unresolved changing byte |
| 0x2E4 | 8,659 | 10 Hz | Constant zero B0:B6; rolling counter/checksum only in this run |
| 0x405 | 2,887 | 3.33 Hz | Illumination and other parked-status flags |

### Frame integrity

All ten streams have a counter in B7 bits 7:6 that advances by one modulo four in every consecutive recorded frame. No counter skips were observed. No per-ID gap exceeded 1.5 times its median period. There are no malformed or blank lines.

For the nine IDs other than 0x1F4, all **496,567** applicable frames satisfy:
```
checksum = (-sum((x >> 4) + (x & 0x0F) for x in B0..B6)
            - (B7 >> 4)) & 0x0F
valid = checksum == (B7 & 0x0F)
counter = (B7 >> 6) & 3
```
For 0x1F4, B7 is 00/40/80/C0. Its lower six bits remain zero; do not apply the above checksum to it.

This is a validation of the observed payloads, not proof of physical bus health, all possible messages, or error-frame coverage.

## Strongest signal decodes

| ID / bytes | Decode | Qualification |
|---|---|---|
| 12C B4:B5 | BE16, RPM | 654–6,250 RPM |
| 12C B0 | B0 − 40 °C | Coolant, 82–91 °C |
| 12C B1 | B1 − 40 °C | Intake air, 31–49 °C |
| 12C B6 & 01 | Brake applied | 12 brake-on runs |
| 12C B6 & 08 | Cruise engaged | Three runs, 393.852 seconds total |
| 0C8 B0:B1 | BE16 / 100 | Speed channel A; physical calibration pending |
| 0C8 B4:B5 | BE16 / 100 | Speed channel B; physical calibration pending |
| 0C8 B6 | Raw 8-bit distance counter | Delta `(new-old)&255` |
| 188 B0 | 0, 1–5, or 7 | Steady forward gear/status; 7 also occurs in R |
| 188 B1 | 0, 1–5, or 6 | Target/commanded gear; 6 is reverse |
| 188 B3 | Selector enum below | Zero means between positions/unknown |
| 1F4 B0 & 20 | Left turn request | Request state, not proven lamp flash phase |
| 1F4 B0 & 40 | Right turn request | Request state, not proven lamp flash phase |
| 1F4 (B0>>3)&3 | Wiper mode | 0 off, 1 intermittent, 2 low, 3 high |
| 1F4 B1 | Illumination level raw | Only 77 and 100 observed |
| 1F4 B3:B5 | BE24, odometer-like raw | Absolute conversion pending |
| 20C B4:B5 | BE16, RPM | Duplicate, at 50 Hz |
| 224 B2:B3 | BE16, fuel accumulator raw | Millilitres per raw tick pending |

Selector mapping in hexadecimal:
`01=P, 02=R, 04=N, 08=D, 20=D3, 40=2, 80=1`.
The end-of-log sweep exercises all these states. `00` occurs briefly between positions; `10` never appears. `188 B2 & 80` is a D-position-confirmed candidate, not a general forward-range flag: it is clear in D3, 2 and 1.

A forward shift is visible near source lines 58,449–59,012: B0/B1 goes through 07/03 and settles at 03/03. Reverse has 07/06 with selector 02, including source line 497,525.

The 20C RPM matches the latest preceding 12C RPM in 43,291 of 43,307 frames, or 99.963%. The other differences are no larger than 7 RPM and are consistent with sampling/update alignment.

Wiper and turn bits must be decoded independently. The observed sequence 44, 4C, 54, 5C combines a right-turn request with off, intermittent, low and high wipers. A whole-byte equality test would miss combined states.

## Strong new candidates

### Fuel-cut status: 0x0A6 B0 & 0x02

Thirteen asserted intervals total **55.910491 seconds**. The 0x224 counter remains exactly constant at every recorded fuel-counter sample inside all thirteen intervals. Across 560 interval-aligned fuel samples with this flag set, every fuel delta is zero. The longest asserted run is 10.968406 seconds.

This is strong evidence for an overrun/fuel-cut status. It is still a hypothesis until compared with a suitable independent sensor/status reference. A momentarily unchanged fuel counter alone is insufficient, because its quantized updates also pause briefly during normal low-rate fueling.

Exact start/end timestamps, counts and original source-line references are in `fuel_cut_intervals.csv`.

### Cruise buttons: 0x0D4 B0 & 0xC0

| Code | Proposed meaning | Evidence |
|---|---|---|
| 00 | No button | Baseline |
| 40 | SET/DECEL | 130 ms pulse at 119.100 s before first engagement |
| 80 | RESUME/ACCEL | Held 10.270 s during cruise acceleration; short pulses before re-engagement |
| C0 | CANCEL | Pulses at 300.211 s and 576.691 s, each immediately followed by disengagement |

Decode this as one four-state field. Interpreting 40 and 80 as unrelated booleans would mislabel C0 as two simultaneous buttons.

At 369.115 s, 12C B6 changes 08→09→01: brake appears while cruise is still active, and cruise clears 20 ms later. This supports keeping brake and cruise engagement as separate bits.

Button names remain strong candidates. No synchronized account of which buttons were pressed was included.

### Throttle-related channels: 0x0A6 B2, B3 and B4

B2 and B3 both span 4–208. B4 spans 0–196 and is zero throughout the initial idle. B2 changes tend to lead B3; derivative correlation peaks with B3 delayed approximately 60 ms. This supports a target/feedback hypothesis, with B4 potentially a relative-throttle or effective-demand channel.

These are not yet proven accelerator-pedal signals. Do not convert their observed maximum to “100% pedal,” assume a 255 denominator, or assign degrees. Reference pedal, actual throttle and commanded throttle separately.

### Cyclic accessory load: 0x0D4 B2 & 0x40

The bit cycles throughout the drive, roughly 10.8 seconds set and 18.6 seconds clear in the central section. During the first 45 seconds of stationary idle, B2/B3 throttle candidates average about 8 when it is set and about 5 when clear. Average raw fuel-counter rate also rises, while RPM stays near 800.

A/C compressor request, fan demand or another periodic accessory load is plausible. The log alone cannot identify the accessory or prove physical clutch engagement. This is a useful target for an A/C on/off experiment.

### Illumination and parked-state flags

405 B3 bit3 perfectly matches the latest 1F4 illumination level in all 2,887 samples: set when the level is 77, clear when it is 100. It is a strong illumination-active candidate; distinguish parking/tail lamps from headlights before naming it.

0D4 B0 bit2 and 405 B2 bit5 agree in 2,886/2,887 aligned samples. They are set before driving and after stopping, with repeated toggles while parked. Parking-brake and seatbelt status are hypotheses, not established labels.

405 B2 bit2 sets at 842.791 s and stays set. Test doors and seatbelts independently.
0D4 B0 bits0 and1 are lighting-state candidates, including a possible high-beam bit. They need an explicit stalk test.

## Distance and odometer: calibration must be explicit

0C8 B6 starts at 12 and ends at 157. It advances exactly 1,681 times, always by one modulo 256, including six wraps.

Channel B speed integration gives 16.804771 nominal km. Treating a counter tick as 10 metres gives 16.810000 nominal km, agreement within about 0.031%. This is strong internal consistency, not independent distance calibration.

Channel A is approximately 0.97984 times channel B above 10 nominal km/h. Its integrated value is 16.466006 nominal km. Both are useful to preserve until compared with GPS and the dashboard.

The coarse odometer-like value changes from [absolute reading withheld] to [absolute reading withheld] in ten steps. The nine complete intervals between those steps contain **exactly 164 fine ticks each**. The first boundary comes after 46 ticks because recording begins partway through that interval.

If each coarse update corresponds to one displayed mile, the trip distance is `1681/164 = 10.25 miles`. The earlier 10.45-mile figure used the unverified 10-metre tick convention. Neither establishes GPS ground distance.

One model fitting all eleven coarse values is `raw = floor(1.61 * displayed_miles)`, with displayed values [absolute reading withheld] through [absolute reading withheld]. This is a fitted interpretation, not an independently observed dashboard reading. Applying an exact km-to-mile divisor instead can yield a materially different absolute odometer. Obtain a dashboard anchor before deploying any absolute-mileage conversion.

0D4 B5:B6 /100 is a strong filtered-speed candidate. It closely tracks the 0C8 higher channel with about 0.2–0.3 seconds of lag and an unresolved offset/scale convention. Do not integrate it for distance in preference to the fine counter.

## Fuel quantities and sender calibration

The raw accumulator progresses from 642 to 15,878: **15,236 raw ticks**. Every value is even. Right-shifting once produces a 15-bit counter advancing by **7,618 half-count units**. These are two representations of the same counter.

Use one convention consistently:
```
raw_delta = (new_raw - old_raw) & 0xFFFF
half_delta = (new_half - old_half) & 0x7FFF
mL_per_half_count = 2 * mL_per_raw_tick
```
No raw counter wrap or reset occurs in this log. Across a key-off, reboot, data gap or reset, establish continuity first; blindly interpreting a reset as rollover produces a large false fuel event.

Full-to-full calibration:
`mL_per_raw_tick = gallons_dispensed * 3785.411784 / sum(valid_raw_deltas)`.

0D4 B3 and B4 are fuel-gauge/sender candidates inherited from the 2003 work. Here their ranges are 5–51 and 128–199, with correlation −0.8096. This does not establish litres, percentage, resistance or a linear conversion. Record a known fill and stable parked readings, then collect several tank levels.

## Test plan, in execution order

### T1. Labeled parked controls

Keep raw CAN plus Pi-clock event markers. On level ground in P, independently repeat parking-brake and seatbelt toggles, each door, parking/headlights/high-beam/flash, dimmer positions, indicators/hazards and wet-screen wiper modes. Perform one slow selector sweep with foot brake held. Three repeats per independent switch.

Targets: 0D4 B0 bits0:2, 405 B2 bits2,5 / B3 bit3, 1F4 B0/B1, 188 B0:B3.

Pass condition: Same bits respond on three independent repeats; establish on/off polarity and reject cross-coupled controls.

### T2. Cyclic load / A/C

Park outside, engine warm, blower held fixed. Mark A/C off for 60s, on for 120s, off for 60s, then repeat. Separate rear-defog and blower-only tests. Compare 0D4 B2 bit6, throttle candidates, raw fuel rate and observed compressor/fan operation from a safe distance.

Targets: 0D4 B2 bit6, 0A6 B2:B4, 224 fuel counter.

Pass condition: Show repeatable dependence on requested control; identify commanded versus physical actuation. Do not equate a status bit to proof that compressor clutch moves.

### T3. Cruise button identity

While stationary first mark single SET/DECEL, RESUME/ACCEL and CANCEL presses, separately and three times each. Test master button separately. If no stationary bus response, a passenger labels normal legal-speed cruise operations. No need for hard acceleration.

Targets: 0D4 B0 bits7:6, 12C B6 bit3, constant status bits.

Pass condition: Directly label the 0x40/0x80/0xC0 enum and distinguish cruise master, button press and engaged status.

### T4. Read-only OBD reference pairing

With supported PIDs only, pair independent OBDLink EX sensor readings with passive can0 capture. First ignition-on/engine-off slow pedal sweeps; then normal idle and gentle driving with no driver interaction with logger. Compare RPM, coolant, IAT, speed, throttle actual/relative/commanded, pedal sensors and fuel/injector status where available.

Targets: 12C RPM/temperatures, 0A6 B2/B3/B4, 0A6 B0 bit1, 20C RPM, 224 B1.

Pass condition: Fit bytes to independently measured quantities and units across rising/falling values. Separate throttle target/feedback from physical accelerator pedal.

### T5. Distance and odometer calibration

Record actual dashboard odometer and trip readings at start/end; record at least 5-10 displayed mile increments with passenger video or equivalent synchronized evidence. Log GPS speed/distance on normal clear-sky roads. Compare both speed channels, fine B6 wraps and 1F4 raw updates.

Targets: 0C8 B0:B1/B4:B5/B6, 0D4 B5:B6, 1F4 B3:B5.

Pass condition: Establish whether each coarse update is exactly one displayed mile. Only then use 164 ticks/mi for cluster-relative distance. Independently fit physical distance to GPS; anchor absolute odometer rather than assuming raw km.

### T6. 2007 fuel calibration

Log an uninterrupted full-to-full tank interval, allowing a new counter baseline at every ignition session. Save gallons dispensed, distance and counter sum. Confirm B3/B4 sender direction with a known fill and parked settled readings. Repeat another tank.

Targets: 224 B2:B3, 0D4 B3/B4.

Pass condition: ml_per_raw_tick = gallons_dispensed * 3785.411784 / summed_raw_deltas. A half-count representation needs twice that factor. Never integrate a reset as rollover; verify counter behavior across key cycles.

### T7. Ignition and availability

Keep Pi powered independently while stationary. Label OFF, ACC, ON with engine off, crank, running, then shutdown/ACC/OFF. Record several cycles and boundary timestamps; do not infer key state from the absence of one packet.

Targets: all IDs and message rates, counter baselines, constant/unknown bytes, CarStats sleep/wake.

Pass condition: Measure actual traffic availability and reset behavior. Establish fresh/stale/unavailable states and safe timeout logic from observations.

## Reference PIDs for T4

Use only supported read-only Mode 01 queries. The public python-OBD command table identifies:
05 coolant, 0C RPM, 0D speed, 0F intake temperature, 11 absolute throttle, 45 relative throttle, 49/4A/4B accelerator positions, 4C commanded throttle actuator, and 5A relative accelerator position. 2F fuel level and 5E fuel rate may help if supported. Support on this Accord is not established by their existence in the standard.

Source for these test-reference names only:
https://python-obd.readthedocs.io/en/latest/Command%20Tables/

The public reference does not establish any proprietary CAN decoding in this report.

## Capture method and acceptance rules

Keep passive `candump -L can0` capture at full resolution. Add a separate marker file using the same Pi clock. While parked, a marker can be written as:
```
printf '%s,%s\n' "$(date +%s.%N)" 'PARKING_BRAKE_ON' >> markers.csv
```
Mark before and after each action, leave several seconds between states, and repeat one control at a time. A passenger handles all driving-phase observations and equipment. All experiments use passive logging or normal read-only diagnostics, not spoofed control frames.

The engine is running at both ends of this capture; RPM never reaches zero. It cannot establish ACC/OFF traffic behavior, engine-start resets, Pi wake-up behavior or a reliable key-off timeout. Test T7 is required for those features.

For CarStats, retain raw unknown fields and keep experimental labels opt-in. Preserve native timestamps and counters even if the display refreshes less often. Mark stale values unavailable rather than silently treating them as zero. Prioritize known telemetry first, candidate validation second, calibrated fuel/distance third. None of these findings authorizes changing the vehicle's control messages.

## Package contents

- `signal_map.json`: 35 signal definitions, confidence, caveats, field locations, unresolved bytes and validation tasks. An analysis schema, not a drop-in CarStats profile.
- `decoded_10hz.csv`: 8,657 rows and 41 columns of decoded/candidate data, latest preceding message on a 0.1-second grid from 0.2 to 865.8 seconds. Nominal units and raw fields are explicitly named.
- `events_native_resolution.csv`: 465 timestamped state records, including initial states and transitions at original message resolution. Use this for short button presses and the 20-ms brake/cruise overlap that 10-Hz resampling can miss.
- `fuel_cut_intervals.csv`: all thirteen candidate fuel-cut intervals with source references and counter behavior.
- `odometer_transitions.csv`: all eleven raw states and corresponding fine ticks.
- `byte_inventory.json`: every byte's observed values, frequencies, changes and variable-bit mask.
- `capture_summary.json`: full-capture metrics.

The raw log is not duplicated in the package. Retain it as the authoritative source. Its SHA-256 is:
`[original source hash withheld]`.

