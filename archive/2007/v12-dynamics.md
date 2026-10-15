# Sanitized historical source: 07-V12

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# 2007 Accord: transmission, cruise, throttle, accessory load and fuel use
## CarStats offline dynamics study, v1.2

This completes the six follow-on analyses using existing recordings. It does not install software, change the vehicle, introduce a new test drive, or identify an OEM torque-converter lockup command.

## Main findings

The most useful new result is the separation of demand-like and feedback throttle channels during high-load shifts. In three shifts, **0A6 B2 stays at 208 throughout**, while **B3 briefly falls from 208 to 68 or 71 and then returns to 208**. B4 remains high (188-192). This supports a shift-associated throttle intervention downstream of the B2 demand-like signal. It makes an unconditional final-actuator-command label for B2 unjustified; an upstream demand interpretation is better supported, but remains an inference.

The other results are measurable reported shift durations, cruise-button response timing, an empirical fifth-gear coupling reference, a repeatable accessory-load association at idle, and a relative fuel-counter allocation. Their qualifications are important: CAN state timing is not mechanical clutch timing, and a kinematic reference is not a directly decoded lockup flag.

## Sources and integrity

| Recording | Frames | Applicable checksum checks | Role |
|---|---:|---:|---|
| drive-a, [date withheld] 02:35 | 518,217 | 496,567 | Driving analyses and reference training |
| drive-b, [date withheld] 11:52 | 319,681 | 306,330 | Driving analyses and independent comparison |
| Original stationary checklist | 446,211 | 427,643 | Accessory-load association |
| MAX A/C | 44,023 | 42,184 | Constant-bit comparison, no qualifying edges |
| Body/dimmer raw.log | 158,096 | 151,492 | Constant-bit comparison, no qualifying edges |
| **Total** | **1,486,228** | **1,424,216** | |

All applicable payload checksums passed. All input lines parse, and recorded timestamps never move backward. The checksum convention excludes 1F4. Modulo-four sequence discontinuities are retained in the audit, including the standing capture's ignition cycles and the drive-b startup. These counters cannot exclude losses of multiples of four; this is not a certification of electrical bus health.

The main driving analyses use **837,898 frames**. Auxiliary stationary files contribute only to the accessory study, not the driving shift or fuel totals. SHA-256 identifiers and per-ID cadence/gap details are in `capture_audit.json`.

## Decoding and time alignment

Byte numbering is zero-based. RPM is 12C B4:B5 big-endian; coolant/IAT are B0/B1 minus 40. Brake is 12C B6&01, cruise is B6&08. 188 B0/B1 are reported current/requested gear, and B3=08 is selector D. Code 7 is an unsettled state, not seventh gear.

SpeedA is 0C8 B0:B1 divided by 100, in **nominal km/h**. The higher B4:B5 channel is retained separately. No new GPS calibration or tire-circumference measurement is supplied. MPH values in this report use SpeedA/1.609344 and retain its calibration uncertainty.

0A6 B2 is demand/request-like; B3 is the previously OBD-correlated throttle-feedback equivalent. B4 is a request-like channel, not an independently calibrated physical pedal sensor. DFCO is B0&02. The accessory candidate is 0D4 B2&40. 224 B2:B3 is the raw fuel accumulator; neither fuel volume nor MPG is inferred here.

Native event boundaries use integer microsecond timestamps. Companion values are the latest **preceding** packet and must be no older than 50 ms. No future sample is used to define an event's starting state. The separate 20 Hz grid is for sustained behavior, not sub-frame event latency. Reported edge precision is not physical actuator precision.

## 1. Shift timing and strategy

There are 98 forward requested-gear changes with selector D: 46 in drive-a and 52 in drive-b. Of these, 85 reach the requested reported gear, 12 are retargeted, and one is censored when the selector leaves D. Eleven of the completions begin with the prior reported gear unsettled, so they are excluded from the clean timing comparison.

The main table therefore contains **74 clean completions: 49 upshifts and 25 downshifts**. A clean start requires the preceding 100 ms to report the old current and target gear together. Completion is the first packet reporting current=target=new gear, sustained for at least 100 ms. The new state is allowed to be brief before the next shift, and its hold time is measured through the following boundary, rather than only to its last sample.

