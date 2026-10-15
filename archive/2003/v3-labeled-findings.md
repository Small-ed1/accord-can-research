# Sanitized historical source: 03-V3

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# 2003 Honda Accord F-CAN Decode Findings :  Consolidated Export v3

**Export date:** [date withheld]  
**Vehicle:** 2003 Honda Accord EX, K24A4, automatic  
**Bus:** 500 kbit/s Classical CAN, standard 11-bit IDs, 8-byte frames  
**Observed IDs:** `0x0C8`, `0x0D4`, `0x12C`, `0x188`, `0x1F4`, `0x224`  
**Capture policy:** listen-only

> This is the canonical research handoff as of this export. It combines the original 809,393-frame CAN/OBD analysis with four new labeled vehicle tests on [date withheld]. Mappings describe the supplied car and captures; they are not claimed as a universal Honda OEM specification. Confidence labels and caveats are part of the data.

## 1. What is now decoded

### Production-ready / vehicle-confirmed or OBD-validated

- Engine RPM
- Coolant temperature
- Intake-air temperature
- Native vehicle speed and distance ticks
- Brake pedal switch
- Parking brake
- Lighting state: off / aux-parking / low / high
- A/C active/request behavior
- Current gear and target gear, including Reverse and shift-transition code
- Full physical selector: P / R / N / D / D3 / 2 / 1
- Wiper state: off / intermittent / slow / fast-manual-up
- Left/right turn-signal status
- Whole-kilometer odometer total
- Cumulative fuel-use/fuel-pulse counter, currently unscaled to gallons/liters

### Very strong / usable with caveat

- Fuel gauge angle and fuel-sender voltage representation
- MIL/check-engine command bit
- Secondary/filtered speed
- `0x0D4 B2 bit7` as an oil-pressure-switch/engine-off candidate
- `0x188 B2 bit7` as a D-range/Drive-state candidate
- `0x224 B6 bit1` as an engine-off/source-state candidate

### Still unresolved

- Physical fuel volume per `0x224` accumulator count
- Exact meaning of `0x1F4 B1`, rare `0x1F4 B2`, and `0x224 B1`
- Exact filter/source semantics of secondary speed `0x0D4 B5:B6`
- Direct mappings for throttle, MAP, calculated load, voltage, ignition advance, trims, or O2/A-F values were not defensibly established in these six F-CAN IDs

## 2. Evidence inventory

### Original [date withheld] dataset

| Capture | Frames | Duration | Purpose |
|---|---:|---:|---|
| `keyon-engine-off.log` | 2,248 | 5.156 s | KOEO baseline |
| `idle.log` | 8,700 | 19.990 s | running idle |
| `rpm-test.log` | 15,229 | 34.987 s | stationary RPM excitation |
| `2003-drive-a.log` | 783,216 | 1,799.975 s | road drive + overlapping OBD |
| **Original total** | **809,393** | | |

The overlapping OBD archive supplied 2,666 valid records. The first pass validated RPM, speed, coolant, and intake-air temperature against OBD.

### New labeled [date withheld] tests

| Capture | Frames | Duration | Local start | Main purpose |
|---|---:|---:|---|---|
| `can-test.log` | 74,439 | 171.098 s | [wall-clock time withheld] | brake, lights/high beams, A/C/recirc, parking brake, cruise main, wipers, mist |
| `can-test-lights.log` | 8,340 | 19.169 s | [wall-clock time withheld] | dedicated off → aux → low → high lighting test |
| `can-test-shifter.log` | 22,067 | 50.719 s | [wall-clock time withheld] | stationary full selector sweep |
| `can-test-fuel.log` | 53,999 | 124.131 s | [wall-clock time withheld] | cruise → acceleration → closed-throttle coast → cruise |
| **New total** | **158,845** | | | |

**Combined frames represented by this handoff: 968,238.**

