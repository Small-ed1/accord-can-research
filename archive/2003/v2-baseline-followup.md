# Sanitized historical source: 03-V2

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# 2003 Honda Accord F-CAN Decode Findings :  Consolidated Export v2

**Export date:** [date withheld]  
**Vehicle context:** 2003 Honda Accord EX, K24A4, automatic transmission  
**Dataset:** [date withheld] captures plus overlapping CarStats OBD telemetry  
**Purpose:** consolidate every defensible finding from the original decode pass and the deeper old-dump-only analysis.

> These mappings describe the supplied car/capture. They are not claimed as a universal OEM specification for every 7th-generation Accord. Confidence labels are part of the data and should be preserved in CarStats.

## 1. Executive summary

The supplied F-CAN capture contains exactly six standard 11-bit CAN IDs, each with an 8-byte payload:

- `0x0C8` :  vehicle motion / distance
- `0x0D4` :  meter/cluster status and motion-related data
- `0x12C` :  engine/gauge data
- `0x188` :  transmission / selector data
- `0x1F4` :  meter/cluster status plus odometer-like total
- `0x224` :  engine message containing a strong fuel-use accumulator candidate

The original pass OBD-validated **RPM, coolant temperature, intake-air temperature, and vehicle speed**. The deeper pass strengthens the transmission and distance interpretation and identifies new high-value status candidates: **parking brake, A/C active/request, engine-off flags, MIL command, turn/wiper packed status, and a likely fuel-pulse/fuel-use accumulator**.

The most important new practical result is `0x224 B2:B3`: its accumulation rate responds strongly to engine load, not just RPM. Honda service information independently states that the 2003 Accord ECM/PCM sends **fuel pulses via F-CAN** for trip-computer fuel-economy calculation. This makes `0x224 B2:B3` a strong candidate for the signal CarStats ultimately needs for direct CAN fuel-use/MPG calculations. The physical scaling remains unknown.

## 2. Capture inventory

| Capture | Frames | Duration | Local time, [date withheld] |
|---|---:|---:|---|
| `keyon-engine-off.log` | 2,248 | 5.156 s | [wall-clock time withheld]–[wall-clock time withheld] |
| `idle.log` | 8,700 | 19.990 s | [wall-clock time withheld]–[wall-clock time withheld] |
| `rpm-test.log` | 15,229 | 34.987 s | [wall-clock time withheld]–[wall-clock time withheld] |
| `2003-drive-a.log` | 783,216 | 1,799.975 s | [wall-clock time withheld]–[wall-clock time withheld] |
| **Total** | **809,393** | | |

Approximate message rates:

- `0x0C8`, `0x0D4`, `0x12C`, `0x188`: ~100 Hz
- `0x1F4`: ~25 Hz
- `0x224`: ~10 Hz

Observed bus configuration: **500 kbit/s Classical CAN, standard 11-bit identifiers, listen-only capture**.

The OBD archive provides 2,666 valid sample records overlapping the drive from about [wall-clock time withheld] to [wall-clock time withheld]. The earlier KOEO, idle, and RPM-test captures do not have overlapping OBD telemetry.

## 3. Confidence model

- **OBD-validated:** independently compared with decoded OBD PID measurements.
- **Very high / strong internal inference:** capture behavior, counters, integration, transition structure, or independent related-Honda evidence makes the mapping highly persuasive, but it lacks a direct labeled physical reference on this car.
- **Strong candidate:** evidence is good enough to use experimentally, but CarStats should retain a candidate/inferred marker until a labeled test confirms it.
- **Partially understood:** field behavior is known, semantic identity or scale is not.
- **Unresolved:** do not assign a user-facing semantic label yet.

## 4. Consolidated signal table