| Shift | Events | Median request-to-report time | Range |
|---|---:|---:|---:|
| 1 -> 2 | 10 | 1.055 s | 0.920-1.380 s |
| 2 -> 3 | 14 | 0.975 s | 0.850-1.080 s |
| 3 -> 4 | 12 | 1.005 s | 0.670-1.140 s |
| 4 -> 5 | 13 | 0.980 s | 0.800-1.030 s |
| 5 -> 4 | 11 | 0.700 s | 0.650-0.890 s |
| 4 -> 3 | 10 | 0.880 s | 0.710-0.990 s |
| 3 -> 2 | 4 | 0.860 s | 0.810-0.870 s |

These are **reported control-state windows**, including any lead-in or confirmation time. They do not measure clutch-to-clutch torque transfer, prove a transmission fault, or justify comparing directly with advertised mechanical shift times.

A distinct no-demand downshift pattern appears: six of seven clean 5->4 requests with B4=0 occur at **51.92-51.99 nominal km/h**, about 32.3 mph. The seventh occurs at 57.98 km/h during braking. Thus a repeatable speed-related pattern is visible, but one universal speed threshold is not established.

The two high-request 1->2 shifts are requested at 5,859 and 5,873 RPM, while the other eight are requested at 2,059-3,196 RPM. Engine RPM can continue rising after a request; the request RPM is not automatically the peak or the physical shift-completion RPM. Full event rows, status lines, request levels and speed/RPM values are in `shift_events.csv`.

## 2. Throttle coordination during shifts

Three especially discriminating shifts begin and end with feedback B3 at 208:

| Capture / shift | Request time | B2 during shift | B3 minimum | First B3 <=100 after request |
|---|---:|---:|---:|---:|
| drive-a, 1->2 | 398.370 s | Always 208 | 68 | 619 ms |
| drive-a, 2->3 | 407.729 s | Always 208 | 71 | 549 ms |
| drive-b, 1->2 | 473.504 s | Always 208 | 68 | 619 ms |

B3 stays below 100 for approximately 270 ms in both 1->2 examples and 190 ms in the 2->3 example. It then returns to 208. B4 remains high at 188-192 rather than falling to zero. Two separate 1->2 events reproduce almost the same delay and depth.

Using the v0.8 relative-throttle-equivalent fit, `0.098 + 0.44499*B3`, this is approximately **92.7% -> 30.4-31.7% -> 92.7%**. These percentages are ECU/OBD equivalents, not measured throttle-plate degrees. The underlying calibration was fitted on steady samples; no new high-speed independent physical throttle trace was recorded.

The repeated event supports throttle reduction associated with the shift, while the demand-like channel remains high. It is stronger evidence of ECU coordination than an event in which all throttle-related channels simply fall together. The exact internal torque-management algorithm, final actuator target, ignition intervention and driver pedal position remain unobserved.

**Map refinement:** keep B2 named `throttle_demand_or_upstream_request_candidate`, not `final_throttle_actuator_command`. B3 remains the OBD-correlated feedback channel. B4 is still not a separately calibrated pedal position.

Away from individual events, derivative correlation between B2 and subsequent B3 peaks at about 60 ms in drive-a and 50 ms in drive-b. Peak correlations are only 0.330 and 0.296. This is a broad response tendency, not a universal fixed lag, particularly in the shift interventions just described. See `throttle_response_lag.csv` and the native `high_load_shift_traces.csv`.

## 3. Torque-converter/driveline coupling estimate

Honda's published four-cylinder automatic gear ratios are 2.652, 1.517, 1.037, 0.738 and 0.566. The theoretical fourth-to-fifth speed-normalized RPM multiplier, with rigid coupling unchanged, is 0.566/0.738 = 0.76694. This is a kinematic reference, not a claim that every observed shift must show a 23.3% RPM drop.

A fifth-gear reference was trained **only on drive-a** using positive request, cruise active, speed >=50 nominal km/h, low speed change, and at least two seconds of separation from gear/target transitions. The dominant RPM/speed band is approximately:

`reference_rpm_in_fifth = 21.177 * speedA_kmh`

Equivalently, about **34.08 RPM per nominal mph**, or **2,045 RPM at nominal 60 mph**. There are 266.75 seconds in the selected core reference band. The central 90% ratio range is 21.133-21.218 RPM/(km/h).

