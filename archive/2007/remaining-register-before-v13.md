# Sanitized historical source: 07-REGISTER

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# 2007 Accord CarStats: complete remaining-signal register
As of [date withheld] (based on all currently recovered analyses and logged captures)

## Scope and important revisions

This is an *offline* evidence register, not a new CarStats release or manufacturer DBC. All byte indices are zero-based B0..B7. F-CAN is 500 kbit/s Classical CAN. The available recordings contain ten 11-bit IDs: 0A6,0C8,0D4,12C,188,1F4,20C,224,2E4,405.

The v0.5 residual audit covered six original logs (1,364,106 frames; 1,307,199 applicable checksum passes), and found 52 then-unassigned varying bit positions across 16 byte slots plus 376 constant bit positions. **That 52-bit figure is historical**: warning lamps, oil life, the D lamp, and several other fields have since been identified. There are nowhere near 52 independently established unsolved physical sensors. Keep the historical masks for reference, not as a current definitive mystery count.

The v1.2 dynamics pass processed five source recordings (1,486,228 frames, 1,424,216 applicable checksum passes); many of those source frames overlap v0.5. Do NOT sum these totals as though they are independent frames.

### Recently settled, and therefore NOT outstanding

- 20C B1 = Maintenance Minder oil life, user dashboard-confirmed; don't count as unknown.
- 12C B6&10 = MIL; 1F4 B0&02 = ABS startup warning; 224 B6&02 = battery/charging lamp; 0D4 B2&80 = oil-pressure lamp, with 405 mirrors; 188 B2&80 = green D lamp including bulb check.
- 405 B5&02 = trunk open, 405 B2&04 = driver belt unbuckled (observed polarity).
- 0A6 B3 = measured throttle-feedback equivalent. From calibrated OBD PID45: relative throttle % ≈0.0980247+0.4449886×B3; PID11 absolute throttle % ≈11.541592+0.3221345×B3 (tested B3 8..208, ~0.131pp steady RMSE). None of these formulas establishes physical pedal percentage.
- 0A6 B0&02 = high-confidence DFCO; 21 events and 694 interior 224 samples, all zero increments while cut asserted; 10 zero-request exits clustered around 1,200 RPM warm. No complete cold-condition entry threshold.
- Odometer 1F4 B3:B5 = BE24/1.61 miles; live raw581670=>[absolute reading withheld] miles matched user's factory readout. 0C8 B6 traveled 164 ticks between complete odometer-mile updates in 14 intervals across two drives; **distance/tick = 1609.344/164=9.8130731707m**. This is odometer-relative; GPS validation remains separate.
- User believes 2007 fuel consumption uses 2003 scale: provisional 0.21117mL per normalized (raw>>1) 224 count (~0.105585mL per original raw count). A 2007 full-to-full metered check is still outstanding.

## The outstanding fields (summary)

| ID | CAN/bit(s) | Category | Identity/scale left to determine |
|---|---|---|---|
| R01 | 0x224 B1 | unidentified | unknown |
| R02 | 0x0D4 B2 bit 6 | partially_identified | high load association; physical action not confirmed |
| R03 | 0x0D4 B3 and B4 | calibration | very strong related sender-like pair; physical units uncalibrated |
| R04 | 0x224 B2:B3 | provisional_calibration | fuel accumulator identified; 2007 volume scale provisional |
| R05 | 0x0A6 B2 | semantic | demand/request-like candidate, not final actuator command |
| R06 | 0x0A6 B4 | semantic | transformed B2 demand-like field |
| R07 | 0x0C8 B0:B1 and B4:B5 | partially_identified | both speed related, exact factory roles not proven |
| R08 | 0x0D4 B5:B6 | partially_identified | delayed speed alias; role incomplete |
| R09 | 0x1F4 B1 bit7 | semantic | strong max-detent candidate, not fully confirmed |
| R10 | 0x2E4 B0 | unidentified | repeatable initialization pattern; originating module unknown |
| R11 | 0x20C B0 bit1 | behavioral | strong ignition-ON association; power state incomplete |
| R12 | 0x12C B6 bit3 cruise engaged + 0D4 B0 buttons | behavioral | button/state decoded, numeric cruise setpoint missing |
| R13 | 0x188 + 0x0C8 + 0x12C reported gears and speeds | behavioral | reported shift behavior decoded; physical converter input missing |
| R14 | 0x1F4 B2 | unexcited | observed zero in all first six 2007 recordings |
| R15 | multiple other constant/reserved payload bits | unexcited | unexcited only |

