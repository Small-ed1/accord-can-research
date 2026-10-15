# Sanitized historical source: 07-V13

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# 2007 Accord F-CAN: remaining-signal follow-through
## Research revision 1.3 | [date withheld]

This is an offline reanalysis and refinement of the supplied remaining-signal register. No vehicle commands were sent, no new physical tests were performed, and no CarStats software was changed.

## Coverage and verification

Five recovered full-CAN recordings were reprocessed: drive-a (518,217 frames), drive-b (319,681), the later body/dimmer capture `raw.log` (158,096), the standing checklist (446,211), and the short startup capture (7,794). Total: **1,449,999 full-CAN frames**.

The nibble-sum checksum was applicable to 1,389,504 of these frames; all passed. The remaining 60,495 were 1F4 frames, for which that checksum rule is not applicable. Rolling-counter discontinuities are retained in `source_audit.json`; startup/power gaps are not silently treated as continuous recording.

Two later continuous 224 captures added **12,113 checked packets** (4,735 and 7,378). Their payload checksums all passed and their parsed B1/fuel columns matched the payload bytes. These are separate from the five full-CAN recordings above. The raw recordings overlap historical v0.5/v1.2 studies; do not add earlier study totals as independent evidence.

All byte indices are zero-based. Raw log source filenames, SHA-256 hashes, event line numbers, sample counts and calculations are supplied alongside this report.

## 1. The accessory bit is not proof of a running compressor

`0D4 B2 & 0x40` is asserted while the contemporaneous engine-RPM channel reports zero:

| Capture | First to last observed timestamp | Set packets with zero RPM |
|---|---:|---:|
| drive-b | 3.087695–10.359014 s | 728 |
| Standing | 599.418655–619.140035 s | 1,973 |
| Standing | 692.725073–706.927023 s | 1,421 |
| Standing | 735.277877–749.219964 s | 1,395 |

These are 7.271, 19.721, 14.202 and 13.942-second first-to-last observation spans. Maximum age of the preceding RPM reference was under 8.5 ms; these are not stale engine-RPM readings carried through a sleeping network.

**Conclusion:** an asserted bit cannot establish compressor rotation or present mechanical accessory load. An A/C request, permission, or electrical command remains possible. This finding does not rule out an energized stationary clutch or a clutch-command bit.

The earlier ~39.6% mean fuel-rate association still matters, but its 43 edge pairs are not 43 independent experiments: 39 came from one standing capture, and the individual fuel windows were approximately 2.4 seconds long. Do not translate that average into a fixed accessory-power or fuel-surcharge figure.

For CarStats, retain a neutral experimental control-state label. The missing discriminator is a synchronized, independently labeled A/C request/clutch signal or safe physical observation, not another unlabeled A/C-button sweep.

## 2. The two primary speed fields behave as scaled representations

Let A = BE16(0C8 B0:B1), and B = BE16(0C8 B4:B5).

Fitting drive-a moving samples gives:

    B ≈ 1.020582138 × A − 0.069633682

Keeping those coefficients unchanged predicts **44,994 moving samples in the separate drive-b recording** with RMSE **0.442 raw count** and maximum absolute error **1.332 raw counts**. The test range is A > 1,000 raw.

That supports two closely scaled representations of the same underlying motion quantity. There is no useful evidence here for treating them as independently varying wheel speeds. The exact source/consumer roles are still unidentified.

Using the existing nominal raw/100 km/h convention:

| Capture | Fine-counter distance | A integrated | B integrated |
|---|---:|---:|---:|
| drive-a | 16.495776 km | 16.466006 km | 16.804771 km |
| drive-b | 8.399991 km | 8.392988 km | 8.565633 km |

A differs from counter distance by −0.180% and −0.083%. B differs by +1.873% and +1.972%. These are whole-recording comparisons and retain endpoint quantization/filtering effects; they are not absolute physical-speed calibrations.

**CarStats recommendation:** prefer A for the odometer-consistent nominal speed readout and retain B diagnostically. Preserve the independently confirmed odometer divisor **1.61** and fine-distance calibration **164 ticks per odometer mile**. No GPS calibration or revised distance constant is claimed.