The drive-b recording independently contains a similar dominant fifth-gear band near 21.18. It also contains long departures from that relationship, particularly during acceleration and lift-off. The exported +/-3% band classification is explicitly a heuristic description of proximity to the reference, **not a percentage of time with a confirmed locked torque converter**.

A clear counterexample to rigid fifth-gear coupling occurs at drive-a elapsed 580.818 s: reported current/target stay 5/5, SpeedA is 88.47 nominal km/h, and the latest preceding RPM is 1,201. The reference would predict 1,874 RPM. This supports substantial departure from the near-rigid relationship, consistent with converter release/overrun behavior. It does not isolate converter slip from every other internal driveline effect, and cannot be used as a fault diagnosis.

The study does not know turbine/input-shaft speed, actual lockup command, or tire circumference. References for gears other than fifth are derived from Honda's ratios and the same coefficient, not independently calibrated locked samples in every gear. Do not publish them as measured turbine RPM or actual slip RPM.

## 4. Cruise behavior

Six cruise sessions total **577.293 seconds**. Every engagement and disengagement has an identifiable nearby button or brake edge in these logs.

| Action | Observations | CAN status response |
|---|---:|---:|
| SET / RESUME engagement | 6 | 159-215 ms |
| CANCEL disengagement | 4 | 41-48 ms |
| Brake-triggered disengagement | 2 | 20.000 and 20.023 ms |

These are delays between recorded switch and cruise-status edges, not brake hydraulic response or injector timing.

A 144.5-second button-free drive-a window (429.25-573.75 s) has a median speed of **58.42 nominal mph**, with a range of **57.39-59.14 mph**. The drive-b recording has a 66.4-second button-free window around 49.16 mph, ranging 48.31-49.80 mph. These are observed speed envelopes, not errors relative to a decoded cruise setpoint, because a setpoint field has not been identified.

The windows exclude the first ten seconds after engagement, three seconds before disengagement, and a two-second-before/ten-second-after guard around SET/RESUME activity. They are selected using control events, not by searching for the smallest speed variance. Some remaining windows contain intentional acceleration or possible driver override; the complete table retains these less-steady cases rather than hiding them.

A 10.270-second held RESUME raises observed speed from 44.67 to 55.56 mph by release. A 6.410-second held SET reduces it from 54.80 to 48.82 mph. These are observed vehicle responses, not recovered increments of the internal setpoint.

DFCO overlaps engaged cruise for **27.415 seconds**: 22.486 in drive-a and 4.929 in drive-b. Native intersections, not rounded 20 Hz grid sums, supply those figures. It is already established that cruise engagement and fuel cut can coexist.

## 5. Accessory-load compensation

The status candidate `0D4 B2&40` has **43 qualifying transitions** with comparable P-idle, stationary, zero-B4 windows on each side. Four are from drive-a and 39 from the original stationary checklist. MAX A/C, the body-controls capture and the drive-b drive contribute no qualifying matched P-idle edge pairs under these rules.

Each comparison uses equal windows from 3.0 to 0.5 seconds before an edge and 0.5 to 3.0 seconds after it. The bit must hold its expected state in each window; selector must remain P; RPM must stay 500-1,500; speed must remain <1 nominal km/h; B4 must stay zero; and every companion sample must be fresh. Fuel intervals must be wholly inside the window, with at least 2.2 seconds of coverage. Rejected edges and reasons are retained.

Pooling the accepted windows, raw fuel-counter rate is **4.17 ticks/s with the bit set versus 2.98 ticks/s clear**, about **40% higher**. Feedback B3 is 2-4 raw counts higher with the bit set. RPM remains around 800: medians of window medians are 805.5 set and 807.0 clear.

In 37 of 43 pairs, the set-state fuel rate is higher by at least 0.05 raw ticks/s; the other six are effectively tied at this counter resolution. The two windows may reuse portions of the same cycle, and most come from one checklist session. These are not 43 independent experiments or a causal estimate of A/C fuel consumption.

