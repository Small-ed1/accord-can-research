# Remaining questions: complete 15-group register

This is the latest disposition of the original 2007 register, including calibration and semantic questions. It is not a claim that 15 unknown sensors remain. Earlier observations are preserved in the [source edition](../archive/2007/v13-remaining-register.json). The [current JSON](../data/remaining_signals.json) and [CSV](../data/remaining_signals.csv) carry the same groups.

The most useful new references are a complete metered fuel interval, a synchronized independent accessory/clutch-control reference, and an independently labeled diagnostic measurement for 224 B1. Repeating already completed body/HVAC switch sweeps is not the default next step.

Follow-up is tracked in the [2007 research checklist](https://github.com/Small-ed1/accord-can-research/issues/1) and [separate 2003 checklist](https://github.com/Small-ed1/accord-can-research/issues/2). Repository setup and software qualification do not replace the new measurements described below.

## R01: `0x224 B1`

**Current status:** unknown; no new physical identity.

Later continuous captures rechecked: first 4735 frames has one F3->F4 transition; second 7378 frames remains F4 while OBD MAP, RPM, coolant and trims vary widely.

**Limits:** Not a direct LTFT copy, MAP, ECT, fuel level, or monotonic fuel counter. BARO interpretation not supported.

**Useful next reference or handling:** Retain raw. Seek a genuinely independent Honda-specific diagnostic reference, not another unlabeled drive.

## R02: `0x0D4 B2 bit 6`

**Current status:** control/permission candidate; active-load meaning excluded.

Set during four fresh-RPM-zero intervals: drive-b 7.271s, standing 19.721s,14.202s,13.942s. Does not imply compressor rotation or present mechanical load. Electrical command/permission remains possible.

**Limits:** Not proven compressor clutch engaged. A/C switch tests did not uniquely toggle this bit. Could include electrical/fan/load control influences.

**Useful next reference or handling:** Keep a neutral label. A synchronized clutch/request diagnostic or safe physical reference is the remaining discriminator.

## R03: `0x0D4 B3 and B4`

**Current status:** sender-related pair; B3 output updates on a 5 Hz grid; volume uncalibrated.

B3 changes align to 200ms multiples in 4917 examined sub-5s inter-change intervals across drive-a/drive-b/Body. B4 can change at 10ms cadence. Prior low-fuel affine fit yields body RMSE1.360 and positive mean residual1.307 raw.

**Limits:** No confirmed absolute tank volume, gallons, true %, volts or ohms. The regression is approximate and does not replace a multi-point fuel-level curve.

**Useful next reference or handling:** Keep both observed channels; use stable refueling anchors to build a volume curve. Do not convert B3 directly into tank %.

## R04: `0x224 B2:B3`

**Current status:** provisional volume calibration unchanged.

Rechecked 25236 raw /12618 normalized increments in drive-a+drive-b. All raw values even. Retain0.105585mL/raw count or0.21117mL/normalized count as a configurable transfer from 2003.

**Limits:** This volume scale is transferred from 2003, not independently metered on 2007. Do not treat resets after ignition as rollover.

**Useful next reference or handling:** One ordinary fully recorded full-to-full interval can validate volume scale. Use the correct counter modulus and reject gaps/resets.

## R05: `0x0A6 B2`

**Current status:** upstream request-like raw channel; pedal identity unproven.

No change to B3 feedback calibration. B2=208 occurs both KOEO and under load. Existing shift-intervention evidence remains valid.

**Limits:** No independent pedal PID (49,4A,4B unsupported); B2 cannot be claimed final PCM actuator command or % pedal.

**Useful next reference or handling:** Expose request only as a raw/inferred quantity; no physical-pedal percentage.

## R06: `0x0A6 B4`

**Current status:** state-dependent demand-related channel; not a fixed B2-only transform.

At B2=208, B4=199 in430 standing frames; B4 spans188..196 in2437 drive-a frames and189..195 in353 drive-b frames.

**Limits:** Not independently proven accelerator-pedal measurement, position percentage or final drive-by-wire actuator command.

**Useful next reference or handling:** Preserve B4 separately. A fixed subtraction from B2 would erase observed state-dependent information. Physical pedal identity remains unproven.

## R07: `0x0C8 B0:B1 and B4:B5`

**Current status:** scaled speed representations; lower A favored for odometer-relative speed.

drive-a-trained B=1.020582138*A-0.069633682 predicts44994 moving drive-b samples with RMSE0.442 raw and maxabs1.332. A integration differs from fine-counter distance by-0.180% drive-a/-0.083% drive-b; higher B differs+1.873%/+1.972%.

**Limits:** No GPS verified physical speed, wheel circumference or definitive explanation for 2.06% difference. Do not use higher-speed channel automatically as odometer-ground speed.

**Useful next reference or handling:** Prefer nominal A/100 km/h for the odometer-consistent readout; retain B diagnostically. Keep confirmed1.61 and164 distance constants; physical speed still lacks GPS validation.

## R08: `0x0D4 B5:B6`

**Current status:** smoothed speed alias; exact consumer/purpose unknown.

drive-a-trained first-order time constant0.281s gives drive-b common-sample RMSE4.323 raw versus18.301 for a drive-a-trained pure-delay model. Both use45029 common moving samples.

**Limits:** Not independent wheel speed, not proven odometer source, fitted offset poor near standstill.

**Useful next reference or handling:** Retain as a filtered-speed diagnostic. Do not claim independent wheel speed or an exact firmware algorithm.

## R09: `0x1F4 B1 bit7`

**Current status:** strongly inferred night-dimming cancel / full-brightness override.

Body capture changes B1=80 to228 (0xE4) at255.138398s. 0xE4=0x80|100. Honda owner manual describes the full-right click as cancelling reduced night brightness.

**Limits:** Meaning of bit7 (override vs detent vs flag) unproven; B1 not a calibrated photometric 0–255 brightness percentage.

**Useful next reference or handling:** Decode lower7 bits separately from flag; use as observed override behavior with inference label. Do not treat228/255 as brightness.

## R10: `0x2E4 B0`

**Current status:** initialization sentinel with a longer-inactivity association; source unknown.

Standing: FF absent after1.937636s/1.327294s 2E4 gaps; five FF frames after28.058187s. Two other FF startups have unknown pre-recording history.

**Limits:** Not eight independent flags, cannot prove cold boot, module/source origin, or identify device restart.

**Useful next reference or handling:** Keep a startup diagnostic, not a universal ignition flag or proven cold-boot indicator.

## R11: `0x20C B0 bit1`

**Current status:** ON-associated bit usable only with freshness; whole-bus traffic insufficient.

During27.690228s without0D4, 1382 packets of20C continue with B0=0; other nine IDs have no frames inside that interval.

**Limits:** Cannot distinguish ACC vs OFF using this bit; no long-term network sleep interval measured.

**Useful next reference or handling:** Distinguish fresh bit-set/fresh bit-clear/stale-unknown. ACC versus OFF and long-term network sleep remain unresolved.

## R12: `0x12C B6 bit3 cruise engaged + 0D4 B0 buttons`

**Current status:** cruise state/buttons known; numeric setpoint absent.

No independently observed cruise target speed was added by this pass.

**Limits:** No separately decoded numerical target set speed; nominal observed speed is not exact cruise command.

**Useful next reference or handling:** Display engagement plus actual speed; do not fabricate a stored setpoint.

## R13: `0x188 + 0x0C8 + 0x12C reported gears and speeds`

**Current status:** gear and reported shifts known; converter lockup/temperature absent.

No turbine speed, TCC command or transmission-fluid temperature added by this pass.

**Limits:** Not torque converter clutch lockup CAN bit, measured clutch transfer duration, transmission fluid temperature or input/turbine RPM.

**Useful next reference or handling:** Keep coupling/shift inferences explicit; source missing quantities through independently supported diagnostics.

## R14: `0x1F4 B2`

**Current status:** unexcited, not proven unused.

1F4 B2 remains00 in all five full logs reprocessed here as well as the earlier original audit.

**Limits:** Do not equate a constant byte with definitely unused or assign a physical label from the 2003 glitch.

**Useful next reference or handling:** Preserve raw; do not assign the separate2003 transient to2007.

## R15: `multiple other constant/reserved payload bits`

**Current status:** constant/unexcited inventory; no new physical names.

Historical52 residual bits are not a current unresolved-sensor count. This pass does not claim a new global residual-mask audit.

**Limits:** Constant does not mean reserved by Honda; no evidence all potential status modes exercised.

**Useful next reference or handling:** Retain original masks as historical provenance, not a new list of52 mysteries.

## Body and powertrain quantities not independently decoded

Horn, individual window position/motor state, moonroof position, lock-actuator/locked state, HVAC set temperature/airflow/recirculation/blower state, rear defogger, washer activation, hazard flash phase, DRL output and SRS/immobilizer/miscellaneous warnings were not independently decoded in these F-CAN captures. Many switches were already exercised. A signal may be local, diagnostic-only, on another bus, or absent from the observed segment; no universal absence is established.

No passive-F-CAN decode establishes actual TCC command, converter/turbine input RPM, ATF temperature, physical pedal percentage, final internal throttle command, analog oil pressure, module/battery voltage, exact cruise setpoint or individual wheel speeds. Inferred coupling, lamp status and related speed channels do not fill those gaps.

## Additional 2003 limitations

The 2003 oil/charging and D-associated indications retain their candidate confidence, its fuel-sender electrical/volume scales remain approximate, its fine-distance scale has not been requalified here, and the single 1F4 B2 transient has no physical identity. A 2007 confirmation cannot settle those automatically. See the separate [2003 register](2003-findings.md).

All additional testing should be ordinary, stationary where possible, and independently labeled. Do not induce warnings by creating faults, disable safety systems or perform experimental frame transmission.