| CAN ID | Location | Finding | Decode / values | Confidence |
|---|---|---|---|---|
| `0x12C` | B4:B5 | Engine RPM | `BE16(B4,B5)` RPM | **OBD-validated** |
| `0x12C` | B0 | Coolant | `B0 - 40` °C | **OBD-validated** |
| `0x12C` | B1 | Intake air | approx. `B1 - 40` °C | **OBD-validated** |
| `0x0C8` | B4:B5 | Native vehicle speed | `raw × 0.01 km/h` | **Very high** |
| `0x0C8` | B4:B5 | OBD-equivalent speed | `raw × 0.0098 km/h` | **OBD-calibrated for this capture** |
| `0x0C8` | B6 | Distance ticks | modulo-256; approx. `0.01 km/tick` | **Very high** |
| `0x0D4` | B0 bit2 | Parking-brake candidate | mask `0x04` | **High candidate** |
| `0x0D4` | B2 bit6 | A/C active/request candidate | mask `0x40` | **High candidate** |
| `0x0D4` | B2 bit7 | Engine-off/KOEO candidate | mask `0x80` | **High candidate** |
| `0x0D4` | B3 | Longitudinal dynamics raw A | raw | **Medium** |
| `0x0D4` | B4 | Longitudinal dynamics raw B | raw | **Medium** |
| `0x0D4` | B5:B6 | Secondary speed-related value | `BE16(B5,B6)` | **Very high speed relation** |
| `0x12C` | B6 bit4 | MIL/check-engine command candidate | mask `0x10` | **High candidate** |
| `0x12C` | B6 bit0 | Engine status bit | raw | **Unresolved** |
| `0x188` | B0 | Current gear | `1–5` forward, `7` shifting/engaging | **High** |
| `0x188` | B1 | Target gear | `1–5` forward target; `6` seen crossing R | **High** |
| `0x188` | B2 bit7 | Transmission/interlock flag | mask `0x80` | **Unresolved** |
| `0x188` | B3 | Selector | `1=P, 2=R, 4=N, 8=D, 0=transition` | **Very high** |
| `0x1F4` | B0 | Turn/wiper packed status candidate | observed `04,0C,1C,24,2C,3C,44` | **High external correlation** |
| `0x1F4` | B3:B5 | Odometer/total-distance candidate | `BE24(B3,B4,B5)` | **High** |
| `0x224` | B2:B3 | Fuel-pulse/fuel-use accumulator candidate | `BE16(B2,B3)` | **High** |
| `0x224` | B6 bit1 | Engine-off candidate | mask `0x02` | **High** |

## 5. Message-by-message findings

### 5.1 `0x0C8` :  vehicle motion and distance

**B4:B5: speed.** This field is unmistakable. Against OBD, `raw × 0.0098 km/h` reproduces the integer PID extremely well: 454/458 matched readings are exact and the remaining four differ by only 1 km/h.

However, the **native CAN distance convention is better represented by `raw × 0.01 km/h`**. Integrating that value over the drive gives approximately 8.60 km, matching the unwrapped B6 distance counter. It also makes the spacing between complete `0x1F4` odometer-candidate updates approximately one mile.

Recommended CarStats handling:

- canonical CAN physical speed: `BE16(B4,B5) / 100` km/h
- preserve an optional OBD-equivalent presentation/calibration path using `×0.0098` when reproducing OBD PID integer behavior matters
- do not silently mix the two scales

**B6: distance tick counter.** Treat as a modulo-256 counter and accumulate `delta = (new-old) & 255`. Strong evidence supports approximately **0.01 km per tick** in the native convention.

### 5.2 `0x0D4` :  meter/cluster status + secondary motion data

#### B0 bit2 :  parking-brake candidate

Across the entire drive B0 has only two state transitions after its initial state:

- `0x04 -> 0x00` at **195.517 s**, while stopped, as the transmission enters the driving phase
- `0x00 -> 0x04` at **755.662 s**, while stopped after returning to Park

Global counts: `{'0': 56024, '4': 130022}`.

This is highly compatible with a parking-brake/handbrake status bit. It should remain marked **inferred** until one labeled handbrake test confirms it.

#### B2 bit6 :  A/C active/request candidate

Observed B2 values are only `0x00`, `0x40`, and `0xC0`:

- KOEO: **all 516 frames = `0xC0`**
- idle: **all 2,000 frames = `0x40`**
- RPM test: `0x40`/`0x00` cycling, 3 transitions after initial state
- drive: `0x40`/`0x00` cycling, 26 transitions after initial state in the portion where cycling occurs

That behavior strongly resembles compressor/request cycling. The safe label is **A/C active/request candidate**, not necessarily the dashboard A/C button state.

#### B2 bit7 :  engine-off/KOEO candidate

The extra `0x80` bit exists in every KOEO frame and disappears in all running captures. This is a strong engine-off/KOEO status candidate.

#### B3/B4 :  longitudinal dynamics pair

Parked behavior:

- KOEO: exactly B3=`87`, B4=`77`
- idle: B3=`86–87`, B4=`77–78`
- RPM test: B3=`86–87`, B4=`77–78`

Driving behavior:

- B3 range: `48–105`
- B4 range: `22–134`
- B3 and B4 are strongly inverse
- they move with longitudinal acceleration/deceleration, not with parked RPM

One-second speed-derived acceleration bins from the drive:

| Condition | Samples | Median accel m/s² | Median B3 | Median B4 |
|---|---:|---:|---:|---:|
| hard_decel | 3162 | -2.084 | 101.0 | 56.0 |
| mild_decel | 2968 | -0.772 | 94.0 | 67.0 |
| slight_decel | 9925 | -0.208 | 88.0 | 75.0 |
| steady | 142781 | 0.000 | 87.0 | 77.0 |
| slight_accel | 11829 | 0.203 | 87.0 | 77.0 |
| mild_accel | 8692 | 0.911 | 84.0 | 81.0 |
| hard_accel | 466 | 1.628 | 89.0 | 77.0 |