The association supports an accessory/load-related status and idle compensation. It does **not identify compressor clutch engagement**, exclude fan or other load interactions, or prove the A/C is cooling. No label is upgraded to physically confirmed compressor status. B3 often falls below the v0.8 calibration's tested minimum of 8 here, so idle throttle differences remain in raw counts rather than extrapolated percentages.

## 6. Relative fuel-counter breakdown

The two drives contribute exactly **25,236 raw increments**: 15,236 drive-a and 10,000 drive-b. No reset or wrap occurs in either drive's analyzed fuel-counter sequence. The covered time between first and last fuel samples totals 1,399.768 seconds; it is shorter than full file duration because the drive-b file starts before its first 224 packet.

| Motion category | Raw increments | Share of increments | Share of covered time |
|---|---:|---:|---:|
| Accelerating | 12,304 | 48.76% | 20.59% |
| Approximately steady speed | 11,276 | 44.68% | 50.31% |
| Slowing | 1,106 | 4.38% | 18.24% |
| Stopped with engine running | 548 | 2.17% | 10.28% |
| Engine off/cranking interval | 2 | 0.008% | 0.586% |

Motion class uses a centered one-second SpeedA slope. Acceleration greater than +0.2 m/s^2 is accelerating; less than -0.2 is slowing; intermediate moving values are approximately steady. Stopped is speed <1 nominal km/h, with engine running defined here as >=400 RPM. This is an accounting convention, not an OEM driving-mode signal.

Changing the acceleration threshold from 0.1 to 0.3 m/s^2 moves the accelerating share from **53.86% to 46.96%**. Therefore the robust interpretation is **roughly half the recorded fuel-counter increments occur while gaining speed**, not that 48.76% is a uniquely defined physical truth. The counter's quantization/reporting delay also blurs category boundaries. Sensitivity tables and every assigned interval are included.

These are relative counter shares. A constant conversion factor would preserve the proportions, but absolute fuel volume, MPG, money saved and causal fuel savings from cruise/DFCO are not calculated. A slowing vehicle can still consume fuel whenever the DFCO bit is not active. No counterfactual 'fuel saved' estimate is made.

## What CarStats can use from this pass

The data support reported shift-duration history, demand-versus-feedback throttle overlays, timed cruise-status/button events, raw accessory load association, a clearly labeled inferred coupling indicator, and relative counter allocation. None requires replacing the known DFCO bit with guessed rules.

Keep actual lockup command, actual converter slip, final actuator command, physical compressor engagement and fuel volume separate from these derived metrics. This study found new **behavior**, not a new confirmed CAN bit for each underlying actuator.

## Reproduction and files

Core scripts require Python 3 with NumPy and pandas. `verify.py` uses only the standard library and reparses the original files without loading analyzer caches.

Place the five raw files under an input root using the relative paths in `analyze.py:SOURCES`. Then:

```bash
python analyze.py --root /path/to/input-root --out /path/to/analysis
python studies.py --work /path/to/analysis
python complete_summary.py --work /path/to/analysis
python verify.py --root /path/to/input-root --work /path/to/analysis
python -m unittest test_analysis -v
```

Run the commands from the directory containing these scripts, or add it to PYTHONPATH. The input root path and output directory are adjustable; the raw logs are never edited. Generated caches are not bundled but are recreated by the first command.

`verification.json` records raw-stream checksum/count validation, 74 clean shift boundaries, 12 cruise response edges, three high-load throttle dips, 43 matched idle-window pairs and the 25,236-increment fuel sum. Unit tests cover integer time parsing, freshness, counter resets versus wraps, retargeted shifts, selector changes and brief-but-completed shifts. Verification does not independently prove physical signal meanings.

Data tables include all 98 request episodes, shift group summaries, cruise intervals/buttons/responses, button-free windows, fuel intervals and threshold sensitivity, accepted/rejected accessory edges, coupling summaries, a 20 Hz driving grid, and the three native high-load shift traces. Original raw logs are not duplicated.

External reference: Honda Newsroom, *2007 Honda Accord Sedan Specifications*, [date withheld], four-cylinder automatic ratio column. https://hondanews.com/en-US/releases/release-44c7378894c75d8ecc4920004c34bfbe-2007-honda-accord-sedan-specifications

The proprietary signal definitions come from this project's prior 2007 observations and paired OBD calibration, not from the public Honda specification table.