All four new logs preserved uninterrupted two-bit rolling counters for all six IDs. Every applicable `0x0D4`, `0x12C`, `0x188`, and `0x224` frame passed the previously derived nibble checksum.

## 3. Canonical signal map

### `0x0C8` :  vehicle motion / distance (~100 Hz)

**B4:B5 :  native vehicle speed**

```text
raw = BE16(B4,B5)
speed_kph = raw / 100
```

Use this as the canonical CAN-native scale. The original OBD comparison also found an empirical `raw × 0.0098 km/h` presentation that reproduced the integer generic OBD speed PID extremely closely, but that is best treated as an OBD-equivalent calibration, not the native distance convention.

**B6 :  distance ticks**

```text
delta = (new - old) & 0xFF
distance_km += delta * 0.01
```

The new fuel test produced exactly **200 ticks = 2.00 km**, while integrating native CAN speed over the same log gave **2.008 km**.

### `0x0D4` :  gauge/meter data (~100 Hz)

**B0 bits 0-1 :  lighting state :  VEHICLE CONFIRMED**

| Code | State |
|---:|---|
| `0` | off |
| `1` | aux / parking lights |
| `2` | low beams |
| `3` | high beams |

The dedicated lights capture held the parking brake on and produced `0x04 → 0x05 → 0x06 → 0x07`, then reversed, isolating these low two bits cleanly.

**B0 bit 2 (`0x04`) :  parking brake :  VEHICLE CONFIRMED**

This bit is additive with the lighting state.

**B2 bit 6 (`0x40`) :  A/C active/request :  VEHICLE CONFIRMED BEHAVIOR**

It tracks the A/C test but also cycles automatically, so use the semantic **A/C active/request/compressor-related**, not simply “A/C button is latched.”

**B2 bit 7 (`0x80`) :  oil-pressure-switch / engine-off candidate**

Asserted in KOEO captures and clear whenever the engine is running. Honda's gauge-module data list includes a discrete oil-pressure-switch input described as ON with engine stopped/low pressure and OFF running. This is therefore a strong candidate, but it has not been directly tested by manipulating oil pressure.

**B3 :  fuel-level gauge angle :  VERY HIGH CONFIDENCE**

Honda's gauge data list defines a fuel-level representation of approximately **5° empty, 50° half, 100° full**. The stationary labeled tests show `B3 = 47–48`; the road fuel run spans `5–72` as fuel sloshes.

**B4 :  fuel-sender voltage :  VERY HIGH CONFIDENCE**

A strong physical approximation is:

```text
volts ≈ B4 * 5 / 255
```

Honda's gauge data list describes approximately **4 V empty, 2.5 V half, 1 V full**. Stationary `B4 = 132–134` gives about **2.59–2.63 V**, matching the half-tank region. In the road test B3/B4 were strongly inverse (`r ≈ -0.939`) and moved violently with slosh, which explains why an earlier pass mistook them for longitudinal-dynamics fields.

**Implementation:** heavily filter fuel level and prefer low-acceleration/steady-state samples. Do not display raw instantaneous percentage during hard acceleration/braking.

**B5:B6 :  secondary speed**

Strongly speed-related and naturally scaled near `raw / 100 km/h`, but it behaves like a filtered/lagged variant in motion. Exact source/filtering remains unresolved.

### `0x12C` :  engine/gauge data (~100 Hz)

**B0 :  coolant:** `B0 - 40 °C` :  OBD validated.  
**B1 :  intake air:** approximately `B1 - 40 °C` :  OBD validated identity.  
**B4:B5 :  RPM:** `BE16(B4,B5)` RPM :  OBD validated, no divide-by-four.

**B6 bit 0 :  brake pedal :  VEHICLE CONFIRMED**

The labeled switch test produced three deliberate ~5-second brake presses:

- 10.863–16.272 s
- 21.312–26.481 s
- 31.140–36.139 s

The bit asserted for each press and cleared between them.

**B6 bit 4 (`0x10`) :  MIL/check-engine command :  VERY HIGH CONFIDENCE**