These fields should **not** be labeled throttle, MAP, or engine load. A neutral name such as `LongitudinalDynamicsRawA/B` is appropriate until scale/source are identified.

#### B5:B6 :  secondary speed-related value

Correlation with the primary `0x0C8` speed raw value is **0.999898** over the drive. Exact source, filtering, lag and scale remain unresolved.

### 5.3 `0x12C` :  engine/gauge data

**B0 coolant:** `B0 - 40 °C`; 227/230 OBD comparisons exact.

**B1 intake air:** approximately `B1 - 40 °C`; all 93 comparisons within 1 °C.

**B4:B5 RPM:** direct big-endian RPM. 872 OBD comparisons, mean absolute error 0.423 RPM. Do **not** divide by four.

#### B6 bit4 :  MIL/check-engine command candidate

Observed states:

- KOEO: **all 517 frames have B6=`0x10`**
- running captures: bit4 is absent

This matches the expected key-on bulb-check/MIL-command lifecycle. Related Honda/Acura reverse-engineering work independently places MIL behavior in the same message family. Keep the CarStats field marked inferred until a labeled MIL on/off test is captured.

#### B6 bit0 :  unresolved engine-status bit

B6=`0x01` occurs dynamically during the drive (33,808 frames globally), but the old dump does not provide a clean labeled event that identifies it. Do not assign a semantic meaning.

### 5.4 `0x188` :  transmission

#### B0 current gear

Codes `1–5` track the five forward gears. Code `7` is **not reverse**: it appears in 38 runs totaling 4,297 frames and every entry coincides with a target-gear change. Treat `7` as shifting/engaging.

#### B1 target gear

Tracks requested forward gear and changes before the completed/current gear. Code `6` appears briefly while the selector passes through R; stable reverse driving was not recorded, so its exact reverse interpretation remains unvalidated.

#### B3 selector

Strong mapping:

- `0 = transition / no stable position`
- `1 = P`
- `2 = R`
- `4 = N`
- `8 = D`

This mapping is supported by the captured P-R-N-D sequence and independently matches known Honda-family patterns.

#### B2 bit7

Observed as `0x80` in 56,100 frames and `0x00` in 129,976 frames. It is tempting to label it “Drive/engaged,” but related-Honda captures can show the same bit while in Park, so that interpretation is rejected. Leave unresolved.

### 5.5 `0x1F4` :  meter status + odometer candidate

#### B0 packed status

Observed values and counts:

- `0x04`: 42,504 frames
- `0x0C`: 1,437 frames
- `0x1C`: 31 frames
- `0x24`: 584 frames
- `0x2C`: 749 frames
- `0x3C`: 4 frames
- `0x44`: 1,202 frames

The values form a clean combinatorial bitfield structure rather than arbitrary analog data. Earlier Honda-family reverse-engineering maps compatible patterns to turn-signal and wiper states. A useful candidate decomposition is:

- turn-state contribution: `0x00` none, `0x20` left candidate, `0x40` right candidate
- wiper contribution: `0x00` off, `0x08` intermittent candidate, `0x10` low candidate, `0x18` high candidate
- persistent base bit `0x04` in all observed values

Observed combinations include `0x2C = 0x20 + 0x0C` and `0x3C = 0x20 + 0x1C`, which supports independent packed subfields. The capture itself was not event-labeled for turn/wiper operation, so semantic names should remain **externally-correlated candidates**, not local confirmation.

#### B3:B5 odometer / total-distance candidate

Raw value rises from **[absolute reading withheld] to [absolute reading withheld]**. Its update spacing tracks long distance intervals and four complete intervals line up at approximately one mile under the native `0x0C8` speed convention. The exact absolute units, display offset, and full field width remain unconfirmed.

### 5.6 `0x224` :  engine fuel-use candidate

#### B2:B3 running accumulator

Raw behavior from the original captures:

- KOEO: 0
- idle: 544 -> 630
- RPM test: 908 -> 1136
- drive: 1458 -> 15388

The deeper analysis looked at **rate of accumulation**, not just absolute value. Median ~2-second rates by RPM band:

#### Idle capture
- [0, 1000): 4.001 counts/s

#### Parked RPM-test capture
- [0, 1000): 4.002 counts/s
- [1000, 1500): 5.003 counts/s
- [1500, 2000): 7.004 counts/s
- [2000, 2500): 10.006 counts/s
- [2500, 3000): 13.006 counts/s
- [3000, 4000): 13.006 counts/s

