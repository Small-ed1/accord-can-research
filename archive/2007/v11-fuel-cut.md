# Sanitized historical source: 07-V11

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# 2007 Accord: DFCO entry, resumption and timing, v1.1

Offline analysis of the original [date withheld] drive-a and drive-b recordings. No vehicle settings, services, firmware or installed CarStats software were changed.

## Result

The strongest newly resolved behavior is an approximately **1,200 RPM fuel-resumption boundary** when the request-like byte remains zero. There are ten such exits, identified from the request channel without first selecting an RPM threshold. All ten bracket 1,200 RPM at the adjacent PCM frames.

Other exits divide into seven with positive request and cruise engaged, and four where request becomes positive 20-140 ms after the flag clears. Those four are plausibly demand-related, but these recordings do not establish their exact causal trigger.

## Input and verification

| Recording | Raw frames | Applicable checksums passing | DFCO events | Active seconds | Fuel samples while flag set |
|---|---:|---:|---:|---:|---:|
| drive-a | 518,217 | 496,567 | 13 | 55.910491 | 558 |
| drive-b | 319,681 | 306,330 | 8 | 13.707965 | 136 |
| Total | 837,898 | 802,897 | 21 | 69.618456 | 694 |

All 694 fuel-counter differences assigned to an active flag are zero. Of those, 673 differences have both bounding fuel samples strictly within the same active interval. The 70-ms event has no wholly enclosed fuel interval, so it is weak counter evidence on its own. Repeated zero differences are samples, not 694 independent experiments.

Every applicable checksum passes. No malformed lines or backward timestamps occur. The drive-a log has no observed modulo-four discontinuities; the drive-b log has one in 0x20C around startup. The primary event channels 0x0A6, 0x12C, 0x0C8, 0x188 and 0x224 have no observed discontinuities in either log. Multiples-of-four losses cannot be excluded by a modulo-four counter alone.

## Timing and decoding method

DFCO = bool(0x0A6 B0 & 0x02), with B0 the first byte. Each edge is the first original 0x0A6 frame containing the changed flag. Its physical/internal transition is bounded by the preceding 0x0A6 frame and that frame, approximately 10 ms apart. Companion fields are the latest preceding valid message, with freshness enforced. The immediately following 0x12C RPM is exported separately.

RPM = big-endian 0x12C B4:B5. Brake = B6 & 0x01; cruise engaged = B6 & 0x08. 0x188 B0/B1 are current/target gear; code 7 is an unsettled transition, not seventh gear. The selector is B3, with 0x08 identifying D.

SpeedA = big-endian 0x0C8 B0:B1 / 100, in nominal km/h. SpeedB = B4:B5 / 100 is also preserved. These channels differ by about 2%; neither is independently GPS-calibrated by this analysis. No fuel volume or MPG is calculated.

0x0A6 B2 is request/target-like, B3 is calibrated feedback/actual-throttle-equivalent, and B4 is a request-like transformed channel. **B4 is not an independently measured accelerator pedal percentage.** Small B3 values in this analysis extend below the previous calibration's tested lower bound of 8, so throttle is retained in raw units here.

## 1. Entry conditions and delay

All 21 entries have B4 = 0. The immediately preceding RPM ranges from 1,557 to 3,531 (median 1,938); the first following RPM ranges from 1,538 to 3,506. SpeedA at entry ranges from 56.70 to 120.37 nominal km/h. These are observed operating points, not minimum or maximum eligibility thresholds.

B4 has been continuously zero for 0.339984 to 1.699489 seconds at activation, median 0.919766 seconds. This is a delay relative to an observed request-channel transition, not a measured foot release or a proven fixed ECU timer. The variability means a universal one-second rule is not established.

The service brake is applied at four entries and released at seventeen. Five entries occur with cruise already engaged. Thus brake application is not required, and 'the driver released the accelerator' is more specific than the available signals justify.

B2 at entry is 7 in eighteen events, 8 in two, and 13 in one. B3 ranges from 6 to 16 at entry and reaches 20 while the flag is active. There is no demonstrated universal zero-throttle-angle trigger.