It is set throughout KOEO and absent in normal running captures, matching the expected bulb-check/indicator lifecycle. No deliberate MIL fault test was performed.

### `0x188` :  transmission (~100 Hz)

**B0 :  current/actual gear :  VEHICLE CONFIRMED**

| Code | Meaning |
|---:|---|
| `0` | P/N, distinguish with selector |
| `1` | 1st |
| `2` | 2nd |
| `3` | 3rd |
| `4` | 4th |
| `5` | 5th |
| `6` | Reverse |
| `7` | shifting / engaging |

Code 7 is explicitly **not Reverse**.

**B1 :  target/requested gear**

`0=P/N`, `1–5=forward targets`, `6=Reverse`. Target changes before actual gear during shifts.

**B2 bit 7 (`0x80`) :  D-range/Drive-state candidate**

In the labeled selector capture it was asserted in **D** and clear in **P/R/N/D3/2/1**. It is redundant with the selector field and its exact internal purpose remains unknown, so keep it experimental.

**B3 :  physical selector :  VEHICLE CONFIRMED**

| Raw | Position |
|---:|---|
| `0x00` | transition / between detents |
| `0x01` | P |
| `0x02` | R |
| `0x04` | N |
| `0x08` | D |
| `0x20` | D3 |
| `0x40` | 2 |
| `0x80` | 1 |

This closes the earlier gap where positions 1 and 2 had been treated as “not shown.” They are present; the decoder simply had not mapped `0x40` and `0x80`. D3=`0x20` was manually confirmed and locked.

### `0x1F4` :  meter status + odometer (~25 Hz)

**B0 :  packed wiper + turn state :  VEHICLE CONFIRMED**

Base value is `0x04`. Add these independent components:

**Wiper contribution**

| Add | Result with no turn | Meaning |
|---:|---:|---|
| `0x00` | `0x04` | off |
| `0x08` | `0x0C` | intermittent |
| `0x10` | `0x14` | slow |
| `0x18` | `0x1C` | fast **or manual-up** |

- **Mist/pull-back is not represented.** The latest test ended with mist and the field remained at the off value.
- Manual-up and fast collapse to the same CAN state.
- Intermittent delay/speed setting is not represented in this byte.

**Turn contribution**

| Add | Example with wipers off | Meaning |
|---:|---:|---|
| `0x00` | `0x04` | none |
| `0x20` | `0x24` | left |
| `0x40` | `0x44` | right |

Combined values seen in the old dump, such as `0x2C` and `0x3C`, support the additive packed structure. **Hazards were not observed as a distinct encoding**, so do not invent `0x60` without evidence.

**B3:B5 :  total odometer in whole kilometers :  CONFIRMED/HIGH**

```text
odometer_km = BE24(B3,B4,B5)
```

Evidence:

- original drive: `[absolute reading withheld] → [absolute reading withheld]`, +8 counts over about 8.60 km
- new fuel run: `[absolute reading withheld] → [absolute reading withheld]`, +2 counts
- same fuel run: native speed integral = **2.008 km**; `0x0C8 B6` distance ticks = **2.00 km**

This is no longer merely “odometer-like.” It is the whole-kilometer total odometer representation. For a miles display, convert kilometers normally (`mi = km / 1.609344`).

**B1 :  unresolved**

Observed `0x3E` in the original dataset, `0x04` in the new parked tests, and `0x03` in the fuel road test. Keep raw-only.

### `0x224` :  engine fuel-use message (~10 Hz)

**B2:B3 :  cumulative fuel-use/fuel-pulse accumulator :  FUNCTIONALLY CONFIRMED**

```text
raw = BE16(B2,B3)
unwrap modulo 65536 across wraps
```

The decisive test is the [date withheld] road capture. During closed-throttle in-gear deceleration:

- accumulator froze exactly at **2338**
- duration: **17.598 s**
- vehicle remained moving: **103.41 → 83.90 km/h**
- engine remained spinning: **2134 → 1715 RPM**