## 3. The secondary speed is better modeled as smoothed, not merely delayed

For `0D4 B5:B6`, a first-order smoothing model of speed B was fitted on drive-a only:

    z[n] = exp(−0.01 / τ) × z[n−1]
           + (1 − exp(−0.01 / τ)) × speed_B[n]

    τ = 0.281 seconds
    predicted_0D4_speed = 1.000154636 × z − 53.084032

The filter uses the nominal 10 ms source interval. Predictions are aligned to native 0D4 times with the last preceding source, at most 30 ms old.

A pure-delay alternative was also optimized on drive-a. Both fixed models were then evaluated on the same moving samples:

| Capture | Common samples | Smoothing RMSE | Pure-delay RMSE |
|---|---:|---:|---:|
| drive-a | 73,291 | 3.891 raw | 16.017 raw |
| Held-out drive-b | 45,029 | 4.323 raw | 18.301 raw |

**Conclusion:** smoothing explains these recordings substantially better than a pure time shift. This improves the signal's behavioral description; it does not recover Honda's exact firmware implementation or establish which subsystem uses it.

The comparison excludes the first five seconds and values at or below 1,000 raw in either predictor. The affine offset is not validated at standstill. Do not turn this fitted model into a substitute for the observed bytes.

## 4. Fuel-sender B3 has a 5 Hz output-update pattern

The 0D4 message broadcasts near 100 Hz, but its B3 value changes on approximately **200 ms boundaries**. Across drive-a, drive-b and the later body recording, all **4,917 examined inter-change intervals shorter than five seconds** were within 0.882 ms of an integer multiple of 200 ms.

B4 can change between adjacent ~10 ms packets. Thus, message frequency should not be advertised as 100 independent fuel-level updates per second. B3 behaves as a slower resampled/transformed representation of the sender-related quantity; internal sensor sampling itself was not observed.

The old low-fuel formula was also tested, unchanged, on the later high-sender-value body capture. At its 69 nonzero B3 change events:

- RMSE: **1.360 B3 counts**
- Mean observed-minus-predicted error: **+1.307 counts**
- Maximum absolute error: **2.447 counts**

This modest systematic difference reinforces the need to preserve the actual two channels. The old relationship remains useful for understanding their association, not for replacing either byte or calculating gallons.

Use settled refueling anchors from ordinary operation to build a volume curve. Neither B3/100 nor the old inverse regression establishes tank percentage.

## 5. Throttle B4 contains information that B2 alone cannot reproduce

A global fixed subtraction or single-input conversion from B2 to B4 fails. With **B2 held at 208**:

| Capture/condition | Frames | Observed B4 |
|---|---:|---:|
| Standing, engine-RPM zero | 430 | 199 |
| drive-a, running | 2,437 | 188–196 |
| drive-b, running | 353 | 189–195 |

This is state-dependent information. B4 should remain a separate raw field rather than be discarded as a fixed offset copy of B2.

The physical cause of the changing offset remains unresolved. Idle compensation or another request transformation would be hypotheses, not decoded identities. This evidence does not establish accelerator-pedal percentage.

Keep B2 and B4 as request-like experimental channels. Preserve B3's existing OBD-equivalent actual-throttle calibration, with its original tested-range and empirical-fit caveats.

## 6. The maximum-dimmer flag has a stronger semantic explanation

The body capture changes `1F4 B1` from 80 to **228 / 0xE4** at 255.138398 seconds:

    0xE4 = 0x80 | 100

Honda's 2007 Accord owner manual explains that turning the brightness knob fully right to the click cancels reduced night brightness. That behavior agrees with the recorded maximum-setting flag.

**Interpretation:** strongly inferred night-dimming cancel / full-brightness override. The manual documents the physical behavior, not this CAN bit. The capture contains only one activation of the high bit, so its full state logic is not manufacturer-confirmed.

Separate the lower-seven-bit level from bit 7. Do not compute brightness as 228/255, and do not equate a raw level with calibrated photometric brightness.

