# Sanitized historical source: 07-V03

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# Accord 2007 stationary test: checklist-matched revision 0.3

Source log: `standing-a.log`  
Basis: all 446,211 raw frames, the three supplied screenshots showing all 25 original checklist items, and the user's confirmation that actions were performed in that order with handbrake markers between numbered sections.

This replaces the earlier statement that the checklist/action order was unavailable. The screenshots supply ordered physical labels. They do not supply independent timestamps for each actuation. Frame timestamps below are matched to that order, not invented stopwatch labels.

This is an offline signal map. No CarStats software was installed or vehicle control messages sent.

## 1. Correct section boundaries

There are two handbrake-test applications inside section 1, followed by three actual section-boundary markers:

| Elapsed application to release | Role |
|---|---|
| 01:31.222 to 01:34.072 | Section 1: parking brake applied, then released |
| 01:35.382 to 02:27.062 | Section 1: reapplied, remaining applied during the following body tests |
| 02:30.482 to 02:34.133 | Section 1 Lighting and body → section 2 Wipers and HVAC |
| 08:30.350 to 08:33.071 | Section 2 → section 3 Powertrain and controls |
| 11:03.334 to 11:06.524 | Section 3 → section 4 Ignition states |

Thus the long handbrake hold was not a malformed marker. The earlier interpretation of all five intervals as section markers was incorrect.

Handbrake/status mapping: `0x0D4 B0 & 0x04`, mirrored by `0x405 B2 & 0x20`. Both agree in all 2,477 aligned comparisons. This is switch/status data, not a measurement of holding force.

## 2. Physical labels now supported

Byte indexes start at zero. Labels are empirical correlations for this vehicle, not an OEM-published DBC.

| Field | Interpretation | Evidence/confidence |
|---|---|---|
| `405 B2 & 04` | Driver seatbelt-related status | High confidence for control identity: two clear intervals during the ordered buckle step, before door tests |
| `405 B4 & 20` | Door-open status responding to the driver door; set=open | High confidence: three pulses in the driver-door open/close step |
| `0D4 B0 & 03` | Lighting enum: 0 off, 1 parking, 2 low, 3 high/flash | High confidence: exact mode order plus three flash pulses |
| `405 B3 & 08` | Lighting/illumination-active state | Correlates with parking/low/high sequence and the 77-versus-100 illumination byte; not limited to low beams |
| `0D4 B0 & 20` | Cruise MAIN enabled | High confidence: MAIN toggles immediately before the SET/RESUME/CANCEL sequence |
| `0D4 B0 & C0` | Cruise button enum: 00 none, 40 SET/DECEL, 80 RESUME/ACCEL, C0 CANCEL | High confidence: ordered stationary groups reinforce earlier drive behavior |
| `20C B0 & 02` | Ignition-ON-state candidate | High confidence for ON versus ACC/OFF association in this one labeled key sequence |

### Seatbelt detail and residual polarity limit

`405 B2 & 04` clears at 101.764–106.265s and 111.666–116.767s. The most natural ordered interpretation is clear=buckled and set=unbuckled/warning active.

However, it returns to set at 116.767s, after the second clear interval. That is an additional transition beyond the written sequence ending “buckled.” The user's declaration that the sequence was followed does not provide an explanation for that extra edge. Do not silently invent an additional unlatching action, erase the edge, or call the polarity fully independently verified. Keep the control identity high confidence and the polarity/status-versus-sensor meaning provisional.

### Driver-door detail

The three set intervals are 122.168–123.668s, 125.168–126.969s and 128.469–130.269s. These follow the seatbelt step and match three driver-door open/close cycles. Raw examples:

- Source line 73,096: `405#[raw payload withheld]` has B4=20.
- Source line 73,994: `405#[raw payload withheld]` has B4=00.

Only the driver door was tested. This does not establish that the bit is exclusive to that door, nor identify passenger/rear-door bits. It must not be labeled trunk or lock status.

## 3. Ignition sequence is now meaningfully labeled

The screenshot specifies: running → engine off/key ON for 15s → ACC for 15s → OFF for 15s → ON for 15s → start.

| Approximate elapsed interval | Matched physical phase | `20C B0 & 02` | RPM / traffic |
|---|---|---|---|
| 692.442–707.249s | First engine-off, key-ON dwell | Set | Zero RPM |
| 707.249–734.994s | Combined ACC and OFF dwells | Clear | Zero RPM; 20C persists while other streams stop |
| 734.994–749.512s | Second engine-off, key-ON dwell | Set | Zero RPM; other streams resume |
| From 749.512s | Rotation begins during start, then engine runs | Set | First positive RPM is cranking, not yet proof of stable idle |

