# Sanitized historical source: 07-V02

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# 2007 Accord: stationary CAN test analysis

Source: `standing-a.log`  
Recorded local time: [date withheld] to [date withheld]  
Duration: **773.899396 seconds (12 minutes 53.899 seconds)**  
Valid frames: **446,211**, ten IDs, no malformed lines.  
Revision: stationary-0.2. This is an offline analysis and proposed signal-map update, not installed CarStats software.

## Basis and limits

This analysis processes every frame in the attached stationary-test log. It uses the earlier drive report as a list of hypotheses, not as independent proof. The user said this was the standing test and planned to pull the handbrake between tests. No separate list of actual actions with timestamps, dashboard video, OBD reference readings or ignition-key positions accompanies the file.

“Observed” below means a pattern measured in the trace. “High-confidence inference” or “strong candidate” describes a proposed physical meaning. Repeating a value or passing a checksum alone cannot identify the physical control.

Byte numbering is zero-based. Multi-byte counters and RPM use big-endian ordering.

## Main results

1. The handbrake-marker interpretation is strongly supported by `0x0D4 B0 & 0x04`, mirrored by `0x405 B2 & 0x20`.
2. Lighting appears to be a two-bit enum in `0x0D4 B0 & 0x03`, with probable off/parking/low/high meanings.
3. Stationary cruise-button codes are clearly present. `0x0D4 B0 & 0x20` is a new cruise-MAIN candidate.
4. Reverse can settle to `0x188 B0 = 6`. The prior drive's persistent value 7 must not be treated as the only reverse representation.
5. `0x188 B2 & 0x80` is asserted in Park during startup, so it cannot unconditionally mean selector=D.
6. The fuel accumulator resets to zero after reinitialization. Counting these drops as wraparound would create false fuel consumption.
7. `0x20C` continues transmitting during periods when the other streams disappear. Any-CAN-traffic is not a reliable ignition-on test for this trace.
8. The accessory/A/C candidate stays asserted during zero-RPM intervals, so it cannot prove mechanical compressor operation.

## 1. Stationary capture and integrity

The fine-distance byte `0x0C8 B6` stays zero throughout, and the coarse odometer bytes `0x1F4 B3:B5` stay at `08 DE C2` ([absolute reading withheld] raw). There is no accumulated distance.

Both speed channels contain a single 38-frame blip lasting about 0.380s at 551.151–551.531s, around the selector's P-to-R transition. The larger channel reaches 2.08 nominal km/h. This is not a driven calibration segment and does not establish actual movement; a small disturbance or reporting transient cannot be distinguished from this data alone.

RPM ranges from 0 to 1,592. Prior temperature formulas give coolant 83–87°C and intake 39–50°C; these are decoded readings, not new independent sensor calibrations.

| ID | Frames | Median-derived Hz while active | Maximum inter-frame gap, s | Counter discontinuities |
|---|---:|---:|---:|---:|
| `0x0A6` | 74,296 | 100.01 | 27.973709 | 3 |
| `0x0C8` | 74,296 | 100.01 | 27.973679 | 3 |
| `0x0D4` | 74,443 | 100.02 | 27.690228 | 9 |
| `0x12C` | 74,296 | 100.02 | 27.973663 | 3 |
| `0x188` | 74,296 | 100.02 | 27.973683 | 3 |
| `0x1F4` | 18,568 | 25.00 | 28.037867 | 3 |
| `0x20C` | 38,683 | 50.00 | 0.107504 | 2 |
| `0x224` | 7,428 | 10.00 | 28.153508 | 3 |
| `0x2E4` | 7,428 | 10.00 | 28.058187 | 3 |
| `0x405` | 2,477 | 3.33 | 28.157944 | 1 |

All **427,643** frames in the nine checksummed streams satisfy the previously established payload checksum:
```
checksum = (-sum((b >> 4) + (b & 15) for b in B0..B6)
            - (B7 >> 4)) & 15
```
`0x1F4` is excluded from that checksum rule; its B7 remains a four-state counter with zero lower six bits.