That behavior matches deceleration fuel cut and rules out simple runtime or crank-revolution accumulation. Approximate regression slopes across the intended test phases were:

- first steady cruise: **~11.6 counts/s**
- acceleration: **~41.2 counts/s**
- closed-throttle coast: **0.0 counts/s**
- second steady cruise: **~17.4 counts/s**

Honda service documentation independently states that the navigation trip computer receives **fuel pulses via F-CAN from the ECM/PCM** to calculate fuel economy. The exact physical volume represented by one count is still unknown.

**What is needed for MPG:** calibrate `fuel_volume_per_count` once. Then CarStats can calculate instantaneous fuel rate, gallons used, trip MPG, and instantaneous MPG directly from CAN.

**B6 bit 1 :  engine-off/source-state candidate**

Set in every KOEO `0x224` frame (`B6=0xE2`) and clear in all running captures (`B6=0xE0`). Exact source semantics remain unknown.

## 4. Negative findings from labeled tests

These are useful constraints, not proof that the information can never exist elsewhere on the vehicle:

- **Rear defrost:** no clean discrete change identified among these six F-CAN IDs during the ~5 s labeled event.
- **Recirculation:** no clean discrete change identified among these six IDs during the A/C/recirc test.
- **Cruise MAIN:** no clean discrete change identified among these six IDs during the labeled button press.
- **Mist/pull-back:** not represented in `0x1F4 B0`.
- **Intermittent wiper delay:** not represented in `0x1F4 B0`.
- **Hazards:** no distinct `0x1F4 B0` state observed.

Honda documentation places many body/combination-switch functions on B-CAN, so absence from these six F-CAN messages should not be interpreted as absence from the vehicle network as a whole.

## 5. Counters and checksum

All six IDs contain an independent two-bit rolling counter:

```python
counter = (B7 >> 6) & 3
```

The original 809,393-frame dataset and all four new labeled logs contained **zero counter discontinuities**.

For `0x0D4`, `0x12C`, `0x188`, and `0x224`, the low nibble of B7 follows:

```python
expected = (
    -sum((b >> 4) + (b & 0x0F) for b in data[:7])
    - (data[7] >> 4)
) & 0x0F
```

The original pass was **576,806 / 576,806**, and every applicable frame in the new tests also passed. No such checksum is claimed for `0x0C8` or `0x1F4`; their low B7 nibble remained zero in the analyzed captures.

## 6. CarStats implementation recommendations

Use directly:

- RPM, coolant, IAT
- native speed and distance ticks
- brake pedal
- lighting state and parking brake
- A/C active/request
- current/target gear and full selector
- wiper/turn status with the documented limitations
- odometer kilometers
- raw/unwrapped fuel-use accumulator

Use with filtering/caveat:

- fuel level from `0x0D4 B3/B4`
- secondary speed
- MIL bit until a deliberate fault-on test is available
- oil-pressure/engine-off candidate and D-range flag as diagnostic/experimental signals

Do not invent semantics for unresolved bytes. Preserve raw data so later labeled tests can promote them without losing history.

## 7. Fuel economy status

CarStats now has both required CAN-side ingredients:

```text
distance: 0x0C8
fuel usage: 0x224 B2:B3
```

The remaining problem is **scale, not identity**. Until `fuel_volume_per_count` is calibrated, display fuel counts/rates rather than fake gallons or MPG. Calibration can be performed by a fill-drive-refill measurement, Honda-enhanced diagnostic data if an injector/fuel quantity reference is available, or a trusted factory-nav/HDS reference.

## 8. Source/provenance notes

See `SOURCES.md` and `test_evidence_v3.json` for hashes and evidence details. The raw four new labeled test logs are included in `raw_new_tests/`. The original reproducible [date withheld] decode package and the previous v2 handoff are preserved under `baseline_v1/` and `baseline_v2/`.