These observed dwell lengths of about 14.8s, 27.7s combined, and 14.5s align with the user's ordered nominal 15-second actions. Exact key positions were not separately timestamped.

The internal ACC→OFF boundary has no independently identified CAN change, so it cannot be assigned an exact time from this file. Both give the same observed flag state. The flag also shows brief clear/set transitions while stopping and reinitializing, which must not be mistaken for long steady key positions.

For CarStats, use this only as a freshness-checked ON-state indicator. Do not treat “any CAN traffic” or “RPM zero” as an ignition decision. This capture does not establish long-term bus sleep or a safe shutdown grace period. It does not prove which module originates 20C or identify the exact electrical circuit being reported.

## 4. Section 2 weakens the proposed A/C labeling

The recovered list explicitly includes A/C OFF 60s → ON 120s → OFF 60s with blower and temperature fixed.

A full scan of `0D4 B2 & 40` during section 2, 154.133–510.350s, finds:
- Longest continuously clear interval: 19.892570s.
- Longest continuously asserted interval: 18.471853s.
- The bit cycles repeatedly throughout the section.
- It also asserts during zero-RPM phases.

Therefore the observed bit cannot be accepted as the direct A/C button-on state from this test. Its physical meaning remains an unresolved cyclic load/request/status signal. This does not establish that the user omitted the test, that the A/C malfunctioned, or that the bit definitely represents a fan instead. A commanded accessory state and actual mechanical operation remain separate questions.

No unique separately named fields were established for blower speed, recirculation, rear defroster or washer spray. Changes in RPM, throttle and fuel rate are indirect responses, not proof of a specific HVAC control.

## 5. Other limits revealed by the recovered order

### Hazards
Despite the reported hazard test, `1F4 B0 & 60` never equals60 in this capture. The known left/right fields respond to individual stalk requests, but the test does not establish a hazard-lamp-state decoder. Do not implement `hazards = left_request && right_request` on the assumption that hazards necessarily appear in those fields. This finding does not mean the physical hazards failed.

### Dimmer
The checklist places the dimmer sweep after headlights have been switched off. The light enum stays0 through that region and `1F4 B1` stays100. Only77 and100 exist in the full recording. The pass therefore does not establish minimum/middle/maximum scaling. A daytime-output override is one plausible explanation, not a verified implementation detail.

### Door locks
No separate reproducible lock/unlock state has been identified after the three driver-door pulses. The successful test of a physical control does not guarantee a newly identifiable field in these ten captured IDs.

### Wipers
The sequence supports the existing off/INT/low/high field in `(1F4 B0 >> 3) & 3`. The raw return from high passes through low and remains INT from173.276 to196.881s before reaching off. That extended INT state should not be silently renamed washer spray merely because spray comes next on the checklist. A separate spray bit is unresolved.

### Pedal sweep
The screenshots identify the zero-RPM sweep as a deliberate accelerator sweep. `0A6 B2/B3/B4` are consequently pedal-responsive in that experiment. This still does not identify exact pedal-position percentage versus commanded/actual throttle, nor prove that approximate quarter-pedal positions were precisely measured. Retain raw units.

## 6. Preserve the previous verified corrections

- `188 B0` can settle to6 in Reverse; the 07/06 → 06/06 transition remains valid.
- `188 B2 & 80` also asserts during startup in Park. It cannot unconditionally identify D.
- The `224 B2:B3` counter resets5208→0 and320→0. Do not count these as rollover fuel use.
- Distance and fuel-volume calibration are not supplied by the standing checklist.
- Startup warning bits remain unnamed without direct instrument-lamp observation.

## 7. Files in this revision

- `recovered_checklist.json`: all25 items, four original section titles, and source screenshot references.
- `section_markers.json`: corrected interpretation of all five parking-brake applications.
- `signal_updates.json`: revised physical labels, confidence and explicit limits.
- `native_signal_intervals_raw_labels_v02.json`: unchanged prior extracted intervals with original analytical names; use the new signal map for current semantics.
- `verification.json`: checks rerun on the full raw log in this revision.
- `README.md`: this report.

Original recordings and previously supplied packages were left unchanged.