There are 33 observed counter discontinuities, all clustered around three reinitialization episodes. The first episode also contains a short burst of repeated-counter messages. Do not describe this file as having no counter skips, and do not convert those events into an exact dropped-frame count. Restarts can reset counters. Outside these episodes no additional counter discontinuities were found. Passing payload checksums is not proof of physical bus health or complete error-frame coverage.

Source references: first frames at lines 1–15; final frames at 446,197–446,211; nonzero speed near 329,771; reinitializations near 351,667,412,764 and 422,915.

## 2. Handbrake markers

Proposed decoding:
```
parking_brake = bool(payload_0D4[0] & 0x04)
parking_brake_mirror = bool(payload_405[2] & 0x20)
```

The two bits agree in all **2,477/2,477** comparisons using the most recent preceding 0D4 frame. Five asserted intervals are observed:

| Marker | Applied, elapsed | Released, elapsed | Held, s | Original log lines |
|---|---|---|---:|---|
| 1 | 01:31.222 | 01:34.072 | 2.850 | 54,582–56,281 |
| 2 | 01:35.382 | 02:27.062 | 51.680 | 57,072–87,986 |
| 3 | 02:30.482 | 02:34.133 | 3.651 | 90,040–92,217 |
| 4 | 08:30.350 | 08:33.071 | 2.720 | [absolute reading withheld]–306,981 |
| 5 | 11:03.334 | 11:06.524 | 3.190 | 395,978–397,882 |

The first transition changes 0D4 B0 from 20 to 24, and 405 B2 from 04 to 24. The service-brake bit changes separately, supporting distinct handbrake and foot-brake signals. See source lines 54,575–54,610.

The second application is held for 51.680s. These are therefore not uniform three-second pulses or a boundary after every individual action. They support broad test grouping, but do not automatically supply labels for every control tested.

Confidence: **high-confidence inference**, combining the repeated pattern, dual-message agreement and the user's stated marker method. It is a switch/status interpretation, not a measurement of parking-brake holding force.

## 3. Lighting and existing body controls

Strong lighting-stalk candidate:
```
light_mode = payload_0D4[0] & 0x03
```

| Code | Proposed meaning | Observed supporting sequence |
|---|---|---|
| 0 | Off | Initial state and after 32.179s |
| 1 | Parking lights |17.316–22.607s |
| 2 | Low beam |22.607–27.598s |
| 3 | High beam / flash |27.598–31.610s; three short pulses around 36.690–38.021s |

These physical labels follow the apparent test sequence; raw enum values are certain, but exact control labels were not recorded independently. This must be decoded as an enum rather than independent low-beam and high-beam switches.

`0x405 B3 & 0x08` is set when `0x1F4 B1=77` and clear whenB1=100, in all 2,477 aligned samples. It remains active through the parking/low/high-like sequence. Name it an illumination-active candidate rather than narrowly “headlights on.” Only 77 and 100 are observed, so this pass does not validate dimmer scaling across its full range.

Existing left/right request masks in 1F4 remain 20/40. Three brief left-request pulses are followed by a longer left segment around 40.532–49.934s and right around 49.973–58.416s. Wiper mode follows off/INT/low/high-style values later at 162.435–196.881s. The observed raw mask does not establish actual lamp-flash phase.

Source references: parking-light-like transition 10,363; low 13,528; high 16,514; flash 21,958; wiper-mode sweep 97,190 onward.

## 4. Cruise controls

The proposed four-state field `0x0D4 B0 & 0xC0` appears while stationary, with two presses of each nonzero code:

| Code | Proposed control | Asserted elapsed intervals |
|---|---|---|
|40|SET/DECEL|636.311–637.801s;640.812–643.632s|
|80|RESUME/ACCEL|645.612–645.842s;649.873–653.933s|
|C0|CANCEL|654.343–654.503s;658.343–662.454s|