## Detailed per-signal evidence

### R01 · 0x224 B1

- **Current status:** unidentified; unknown.
- **Broadcast cadence:** 10 Hz; raw mask 0xFF.
- **Observed values:** F3 (243), F4 (244), F5 (245); low frequency +/-1 changes, F6 appears only in old 2003 studies
- **Direct evidence:** drive-a: F3->F4->F3->F4 (3 transitions/8,662 frames); drive-b: F5->F4 (1/5,340); [date withheld] first continuous: F3->F4 after 276.642 s (4,735 frames); [date withheld] second: F4 constant (7,378 frames). Body log F3 constant (2,643 frames).
- **Limitations/rejected interpretations:** Not a direct LTFT copy, MAP, ECT, fuel level, or monotonic fuel counter. BARO interpretation not supported.
- **Lowest-effort resolution:** Keep raw. Look for a Honda-specific engine diagnostic reference or a different independently labeled measurement, without repeating already-completed drives.

### R02 · 0x0D4 B2 bit 6

- **Current status:** partially_identified; high load association; physical action not confirmed.
- **Broadcast cadence:** 100 Hz; raw mask 0x40.
- **Observed values:** Binary 0/1. Strong candidate accessory/compressor permission or cyclical load state.
- **Direct evidence:** drive-b 9 clear intervals of 5.84–6.59s, average 6.221s; MAX A/C captures bit continuously set for 73.564s. 43 matched parked-idle edge comparisons: fuel-counter rate set 4.167 raw ticks/s vs clear 2.985 ticks/s (+39.6%); B3 feedback median +3 raw units, RPM around 800.
- **Limitations/rejected interpretations:** Not proven compressor clutch engaged. A/C switch tests did not uniquely toggle this bit. Could include electrical/fan/load control influences.
- **Lowest-effort resolution:** Optional single synchronized physical clutch/relay observation in a safe stationary setting. Do not repeat A/C button-only test.

### R03 · 0x0D4 B3 and B4

- **Current status:** calibration; very strong related sender-like pair; physical units uncalibrated.
- **Broadcast cadence:** 100 Hz; raw mask 0xFF each.
- **Observed values:** drive-a median B3=32/B4=157 (ranges B3 5–51, B4 128–199); drive-b 28/163; body parked B3=97/B4=58 (ranges 90–103,49–69).
- **Direct evidence:** At B3 change events, B3 ≈ 133.642446 - 0.646609 × B4 15 ms earlier. drive-a n=3108 RMSE0.560 R²0.98768; held-out drive-b n=1745 RMSE0.511 R²0.98982. Different fuel level between old drive-a and late capture supports sender relationship.
- **Limitations/rejected interpretations:** No confirmed absolute tank volume, gallons, true %, volts or ohms. The regression is approximate and does not replace a multi-point fuel-level curve.
- **Lowest-effort resolution:** Use refuel + stable level anchors during normal fill cycles; collect settled B3/B4 after fuel settles, never infer gallons from a single pair.

### R04 · 0x224 B2:B3