#### Road-driving capture
- [0, 1000): 4.001 counts/s
- [1000, 1500): 5.002 counts/s
- [1500, 2000): 15.005 counts/s
- [2000, 2500): 30.010 counts/s
- [2500, 3000): 41.014 counts/s
- [3000, 4000): 52.017 counts/s
- [4000, 5000): 65.522 counts/s

The key result is the same-RPM load separation: around 2,000–2,500 RPM, parked revving is about **10 counts/s**, while road driving is about **30 counts/s**. At 2,500–3,000 RPM the difference is roughly **13 counts/s parked versus 41 counts/s driving**. This strongly rejects a simple elapsed-time or crank-revolution counter and points toward a quantity that rises with engine work/fueling.

Honda's 2003 Accord service information independently states that the ECM/PCM sends **fuel pulses via F-CAN** to the navigation trip computer for fuel-economy calculation. Combined with the observed accumulator behavior and the related-Honda architecture assigning `0x224` to the engine side, `B2:B3` is a strong **fuel-pulse / cumulative fuel-use candidate**.

Do **not** yet convert counts to liters, gallons, injector milliseconds, or mass. Physical scaling requires a fuel-consumption reference.

#### B6 bit1 :  engine-off candidate

- all 52 KOEO `0x224` frames: B6=`0xE2`
- all 18,556 running frames: B6=`0xE0`

Bit1 therefore behaves as a strong engine-off/source-state candidate.

## 6. Rolling counters and checksum

All six message IDs contain an independent 2-bit rolling counter:

```python
counter = (data[7] >> 6) & 3
```

Each ID advances `0,1,2,3` independently. Across all four captures there were **zero observed counter discontinuities**.

For `0x0D4`, `0x12C`, `0x188`, and `0x224`, the low nibble of B7 is validated by:

```python
expected = (
    -sum((b >> 4) + (b & 0x0F) for b in data[:7])
    - (data[7] >> 4)
) & 0x0F
valid = (data[7] & 0x0F) == expected
```

It passes **576,806 / 576,806** applicable frames. No CAN-ID contribution is needed for the observed formula. The low nibble is always zero for `0x0C8` and `0x1F4`; the checksum formula is not claimed for those IDs.

## 7. What the old dump still cannot identify defensibly

The following were screened against the OBD overlap but no direct CAN field could be established without confusing indirect RPM/speed correlation for identity:

- analog throttle position
- MAP
- engine load
- battery/control-module voltage
- ignition advance
- fuel trims
- O2 / A-F sensor values

Other unresolved pieces:

- `0x12C B6 bit0`
- `0x188 B2 bit7`
- `0x1F4 B1`
- `0x224 B1`
- exact physical meaning and calibration of `0x0D4 B3/B4`
- exact physical scale of `0x224 B2:B3`
- exact absolute units/offset of `0x1F4 B3:B5`
- hazard-state encoding and other meter-status bits not deliberately exercised

## 8. Recommended CarStats integration boundary

### Safe to use now as primary CAN data

- RPM
- coolant temperature
- intake-air temperature
- native speed
- distance-tick deltas
- selector P/R/N/D
- forward current/target gear, while treating code 7 as shift/engage

### Safe to expose as inferred/experimental

- parking brake candidate
- A/C active/request candidate
- MIL command candidate
- turn/wiper packed status candidate
- odometer raw candidate
- fuel-use accumulator raw/rate

### Keep raw-only

- `0x0D4 B3/B4` until physical identity/scale is known
- `0x12C B6 bit0`
- `0x188 B2 bit7`
- `0x1F4 B1`
- `0x224 B1`

## 9. Highest-value confirmation tests

These are no longer discovery from scratch. They are targeted confirmations:

1. **Parked:** labeled parking-brake release/apply, A/C on/off, turn signals, wiper speeds, MIL condition if naturally available.
2. **Parking lot:** stable reverse driving and selector holds.
3. **Fuel calibration:** compare `0x224` count deltas against a defensible fuel-use reference over a sufficiently long interval.
4. **Road:** controlled same-RPM/different-load runs only if identifying the remaining drivetrain/dynamics fields is worth the effort.

## 10. Files in this export

- `CAN_FINDINGS_v2.md` :  this report
- `signal_map_v2.json` :  machine-readable consolidated signal map and confidence labels
- `signal_summary_v2.csv` :  flattened signal inventory
- `evidence_stats_v2.json` :  raw aggregate evidence used for the new interpretations
- `SOURCES.md` :  local and external provenance
- `original_signal_map_v1.json` :  untouched first-pass signal map for comparison
- `original_accord_2003_observed_v1.dbc` :  untouched first-pass DBC
- `original_accord_can_decode_report_v1.md` :  untouched first-pass report

The original DBC is intentionally not silently rewritten with candidate bitfields. The v2 JSON is the authoritative research handoff until the new candidates receive explicit physical confirmation.