External source: Honda 2007 Accord Sedan Owner's Manual, printed page 71, reproduced at:
https://manuals.plus/m/[original source hash withheld]

## 7. Startup and power behavior are partial-network behavior

In the standing recording, the five-packet `2E4 B0=FF` burst appears after a **28.058-second gap in 2E4 traffic**. It is absent after two shorter gaps of **1.938 and 1.327 seconds**. The other two recorded FF starts have unknown pre-recording histories.

This is consistent with a longer-inactivity initialization state, but one measured long gap does not establish a sleep timeout, cold-boot rule, or originating module.

Crucially, during the associated **27.690-second gap in 0D4 traffic**, **1,382 packets of 20C continued**, all with B0=0. No other captured ID transmitted inside that interval.

For the Pi's power-state logic:

- Fresh `20C B0 & 0x02` set: ON-associated state.
- Fresh bit clear: not-ON-associated state; ACC versus OFF unresolved.
- Stale/missing data: unknown, not a fresh OFF indication.

Traffic alone cannot mean ignition ON. Neither this short recording nor the FF pattern establishes long-term network sleep or a complete shutdown/wake design.

## 8. 224 B1 and fuel-volume scale remain genuinely unresolved

The later first continuous capture has 4,735 packets and one F3→F4 transition. The second contains **7,378 F4 packets** over 737.571 seconds, while its OBD references span:

- RPM: 653–4,263
- MAP: 18–99 kPa
- Coolant: 81–92 °C
- LTFT: −10.15625% to −7.81250%
- STFT: −25% to +10.15625%

These reinforce the rejection of a direct copy of those changing measurements. They do not identify the hidden quantity. No new physical label is assigned to B1.

For the fuel accumulator, drive-a and drive-b were independently recounted as **15,236 + 10,000 = 25,236 raw increments**, or **12,618 normalized increments**. The transferred scale remains:

    mL ≈ summed_raw_delta × 0.105585
       ≈ summed_normalized_delta × 0.21117

This would represent 2,664.543 mL for those two drives, strictly as a provisional calibration check, not a metered 2007 fuel measurement.

Use raw modulo 65,536 or normalized modulo 32,768 only within continuous valid coverage. Ignition resets and missing coverage must not become apparent fuel consumption. A fully recorded ordinary full-to-full fuel interval remains the appropriate calibration reference.

## Disposition of all 15 original groups

| Group | Disposition after this pass |
|---|---|
| R01: 224 B1 | Unknown; direct-copy interpretations remain rejected. |
| R02: accessory bit | Control/permission candidate; asserted state does not prove active load. |
| R03: sender pair | Related channels; B3 has a 5 Hz output-update grid; volume still uncalibrated. |
| R04: fuel counter | Counter recounted; transferred volume scale remains provisional. |
| R05: throttle B2 | Upstream request-like; no physical pedal identity. |
| R06: throttle B4 | State-dependent information; preserve separately from B2. |
| R07: two speeds | Scaled representations; lower A best matches odometer-relative distance. |
| R08: secondary speed | Smoothing model favored; exact purpose unknown. |
| R09: dimmer bit | Strong full-brightness/night-dimming-cancel interpretation. |
| R10: startup FF | Conditional initialization sentinel; not a universal ignition flag. |
| R11: ignition-associated bit | Useful with freshness; ACC/OFF and sleep timing remain unresolved. |
| R12: cruise | State/buttons usable; no newly identified numerical setpoint. |
| R13: transmission | Gear/shift states usable; no new TCC, turbine speed or fluid-temperature channel. |
| R14: 1F4 B2 | Still zero in the five reprocessed logs; not proven unused. |
| R15: other constant bits | Historical masks retained; no new global residual-mask count claimed. |

The highest-value remaining references are a metered fill-to-fill interval with complete coverage, a synchronized compressor-control reference, and an independently labeled diagnostic reference for 224 B1. Previously completed body/HVAC switch sweeps do not need to be repeated merely because no separate F-CAN status was identified.