- **Current status:** provisional_calibration; fuel accumulator identified; 2007 volume scale provisional.
- **Broadcast cadence:** 10 Hz; raw mask 0xFFFF.
- **Observed values:** 16-bit BE raw counter always even in checked recordings; normalized counter is raw>>1, modulo32768; original raw modulo65536.
- **Direct evidence:** drive-a +15,236 raw ticks; drive-b +10,000 raw ticks; 21 deceleration cut intervals, 694 aligned samples at zero increment. User suggests porting 2003 calibration ~0.21117mL/normalized tick (=~0.105585mL/raw tick).
- **Limitations/rejected interpretations:** This volume scale is transferred from 2003, not independently metered on 2007. Do not treat resets after ignition as rollover.
- **Lowest-effort resolution:** Use as configurable MPG baseline, then check via one ordinary measured full-to-full fuel interval, with complete trip recordings.

### R05 · 0x0A6 B2

- **Current status:** semantic; demand/request-like candidate, not final actuator command.
- **Broadcast cadence:** 100 Hz; raw mask 0xFF.
- **Observed values:** Raw 4..208 in drive-a; responds during KOEO pedal steps. During three high-load upshifts remains 208 as feedback B3 drops to 68–71 and recovers.
- **Direct evidence:** KOEO B2 leads B3 roughly 5 packets/50ms on pedal transitions. Three shift dips start ~549–619ms after target shift request, with B2 fixed at 208.
- **Limitations/rejected interpretations:** No independent pedal PID (49,4A,4B unsupported); B2 cannot be claimed final PCM actuator command or % pedal.
- **Lowest-effort resolution:** Retain raw request-like overlay; identifying the true final actuator command requires independent factory or physical reference.

### R06 · 0x0A6 B4

- **Current status:** semantic; transformed B2 demand-like field.
- **Broadcast cadence:** 100 Hz; raw mask 0xFF.
- **Observed values:** Mostly B2−8,−9,or−10; during KOEO pedal-released B4=0; high-load B4 188..192 when B2=208.
- **Direct evidence:** B2−B4 distribution across 9,569 frames: 9 in 6,970; 10 in1,342; 8 in1,257; 21 DFCO entries all B4=0; high-load shifts retain high B4.
- **Limitations/rejected interpretations:** Not independently proven accelerator-pedal measurement, position percentage or final drive-by-wire actuator command.
- **Lowest-effort resolution:** Keep raw and avoid % pedal gauge without reference. Established B3 provides actual throttle OBD-equivalent.

### R07 · 0x0C8 B0:B1 and B4:B5

- **Current status:** partially_identified; both speed related, exact factory roles not proven.
- **Broadcast cadence:** 100 Hz; raw mask two BE16 speed channels.
- **Observed values:** Lower A and higher B nominal speed channels. B/A ≈1.0206 moving; A around 0.97984 B. Original 2003 had no occupied B0:B1.
- **Direct evidence:** drive-b: A integration8.392988km; higher B8.565633km, compared with 856 fine ticks/164=5.219512 mi (~8.4km). Distance calibration 164ticks/display mile, odometer BE24/1.61 independently matched factory.
- **Limitations/rejected interpretations:** No GPS verified physical speed, wheel circumference or definitive explanation for 2.06% difference. Do not use higher-speed channel automatically as odometer-ground speed.
- **Lowest-effort resolution:** Compare against independently logged GPS speed over normal driving, if desired; no need to redo distance-counter experiments.

### R08 · 0x0D4 B5:B6

- **Current status:** partially_identified; delayed speed alias; role incomplete.
- **Broadcast cadence:** 100 Hz; raw mask 0xFFFF.
- **Observed values:** BE16 raw approximately tracks high speed channel 0C8 B4:B5 with 0.27s lag and ~−52 raw count offset over moving range.
- **Direct evidence:** Cross-correlation about 0.99997 in both drive-a and drive-b above 1,000 raw speed counts; held-out fit residual 16.15 and18.31 raw units.
- **Limitations/rejected interpretations:** Not independent wheel speed, not proven odometer source, fitted offset poor near standstill.
- **Lowest-effort resolution:** Preserve as diagnostics/filtered speed, no additional experiment required for main CarStats speed.