All entries occur with selector D and coolant 84-91 C; coolant across the active intervals ranges from 83 to 91 C. There is no independently measured cold-engine cutoff threshold, lower-gear rule, reverse/neutral rule or lowest road-speed eligibility threshold.

## 2. Automatic resumption near 1,200 RPM

Ten exits are selected solely because B4 is zero at the edge and stays zero for at least one full second afterward. In those ten cases, the last preceding RPM is 1,201-1,233, and the first following RPM is 1,189-1,200. The first <=1,200 RPM sample arrives 0.371-0.546 ms after the flag clears, consistent with adjacent messages from the same update cycle.

Examples: drive-a event 4 brackets 1,202 -> 1,192; drive-a event 8 brackets 1,201 -> 1,199; drive-b event 5 brackets 1,219 -> 1,197. Every pair straddles approximately 1,200 RPM. The numerical overlap does not establish a one-RPM-accurate physical threshold.

The warm-engine 1,200 RPM rule appears in six drive-a events and independently in four drive-b events. Their road speeds span 56.88-90.90 nominal km/h, and three have no brake applied. Fuel can resume at substantial road speed because engine RPM, road speed and the current gear code do not remain in a fixed ratio throughout these events. An exact torque-converter lock state is not available, so converter unlocking is an interpretation, not a decoded signal.

## 3. Request-related exits

Seven exits have B4 > 0 and cruise engaged at the clearing edge. Their RPM values are 1,667-2,228 using the last preceding PCM sample. In these cases the first positive B4 occurs 20-1,290 ms before the flag clears. Small positive request therefore can coexist with fuel cut, especially during cruise regulation.

The remaining four exits have B4 = 0 at the clearing edge, followed by positive B4 after 20, 50, 100 or 140 ms. Their edge RPMs are approximately 1,339, 1,554, 1,802 and 1,922. B2 begins rising before or close to these exits, except that one small rise follows the edge. A demand-change interpretation fits, but it cannot distinguish physical pedal movement, idle/torque control or another internal enabling condition. These four are explicitly not claimed as causal proof.

## 4. Hysteresis and gear changes

An approximately 1,200 RPM hold/resumption floor is well supported for the zero-request exits. The entry side is conditional and delayed; simply subtracting 1,200 from an entry RPM does not recover an OEM hysteresis width. Do not implement an inferred universal 1,600-on/1,200-off control map.

The flag remains asserted through a complete 4th-to-5th change in drive-a event 12. The current/target state is 4/4, then 7/5 at +0.041 s, then 5/5 at +0.841 s. Fuel cut lasts 1.409732 s in total and ends near the RPM floor, after the shift completes. Two other entries occur while current gear is already code 7 with target 4. **A gear change does not unconditionally cancel fuel cut.**

No separate lockup flag, injector electrical trace or engine output torque is present. The analysis does not claim to recover transmission clutch commands or the complete OEM decision map.

## 5. Flag versus fuel-accounting timing

The last positive counter difference precedes entry by 8.769-448.788 ms (median 148.765 ms). The first positive difference after exit arrives 31.134-431.020 ms later (median 241.076 ms). The counter is sampled at about 100 ms intervals and its increments are quantized. These are reported fuel-accounting delays, not injector shutoff or reopening latency.

Use the 100 Hz status bit for a responsive fuel-cut indication. Do not wait for the 10 Hz accumulator to restart, and do not infer fuel cut solely from a single zero counter difference.

## Exact-edge correction to earlier replies

The earlier quick summary's 1,594-3,809 entry RPM range and three brake-on entries are not reproduced at the actual first changed frame. This pass explicitly uses last-preceding references and retains the first following RPM for the timing bracket. It yields 1,557-3,531 before the edge and four brake-on entries. The earlier 21-event count, 69.62-second total and 694 zero fuel samples remain valid. All edge snapshots in this package supersede the old fuelcut_edges.csv estimates.

## CarStats handling