Names remain strong candidates based on the prior driving behavior and this grouped test. All three codes exist independently of cruise engagement: `0x12C B6 & 0x08` never sets in this recording.

New candidate: `0x0D4 B0 & 0x20` for cruise MAIN/master enabled. It clears 626.130–631.521s while the engine remains running, then the button tests follow. This supports an independent master switch rather than an engine-running bit. It also clears at shutdown-like transitions, so one transition alone would have been ambiguous.

Source references: MAIN-like transition 373,709–373,722; button events 379,812,387,926 and 392,992. Verify the physical names against the actual button order before publishing a definitive DBC.

## 5. Transmission corrections

A complete stationary selector sweep appears:
```
P -> R -> N -> D -> D3 -> 2 -> 1 -> P
```
The existing B3 enum is supported:01=P,02=R,04=N,08=D,20=D3,40=2,80=1. Brief 00 values occur between positions.

At 551.221s the pairB0/B1 is 07/06. At 552.611s, after 1.390s, it becomes **06/06** and remains there for 3.930s while selectorB3=02. ThusB0=6 is a settled-reverse status in this capture. B0=7 remains a transition/unsettled status and can also appear at initialization; the earlier drive's reverse interval never settling to 6 does not invalidate the new observation.

`0x188 B2 & 0x80` is set inD, but also for approximately 2.000s after each of three reinitializations while B3 saysPark. It may serve an indicator/bulb-check role, but that name is not proven. **Use B3 for selector; do not use this bit as unconditional D confirmation.**

Source references:329,815 initialR;330,638–330,655 transition to 06/06;351,685,412,776,422,927 for startup-in-P assertions.

## 6. Throttle and accessory behavior

During the zero-RPM sweep,0A6 B2/B3 reach 208 whileB4 reaches 199. For the selected 594–615s window, B3's change pattern best followsB2 with approximately 50ms delay (five 100Hz sample steps; correlation about 0.966). B2 minusB4 is 9 or 10 throughout that selected window.

This strengthens a demand/feedback/relative-channel interpretation. It does not establish accelerator-pedal percentage, throttle angle, or a physical scaling factor. At rest with engine off, B3 can sit 19 while B2 is 9, which is another reason not to treat them as simply interchangeable sensor copies. Independent pedal/commanded-throttle/actual-throttle readings are still needed.

The periodic accessory candidate `0x0D4 B2 & 0x40` remains set with RPM=0, including 599.419–619.150s. Source lines 358,079–358,090 showB2=C0, zeroRPM and zero fuel accumulator together. Therefore it cannot be interpreted as confirmation of a mechanically turning compressor. An A/C request, fan request or other accessory command remains plausible.

In the running 200–510s segment, the observed raw fuel rate averages about 3.962ticks/s with this bit asserted versus 2.908ticks/s clear. That is an association, not identification of the load. No timed A/C-control labels exist in the file, so the physical accessory cannot be settled from this pass alone.

## 7. Counter resets and shutdown-like traffic

The 0x224 counter has two negative transitions:
- 5,208 ->0 at 589.395s, after a reinitialization gap.
- 320 ->0 at 692.522s, after a second reinitialization gap.

These are resets, not normal 16-bit rollovers. The third reinitialization occurs while the counter is already zero. There are 1,290 observed positive deltas, all+2, summing 2,580raw ticks across the available intervals. This is not a calibrated fuel volume and cannot recover unobserved increments at shutdown boundaries.

For CarStats integration, establish a new baseline after each reset or loss of continuity. Preserve accumulated historical totals separately. Never blindly use `(new-old)&65535` across these boundaries.

The engine has clear zero-RPM periods in the persistent 20C stream at 587.898–619.352s and 691.554–749.512s. These windows include reinitializations and message absences; exact key positions remain unlabelled.