### R09 · 0x1F4 B1 bit7

- **Current status:** semantic; strong max-detent candidate, not fully confirmed.
- **Broadcast cadence:** 25 Hz; raw mask 0x80.
- **Observed values:** B1 states include lights-off 100/0x64, lights-on 77/0x4D, minimum24/0x18, middle48/0x30, maximum228/0xE4 (=0x80|0x64).
- **Direct evidence:** Lights-ON sweep: 41 transitions/35 distinct byte values; bit7 sets once at max position, stays asserted for remaining recording.
- **Limitations/rejected interpretations:** Meaning of bit7 (override vs detent vs flag) unproven; B1 not a calibrated photometric 0–255 brightness percentage.
- **Lowest-effort resolution:** Treat 0xE4 as observed full-bright state; only investigate its distinction from intermediate 0x64 if exact firmware behavior is needed.

### R10 · 0x2E4 B0

- **Current status:** unidentified; repeatable initialization pattern; originating module unknown.
- **Broadcast cadence:** 10 Hz; raw mask 0xFF.
- **Observed values:** B0=FF for exactly 5 packets then 00 on some startup sequences (~0.493–0.497s); other bytes remain zero except protocol.
- **Direct evidence:** Seen in 3 initialization episodes, absent during 2 shorter reinitializations, so not a universal ignition-on flag.
- **Limitations/rejected interpretations:** Not eight independent flags, cannot prove cold boot, module/source origin, or identify device restart.
- **Lowest-effort resolution:** Preserve as diagnostics sentinel with observed timestamp and bus availability; physical meaning not necessary for main UI.

### R11 · 0x20C B0 bit1

- **Current status:** behavioral; strong ignition-ON association; power state incomplete.
- **Broadcast cadence:** 50 Hz; raw mask 0x02.
- **Observed values:** 2 with ignition ON, 0 during ACC/OFF in labeled standing sequence; 20C messages can continue while fast engine IDs stop.
- **Direct evidence:** Standing OFF/ACC/ON capture ON-associated; startup 2.427s 00→02 as high-rate traffic resumed.
- **Limitations/rejected interpretations:** Cannot distinguish ACC vs OFF using this bit; no long-term network sleep interval measured.
- **Lowest-effort resolution:** Use as ON-associated availability, freshness gate and independent key-off power path. Only test power-sleep timing if required for Pi shutdown design.

### R12 · 0x12C B6 bit3 cruise engaged + 0D4 B0 buttons

- **Current status:** behavioral; button/state decoded, numeric cruise setpoint missing.
- **Broadcast cadence:** 100 Hz; raw mask 0x08 & enum0xC0.
- **Observed values:** Six engaged intervals total577.293s; SET/RESUME status activation159–215ms, CANCEL41–48ms, brake20ms; cruise can overlap DFCO.
- **Direct evidence:** drive-a longest button-free speed median58.42 nominal mph range57.39–59.14mph; drive-b button-free speed median~49.16mph range48.31–49.80mph.
- **Limitations/rejected interpretations:** No separately decoded numerical target set speed; nominal observed speed is not exact cruise command.
- **Lowest-effort resolution:** Use observed speed and engaged state in UI; do not label an estimated speed as stored cruise setpoint.

### R13 · 0x188 + 0x0C8 + 0x12C reported gears and speeds

- **Current status:** behavioral; reported shift behavior decoded; physical converter input missing.
- **Broadcast cadence:** 100 Hz; raw mask status + multiple.
- **Observed values:** 74 clean shifts: 1→2 1.055s, 2→3 .975, 3→4 1.005, 4→5 .980; 5→4 .700, 4→3 .880,3→2 .860 median status durations.
- **Direct evidence:** Fifth-gear near-rigid band approx21.177 rpm/(nominal km/h); ~2,045rpm at nominal60mph, but can fall to1,201rpm at88.47km/h while still reported5th.
- **Limitations/rejected interpretations:** Not torque converter clutch lockup CAN bit, measured clutch transfer duration, transmission fluid temperature or input/turbine RPM.
- **Lowest-effort resolution:** Keep shift/coupling estimates explicitly inferred; no further passive F-CAN bytes identified for converter/TFT.