Decode the observed bit directly, preserve freshness/unavailable state, and label its demonstrated operating behavior as deceleration fuel cut. The approximately 1,200 RPM result belongs in the behavior documentation; it should not replace the actual bit with guessed logic. Brake, request, cruise and gear are explanatory overlays, not substitute decoders. Behavior during rev limiting or other non-deceleration fuel suppression was not established.

## Every event

RPM pairs below are last preceding / first following the OFF edge. Request groups: Z = B4 zero through the following second; C = positive B4 with cruise at exit; N = positive B4 shortly after exit, causality unresolved.

| Capture/event | Start (s) | Duration (s) | OFF RPM bracket | Group | Current/target sequence |
|---|---:|---:|---:|:---:|---|
| drive-a 1 | 189.106 | 2.680 | 1980 / 1980 | C | 5/5 |
| drive-a 2 | 269.682 | 1.820 | 1988 / 1986 | C | 5/5 |
| drive-a 3 | 276.191 | 2.120 | 1977 / 1976 | C | 5/5 |
| drive-a 4 | 301.356 | 9.478 | 1202 / 1192 | Z | 5/5 |
| drive-a 5 | 370.095 | 2.210 | 1206 / 1196 | Z | 5/5 |
| drive-a 6 | 416.737 | 7.399 | 2228 / 2228 | C | 7/4 > 4/4 |
| drive-a 7 | 476.176 | 10.968 | 1955 / 1952 | C | 5/5 |
| drive-a 8 | 577.759 | 3.059 | 1201 / 1199 | Z | 5/5 |
| drive-a 9 | 687.930 | 2.050 | 1802 / 1799 | N | 5/5 |
| drive-a 10 | 723.303 | 3.309 | 1339 / 1340 | N | 5/5 |
| drive-a 11 | 747.229 | 8.828 | 1203 / 1194 | Z | 5/5 |
| drive-a 12 | 773.265 | 1.410 | 1211 / 1200 | Z | 4/4 > 7/5 > 5/5 |
| drive-a 13 | 810.948 | 0.580 | 1209 / 1197 | Z | 7/4 > 4/4 |
| drive-b 1 | 180.258 | 4.849 | 1667 / 1664 | C | 5/5 |
| drive-b 2 | 296.190 | 0.070 | 1554 / 1527 | N | 5/5 |
| drive-b 3 | 302.259 | 0.340 | 1922 / 1919 | N | 5/5 |
| drive-b 4 | 309.218 | 0.460 | 1954 / 1954 | C | 5/5 |
| drive-b 5 | 350.432 | 3.600 | 1219 / 1197 | Z | 5/5 |
| drive-b 6 | 420.861 | 0.460 | 1220 / 1198 | Z | 5/5 |
| drive-b 7 | 454.716 | 3.709 | 1201 / 1191 | Z | 4/4 |
| drive-b 8 | 511.927 | 0.220 | 1233 / 1189 | Z | 4/4 |

## Files and reproduction

`events.csv` contains complete per-event snapshots, exact source line references, companion ages, request timing and fuel-counter timing. `event_summary.csv` is a compact subset. `edge_samples.csv` preserves 0A6-centered native snapshots within 100 ms of every entry and exit. `fuel_counter_edges.csv` contains all relevant 224 samples, raw differences and phase labels. `gear_changes.csv` contains gear transitions within 0.5 seconds of each event and through its duration. `summary.json` includes hashes, per-ID integrity/cadence statistics and summary values.

`analyze.py` uses standard-library integer-microsecond timestamps. `verify.py` independently streams the original logs without reusing the analyzer's as-of helper and verifies all 42 edges, their RPM references, request grouping and the fuel-counter result. `verification.json` records the successful check.

Run with the original raw logs:

```bash
python3 analyze.py --drive-a /path/to/drive-a.log \
  --drive-b /path/to/drive-b.log --out ./recomputed
python3 verify.py --drive-a /path/to/drive-a.log \
  --drive-b /path/to/drive-b.log --out ./recomputed
```

The raw logs are not duplicated in this archive. Retain the originals. `event_summary.csv` is a convenience subset of `events.csv`; README is the interpretive report. No new driving test is required to reproduce these results.