Across the 26-second window 708–734s, **1,300 frames of 0x20C and no frames from the other nine IDs** were received. `20C B0=00` during this window; B0=02 resumes with broader traffic and can coexist with zeroRPM. The 20C counter continues cycling.

Consequences:
- Any CAN traffic is insufficient to establish ignition ON.
- 0x20C B0 bit 1 is a promising separate operating/ignition-state candidate.
- ZeroRPM alone must not mean ignition OFF.
- Absence of one message must be represented as stale/unavailable rather than zero.
- This capture does not independently distinguishACC fromOFF, show long-term sleep, or establish safe Pi shutdown timing.

Source references: fuel before-reset lines 351,492 and 412,644; after-reset 351,739 and 412,830. Long 20C-only section starts after 421,524 and continues until 422,914.

## 8. Isolated unresolved body flags

Two reproducible patterns deserve physical labels:

| Field | Raw behavior | Remaining requirement |
|---|---|---|
|405 B2 &04|Clears 101.764–106.265s and 111.666–116.767s while handbrake flag remains asserted|Identify exactly which buckle/door/control was being changed and polarity|
|405 B4 &20|Three pulses 122.168–123.668s,125.168–126.969s,128.469–130.269s|Identify the physical control; do not guess a specific door, trunk or seatbelt|

These flags are independent of the handbrake mirror. The actual action order could label them without a road test. If the order cannot be reconstructed, only these controls need a short individually labeled stationary repeat.

## 9. New startup/status bits, not yet named

The following fields change during the three reinitialization/engine-off sequences:

| Field | Observed behavior | Safe interpretation now |
|---|---|---|
|0D4 B2 &80|Set in engine-off-like phases, clears near crank/start|Engine-off-related status candidate|
|12C B6 &10;405 B0 &01|First long engine-off phase clears afterabout 20s, before start|Startup/warning candidates, not generic engine-stopped flags|
|1F4 B0 &02|About 2.15s after each reinitialization|Startup timer/bulb-check candidate|
|405 B1 &01|About 2.4s after each reinitialization|Startup timer/bulb-check candidate|
|224 B6 &02|Set during engine-off-like phases; clears after rotation begins|Engine-status candidate|
|405 B2 &80;405 B3 &01|Set with engine-off-like state and clear after start|Warning/status candidates|
|2E4 B0|FF for the first five frames of the third reinitialization, then 00|Startup raw value; no longer classifyID asalways-empty|

Do not assign oil-pressure, battery, MIL, immobilizer or warning-lamp names from timing alone. A synchronized dashboard/key-state recording can test those interpretations.

## 10. Recommended next steps

First, label the already isolated body-control and cruise/lighting sequences from the actual test order. The handbrake marker times and native intervals are included.

Second, pair the existing engine-off sweep with independently supported pedal and throttle readings, or repeat only that short segment with those readings. Keep raw units until matched.

Third, annotate actualOFF/ACC/ON/start states and dashboard lights in a stationary capture that runs long enough to observe whether 20C eventually sleeps. This is the remaining evidence needed for reliable power management.

Distance, fuel-volume calibration and driving fuel-cut validation remain separate tasks. This standing capture should not be used to replace those calibrations.

## Package contents

- `capture_summary.json`: whole-file metrics, per-ID timing, checksum results, discontinuities, resets and caveats.
- `signal_updates.json`: proposed decodes, confidence levels and explicit limitations.
- `native_signal_intervals.json`: source-line-indexed state intervals; gaps are censored rather than filled.
- `handbrake_marker_intervals.json`: five marker intervals.
- `byte_inventory.json`: all bytes, values, counts and changing-bit masks.
- `README.md`: this report.

SHA-256 of the raw source:
`[original source hash withheld]`

The original log and earlier package are unchanged. No vehicle messages were transmitted, no CarStats decoder was installed, and no physical-control identity is claimed solely from checksum validity.