### R14 · 0x1F4 B2

- **Current status:** unexcited; observed zero in all first six 2007 recordings.
- **Broadcast cadence:** 25 Hz; raw mask 0xFF.
- **Observed values:** 0x00 across all 6 original 2007 logs; earlier 2003 separate capture had a lone 0x04 transient (different vehicle).
- **Direct evidence:** v0.5 full byte audit: variable=0x00 for the 2007.
- **Limitations/rejected interpretations:** Do not equate a constant byte with definitely unused or assign a physical label from the 2003 glitch.
- **Lowest-effort resolution:** Preserve raw only; no extra test without a new naturally occurring event.

### R15 · multiple other constant/reserved payload bits

- **Current status:** unexcited; unexcited only.
- **Broadcast cadence:** multiple/unknown; raw mask varies.
- **Observed values:** v0.5 six-log scan: 376/640 payload-bit positions never varied, and its 52 residual variable bits were counted before subsequent decodes.
- **Direct evidence:** Baseline 80-byte mask inventory; most now resolved or tracked related sender/speed channels, not 52 independent sensors.
- **Limitations/rejected interpretations:** Constant does not mean reserved by Honda; no evidence all potential status modes exercised.
- **Lowest-effort resolution:** Keep full raw snapshots; do not invent names or repeat previously completed switch tests.

## Body/electronics not independently visible in these F-CAN captures

Horn, individual window position/motor status, moonroof position, lock actuator/locked state, HVAC set temperature/airflow/recirculation/blower state, rear defogger, washer activation, actual hazard flash phase, DRL output, SRS/immobilizer/misc warning lamps. Most controls have ALREADY been operated in recorded tests, so absence of a standalone decoded F-CAN bit is NOT a request to repeat those tests. They may be B-CAN, diagnostic-only, or locally wired.

Actual torque-converter clutch command, converter input/turbine RPM, true pedal sensor %, final internal throttle actuator command, ATF temperature, physical oil pressure, module/battery voltage, absolute MPG-fuel calibration, actual cruise setpoint and individual wheel speeds have not been decoded through passive F-CAN. Some will require separate diagnostics or additional interfaces; not all are guaranteed to be broadcast anywhere.

## Data files in this archive

- `remaining_signal_register.csv/json`: this curated contemporary list and caveats.
- `per_capture_signal_stats.csv`: min/median/max/distinct and most common values for target byte positions in eight original/later full-CAN files.
- `v05_byte_masks_80.csv`: all 80 payload-byte slots with [date withheld] *historical* masks and variability; not current counts of unsolved signals.
- `v05_per_capture_byte_changes.csv`: 480 rows of transitions/range by byte (6 captures×80 slots).
- `evidence/...`: selected original packaged JSON/CSV source tables, copied unchanged (no raw logs duplicated). Read timestamps/counters and known source limitations before interpreting events.

## Analysis hygiene

1. Do not infer physical units, status polarity or safety-critical behavior from a co-moving bit alone.
2. Never treat stale frames as off/closed or add fuel/distance deltas across unobserved resets. Use modulo arithmetic only within continuous valid coverage.
3. The output marks hypotheses vs validations. Correlated fuel/throttle dynamics do not prove injector timing, physical compressor engagement or torque-converter lock.
4. Compare same-convention units: 0x224 *raw* fuel tick = half a *normalized* tick; absolute odometer BE24/1.61 is not the same scale as 0x0C8 B6 distance tick; 0x0C8 speed channels A and B differ ~2%.
5. There is no reliable published physical identity for 0x224 B1 from these sources. Don't relabel it BARO, LTFT, fuel level, etc.

