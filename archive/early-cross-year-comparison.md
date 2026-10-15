# Sanitized historical source: COMPARE-EARLY

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# Honda Accord F-CAN: 2003 versus 2007
Consolidated register, 13 October 2026. Scope: the recovered 2003 full map and later source updates, versus all six 2007 logs through analysis v0.5.

**Conventions:** B0 is the first byte. CAN IDs, masks and enum codes are hexadecimal unless stated otherwise. BE16 and BE24 use the first listed byte as most significant. A set bit is Boolean true. Missing/stale data is unavailable, not false.

**Labeled** means a supported physical/control identity. **Partial** means a known field or quantity with remaining scale/polarity/state caveats. **Hypothesis** is not a confirmed physical name. **Unknown** has no supported physical label. Calibration is a conversion parameter, not an extra CAN field.

## Source/version boundaries
The 2003 baseline is the actual Accord_CAN_Full_Mapping_2026-09-24.xlsx, with all 46 original Signal Map rows preserved in the workbook. Later dimmer source, the [date withheld] odometer review, and [date withheld] fuel analysis are separate evidence. This register does not silently rewrite the original document's stronger historical claims.

The [date withheld] reference called the odometer whole kilometres, but the [date withheld] review retained the unresolved factory-display mismatch. Neither that review nor the raw field establishes a 256-ticks-per-mile setting. The 2007 164-tick relationship remains a conditional dashboard-relative calibration.

Four additional IDs (0A6,20C,2E4,405) are observed on the 2007 relative to the recovered six-ID 2003 dataset. This does not claim those IDs can never appear on any 2003.

## Labeled fields
| Signal / quantity | 2007 field | 2007 status | Decode / observed rule | 2003 comparison | Limits / interpretation | Source codes |
| --- | --- | --- | --- | --- | --- | --- |
| Engine RPM | 0x12C B4:B5 | Labeled | BE16(B4,B5), rpm | OBD-validated, same field and direct-RPM scale. | No divide-by-four. 2007 has trace support, not a new paired OBD calibration. | 03-MAP; 03-V3; 07-V01 |
| Coolant temperature | 0x12C B0 | Labeled | B0 - 40, °C | OBD-validated; same formula. | 2003 independent validation is narrower than a full sensor-range calibration. | 03-MAP; 03-V3; 07-V01 |
| Intake-air temperature | 0x12C B1 | Labeled | B1 - 40, °C | OBD-validated identity; same approximate formula. | 2003 comparisons were within 1 °C; preserve ordinary sensor uncertainty. | 03-MAP; 03-V3; 07-V01 |
| Duplicate RPM | 0x20C B4:B5 | Labeled | BE16(B4,B5), rpm | 0x20C not observed in the recovered 2003 six-ID captures. | Duplicate measurement at roughly 50 Hz, not a second independent RPM sensor. | 03-MAP; 07-V01; 07-V04 |
| Actual gear / transition status | 0x188 B0 | Labeled | 0=P/N; 1–5=forward; 6=Reverse; 7=transition/unsettled | Same codes; settled Reverse=6 was already confirmed on 2003. | Use selector to distinguish P/N; 7 can persist during Reverse engagement or startup and is not 7th gear. | 03-MAP; 03-V3; 07-V02; 07-V03 |
| Target/requested gear | 0x188 B1 | Labeled | 0=P/N; 1–5=forward target; 6=Reverse target | Same field and codes. | Target is not proof that the shift has completed. | 03-MAP; 03-V3; 07-V03 |
| Full physical selector | 0x188 B3 | Labeled | 00=between detents; 01=P; 02=R; 04=N; 08=D; 20=D3; 40=2; 80=1 | Same full seven-position mapping. | Hex codes; 0x10 never appeared. Do not treat 0 as Park. | 03-MAP; 03-V3; 07-V03 |
| Service-brake switch | 0x12C B6 & 0x01 | Labeled | Set=pedal applied | Vehicle-confirmed; same bit. | Binary switch, not hydraulic pressure or braking force. | 03-MAP; 03-V3; 07-V01; 07-V03 |
| Parking-brake switch | 0x0D4 B0 & 0x04 | Labeled | Set=handbrake applied | Vehicle-confirmed; same bit. | Not holding force or the brake-fluid portion of a combined warning lamp. | 03-MAP; 03-V3; 07-V03; 07-V04 |
| Parking-brake mirror | 0x405 B2 & 0x20 | Labeled | Set=handbrake applied | 0x405 not observed in the recovered 2003 captures. | Same observed state as 0D4, refreshed more slowly; not an independent switch. | 03-MAP; 07-V02; 07-V04 |
| Exterior-light switch mode | 0x0D4 B0 & 0x03 | Labeled | 0=off; 1=parking; 2=low; 3=high/flash | Same enum, vehicle-confirmed. | Switch/request mode, not proof of bulb output or DRL state. | 03-MAP; 03-V3; 07-V03 |
| Lighting/illumination-active state | 0x405 B3 & 0x08 | Labeled | Set through tested parking/low/high sequence | 0x405 not observed in recovered 2003 captures. | Also agrees with 77-versus-100 brightness output; not limited to low beams. | 03-MAP; 07-V02; 07-V03 |
| Left turn request | 0x1F4 B0 & 0x20 | Labeled | Set=left stalk request | Same bit, vehicle-confirmed. | Not a validated flashing-lamp phase or hazard state. | 03-MAP; 03-V3; 07-V03 |
| Right turn request | 0x1F4 B0 & 0x40 | Labeled | Set=right stalk request | Same bit, vehicle-confirmed. | Not a validated flashing-lamp phase or hazard state. | 03-MAP; 03-V3; 07-V03 |
| Wiper operating mode | 0x1F4 (B0 >> 3) & 0x03 | Labeled | 0=off; 1=intermittent; 2=low; 3=high | Same mapping; 2003 high and manual-up shared code 3. | No independent mist/washer/delay mapping; do not infer additional positions. | 03-MAP; 03-V3; 07-V03 |
| Cruise MAIN enabled | 0x0D4 B0 & 0x20 | Labeled | Set=MAIN enabled | No clean mapping in 2003 labeled test; upper B0 bits were recorded zero in the full-map baseline. | Newly mapped relative to recovered 2003 work; does not establish factory feature absence on 2003. | 03-MAP; 03-V3; 03-REVIEW; 07-V03 |
| Cruise button enum | 0x0D4 B0 & 0xC0 | Labeled | 00=none; 40=SET/DECEL; 80=RESUME/ACCEL; C0=CANCEL | Not decoded in recovered 2003 work; corresponding baseline bits were zero. | One enum, not two separate Boolean switches. | 03-MAP; 03-REVIEW; 07-V03; 07-V04 |
| Cruise engaged | 0x12C B6 & 0x08 | Labeled | Set=cruise engaged | Not decoded in recovered 2003 work; 2003 Cruise UI explicitly did not claim engagement. | Separate from MAIN and individual button presses. | 03-MAP; 03-REVIEW; 07-V01; 07-V04 |
| Front-left / driver door open | 0x405 B4 & 0x20 | Labeled | Set=open; clear=closed | No individual-door F-CAN mapping in recovered 2003 six-ID reference. | Individually exercised; simultaneous combinations not yet captured. Stale message means unavailable. | 03-MAP; 07-V03; 07-V04 |
| Front-right door open | 0x405 B4 & 0x40 | Labeled | Set=open; clear=closed | No individual-door F-CAN mapping in recovered 2003 six-ID reference. | Individually exercised; simultaneous combinations not yet captured. Stale message means unavailable. | 03-MAP; 07-V03; 07-V04 |
| Rear-right door open | 0x405 B5 & 0x01 | Labeled | Set=open; clear=closed | No individual-door F-CAN mapping in recovered 2003 six-ID reference. | Individually exercised; simultaneous combinations not yet captured. Stale message means unavailable. | 03-MAP; 07-V03; 07-V04 |
| Rear-left door open | 0x405 B4 & 0x80 | Labeled | Set=open; clear=closed | No individual-door F-CAN mapping in recovered 2003 six-ID reference. | Individually exercised; simultaneous combinations not yet captured. Stale message means unavailable. | 03-MAP; 07-V03; 07-V04 |

## Partly resolved and calibration
| Signal / quantity | 2007 field | 2007 status | Decode / observed rule | 2003 comparison | Limits / interpretation | Source codes |
| --- | --- | --- | --- | --- | --- | --- |
| Higher/native speed channel B | 0x0C8 B4:B5 | Partial | BE16/100, nominal km/h | Same field; archived native /100 scale and separate OBD-equivalent raw × 0.0098. | 2007 physical absolute scale awaits GPS/dashboard pairing; channel B is about 2.06% above A. | 03-MAP; 03-V3; 07-V01; 07-V04 |
| Additional lower speed channel A | 0x0C8 B0:B1 | Partial | BE16/100, nominal km/h | These bytes were zero in the original 2003 captures. | New occupied field. drive-b integration fits provisional odometer-relative distance better; not GPS calibration. | 03-MAP; 07-V04 |
| Filtered/secondary speed | 0x0D4 B5:B6 | Partial | BE16/100, nominal km/h | Same speed-related pair; about 0.26 s lag and -0.78 km/h fitted bias in the 2003 fuel test. | 2007 approximately 0.27 s behind channel B with -52 raw-count fitted bias in moving data; not an exact low-speed formula. | 03-MAP; 07-V05 |
| Incremental distance counter | 0x0C8 B6 | Partial | delta=(new-old)&255 within continuous coverage | Modulo-256 byte; archived 0.01 km/tick convention, supported by integration in 2003 logs. | 2007 repeatedly has 164 ticks per coarse update. 164 ticks/dashboard-mile is conditional, not independently calibrated. | 03-MAP; 03-REVIEW; 07-V04 |
| Coarse odometer / cumulative distance | 0x1F4 B3:B5 | Partial | BE24 raw | [date withheld] map called this whole km; [date withheld] review retained unresolved absolute dashboard mismatch. | Same bytes. Do not silently port raw/1.609344 or a 256-ticks-per-mile assumption. Absolute anchor still required. | 03-MAP; 03-REVIEW; 07-V01; 07-V04 |
| Fuel-use accumulator | 0x224 B2:B3 | Partial | BE16 raw, modulo65536; optional raw>>1, modulo32768 | Functional fuel-use identity confirmed. Later service emits shifted counts. | Counter meaning is established; gallons/litres are not calibrated for 2007. Reinitialize after resets/gaps. | 03-MAP; 03-FUEL; 07-V01; 07-V03; 07-V04 |
| Fuel volume per count | Same accumulator, not another field | Calibration | 2007 mL per raw or shifted count remains unset | [date withheld] working 0.09–0.10 mL/raw; later [date withheld] analysis used user-supplied 0.211 mL/decoded count. | Later 03 convention raw>>1 implies ~0.1055 mL/raw if 0.211 is per shifted count. Never mix the conventions or claim a 2007 fill calibration. | 03-MAP; 03-FUEL; 03-[date withheld]; 07-V03; 07-V04 |
| Cluster brightness/dimmer output | 0x1F4 B1 | Partial | Raw decimal 77 and 100 observed on 2007 | [date withheld] hypothesis; [date withheld] source handles levels0–99 and special full-bright 0xE4. | 2007 min/max sweep was performed with lights off; numeric knob scale and override semantics still unverified. | 03-MAP; 03-PATCH; 07-V03 |
| Driver seatbelt-related state | 0x405 B2 & 0x04 | Partial | Likely set=unbuckled/warning; clear=buckled | 0x405 absent in the recovered 2003 six-ID captures. | Control identity supported by ordered test; extra edge prevents claiming perfect buckle polarity or sensor-versus-warning semantics. | 03-MAP; 07-V03 |
| Ignition-ON association | 0x20C B0 & 0x02 | Partial | Set=ON-associated; clear in recorded ACC/OFF phases | 0x20C absent in recovered 2003 captures; no equivalent direct ON flag decoded. | Strong labeled association; cannot distinguish ACC from OFF, exact circuit, or long-term sleep. Freshness required. | 03-MAP; 07-V03; 07-V04 |

## Hypotheses and physically unnamed fields
| Signal / quantity | 2007 field | 2007 status | Decode / observed rule | 2003 comparison | Limits / interpretation | Source codes |
| --- | --- | --- | --- | --- | --- | --- |
| Deceleration fuel-cut status | 0x0A6 B0 & 0x02 | Hypothesis | Set=fuel-cut candidate | 0x0A6 not captured. Fuel-cut behavior was identified from a flat0x224 counter while moving/in gear. | Flat fuel counter within all tested asserted intervals, including sustained coast intervals; no independent injector/status reference. | 03-MAP; 07-V01; 07-V04 |
| Throttle/pedal-responsive channel A | 0x0A6 B2 | Hypothesis | Raw byte only | 0x0A6 absent; no defensible direct throttle/pedal field in original six IDs. | Commanded/target throttle or effective demand. No calibrated %, angle, or definite accelerator-versus-throttle identity. | 03-MAP; 07-V01; 07-V02; 07-V03 |
| Throttle/pedal-responsive channel B | 0x0A6 B3 | Hypothesis | Raw byte only | 0x0A6 absent; no defensible direct throttle/pedal field in original six IDs. | Actual/feedback throttle; delayed relative to B2. No calibrated %, angle, or definite accelerator-versus-throttle identity. | 03-MAP; 07-V01; 07-V02; 07-V03 |
| Throttle/pedal-responsive relative channel | 0x0A6 B4 | Hypothesis | Raw byte only | 0x0A6 absent; no defensible direct throttle/pedal field in original six IDs. | Relative/effective demand; approximately B2 minus9–10 in selected engine-off window. No calibrated %, angle, or definite accelerator-versus-throttle identity. | 03-MAP; 07-V01; 07-V02; 07-V03 |
| A/C compressor-related command | 0x0D4 B2 & 0x40 | Hypothesis | Set=probable compressor request/permission | Same bit; A/C/compressor-related behavior was labeled vehicle-confirmed, not just button latch. | 2007 MAXAC holds it on; cycling continues in OFF portions and at zeroRPM. Physical clutch actuation not verified. | 03-MAP; 07-V03; 07-V04 |
| Fuel gauge/level representation | 0x0D4 B3 | Hypothesis | Raw byte; prior03 angle interpretation | Very-high-confidence fuel gauge angle: roughly5 empty,50 half,100 full. | 2007 sender-pair relationship is strong (held-out R²0.9898), but no07 gauge-angle/level calibration. Do not use regression as exact decoder. | 03-MAP; 03-V3; 07-V05 |
| Fuel-sender electrical representation | 0x0D4 B4 | Hypothesis | Raw byte; candidate03 formula B4*5/255 V | Very-high-confidence approximate sender voltage; reference full~1V,half~2.5V,empty~4V. | 2007 related inverse pair established; voltage, resistance and gallons unvalidated on07. | 03-MAP; 03-V3; 07-V05 |
| Status A / MIL hypothesis | 0x12C B6 & 0x10; mirror0x405 B0 & 0x01 | Hypothesis | Boolean pair, exact on7585 fresh comparisons | 12C bit labeled MIL/check-engine with very high inferred confidence, not a fault-on confirmation. | New07 timing: can clear after~20s withRPM0. Earlier03 MIL label is a useful hypothesis, not new physical confirmation; mirror unknown on03. | 03-MAP; 07-V05 |
| Status B / startup self-test | 0x1F4 B0 & 0x02; mirror0x405 B1 & 0x01 | Hypothesis | Boolean pair, exact on7590 fresh comparisons | No physical label in03 map; bit not part of decoded03 wiper/turn fields. | 2.152–2.158s startup pulse. ABS/SRS/VSA/DRL identities not determined. | 03-MAP; 07-V05 |
| Status C / charging-warning hypothesis | 0x224 B6 & 0x02; mirror0x405 B3 & 0x01 | Hypothesis | Boolean pair, exact on7584 fresh comparisons | 224 bit was a strong charging/battery-indicator candidate, not physically fault-confirmed. | 2007 clears0.48–0.76s after first rotation. Preserve battery-warning hypothesis without asserting lamp identity. | 03-MAP; 07-V05 |
| Status E / oil-switch hypothesis | 0x0D4 B2 & 0x80 | Hypothesis | Boolean engine-start-related state | Same bit was a strong oil-pressure-switch/engine-off candidate. | Distinct from statusC and compressor bit. At most candidate switch/lamp, never measured oil pressure. | 03-MAP; 07-V05 |
| Status D / independent startup warning | 0x405 B2 & 0x80 | Unknown | Boolean; physical warning/status unknown | 0x405 not observed in recovered03 captures. | Seven actual-frame disagreements from405 B3&01; do not merge into charging/statusC. | 03-MAP; 07-V05 |
| D-indicator / D-range request | 0x188 B2 & 0x80 | Hypothesis | Set inD and some startup states | D-range/confirmation candidate, not TCC or shift-lock. | Also set during startup inPark. D-lamp/test-command interpretation plausible, but not physically confirmed. | 03-MAP; 07-V02; 07-V05 |
| Initialization sentinel | 0x2E4 B0 | Hypothesis | B0==0xFF; otherwise0 | 0x2E4 not captured in03 reference. | Five FF frames,~0.5s, in three reinitializations; absent in two short ones. Not a universal key-cycle detector. | 03-MAP; 07-V05 |
| Slow/per-session value | 0x20C B1 | Unknown | Decimal79 or80 | 0x20C absent in03 captured reference. | No within-file change; no defensible temperature/pressure/calibration identity. | 03-MAP; 07-V05 |
| Slow engine-message value | 0x224 B1 | Unknown | Decimal243–245 on07 | Already unresolved on03; values0xF3–0xF6 (243–246) then. | Slow learned/environmental/calibration state possible; not established BARO, trim, temperature or fuel count. | 03-MAP; 07-V05 |
| Rare meter transient | 0x1F4 B2 | Unknown | 07 constant0;03 one0x04 frame | Unresolved single0x04 transient during lighting test. | Not observed varying in the07 recordings. No justified physical control label. | 03-MAP; 07-V05 |

## Functions without a verified CAN field
| Function | 2007 | 2003 | Limit | Sources |
| --- | --- | --- | --- | --- |
| Hazards / actual turn-lamp flash phase | No verified encoding; 1F4 left and right masks did not jointly assert during the hazard test. | No distinct hazard encoding found. | Do not synthesize hazard state from left&&right. | 03-MAP; 07-V03; 07-V05 |
| Separate washer spray / mist | No dedicated mapping. | Pull-back mist not represented in1F4 B0; high/manual-up shared a code. | Wiper-mode changes are not proof of spray. | 03-MAP; 07-V03; 07-V05 |
| Intermittent wiper-delay setting | No verified encoding. | Not represented in the decoded1F4 wiper field. | Only operating mode is labeled. | 03-MAP; 07-V03 |
| Door lock/unlock state or request | No clean residual field after the labeled test. | No such F-CAN mapping in the recovered full reference. | Door-ajar bits are not lock status. | 03-MAP; 07-V03; 07-V05 |
| Trunk-open state | No field established in reviewed captures. | No mapped field in recovered full reference. | Four-door mapping does not establish trunk. | 03-MAP; 07-V04; 07-V05 |
| Blower speed, recirculation, rear defrost, temperature command | No independently labeled fields. | No clean recirc/rear-defrost fields; other HVAC fields unmapped. | RPM/fuel response is an indirect load response, not a control decoder. | 03-MAP; 03-V3; 07-V03; 07-V05 |
| DRL lamp output | Unmapped. | No DRL output field in recovered reference. | Headlight switch enum and parking brake do not prove DRL output. | 03-MAP; 07-V04; 07-V05 |
| Individual ABS / SRS / VSA warning-lamp identities | Unmapped; startup/self-test bits isolated. | No verified individual mappings in recovered reference. | Do not label neutral statusB as a specific lamp. | 03-MAP; 07-V05 |
| Torque-converter lockup / slip state | No direct field identified. | Explicitly unresolved in03 full map. | 188 B2&80 is not proven TCC. | 03-MAP; 07-V05 |
| Calibrated pedal% / commanded throttle% / actual throttle angle | No exact independent identity and unit calibration;0A6 candidates only. | No defensible direct CAN mapping. | Keep channel raw values until paired independent references. | 03-MAP; 07-V03 |
| MAP, BARO, calculated load, battery voltage, ignition timing, fuel trims, O2 / air-fuel values | No established direct CAN fields. | Direct throttle/MAP/load/voltage/timing/trims/O2 explicitly unresolved; BARO not established. | OBD/scanner readings and UI placeholders are not CAN decodes. | 03-MAP; 07-V05 |
| Exact ACC-versus-OFF separation / long-term sleep | Not resolved;20C survives both observed dwells. | No equivalent direct state mapped in03 recovered captures. | Any-CAN-traffic cannot be used as ignition ON. | 03-MAP; 07-V03; 07-V04 |

## Protocol
| Item | 2007 scope | Rule | 2003 comparison | Limit |
| --- | --- | --- | --- | --- |
| Rolling counter | All10 observed07 IDs; B7 bits7:6 | (B7>>6)&3, modulo4 perID | Same across all6 observed03 IDs | Can hide losses in multiples of4; reinitializations reset continuity. |
| Nibble checksum | 07: every observedID except0x1F4 | (-sum(nibbles ofB0..B6) -(B7>>4)) &15; compareB7&15 | 03: established on0D4,12C,188,224 only | Important07 difference:0C8 now carries the validated checksum. |
| Counter-only tail | 07:0x1F4 B7 | B7 in00/40/80/C0; lower6 bits0 | 03:0x1F4 and0x0C8 had counter-only tails in analyzed records | Do not apply checksum validation to07 1F4. |
| Observed rates | 07:0A6,0C8,0D4,12C,188=100Hz;20C=50Hz;1F4=25Hz;224,2E4=10Hz;405≈3.33Hz | Nominal while active | 03:0C8,0D4,12C,188≈100Hz;1F4≈25Hz;224≈10Hz | Frame cadence is not independent sensor-update cadence. |

## Complete byte accounting
The workbook and 2007_byte_audit.csv enumerate all 80 bytes (640 bit positions). All 264 observed varying positions are assigned to a labeled, partial, hypothesized, unknown or protocol field. That does not mean all are semantically decoded. The residual pass's 52 bits were search residuals after its chosen exclusions, not 52 independent new sensors. The 376 never-varying positions may include high bits of valid numeric fields and unexercised states; they are not proven unused.

## Sources
| Code | Document | Use | File ID |
| --- | --- | --- | --- |
| 03-MAP | Accord_CAN_Full_Mapping_2026-09-24.xlsx | 2003 reference; all 46 original Signal Map rows retained | [private source identifier withheld] |
| 03-V3 | CAN_FINDINGS_v3.md | September24 research handoff; confidence and negative findings | [private source identifier withheld] |
| 03-PATCH | CarStats_API_Scanner_v0.5.patch | September25 implemented dimmer 0–99 and special0xE4 handling | [private source identifier withheld] |
| 03-FUEL | CarStats_STEP6_Fuel_v0.3_Cumulative.patch | Decoded fuel counts are raw>>1; original default0.20mL/decoded count | [private source identifier withheld] |
| 03-REVIEW | CarStats_v5_Review.md | September27 review: absolute odometer discrepancy unresolved; Cruise page did not have actual cruise status | [private source identifier withheld] |
| 03-[date withheld] | carstats-analysis-[date withheld].pdf | October1 analysis uses user-supplied0.211mL/count; not an independent calibration experiment | [private source identifier withheld] |
| 07-V01 | accord07_can_analysis/README.md | drive-a baseline, core signals and scale limits; gear qualification superseded byV02 | [private source identifier withheld] |
| 07-V02 | accord07_standing_test_analysis/README.md | Standing tests; Reverse=6, counter resets, standby traffic; order limitations superseded byV03 | [private source identifier withheld] |
| 07-V03 | accord07_labeled_test_v03/README.md | Recovered physical checklist order; labels and residual caveats | [private source identifier withheld] |
| 07-V04 | accord07_oct13_followup_v04/README.md | Four follow-up captures; door mapping, MAXAC, speed, cruise and fuel cut | [private source identifier withheld] |
| 07-V05 | accord07_residual_decode_v05/README.md and mask_inventory.json | Six-log residual audit; 80 bytes,264 changing positions, warning mirrors | [private source identifier withheld]; package [private source identifier withheld] |

No raw recording or original 2003 workbook was modified. This comparison creates no installed decoder and sends no vehicle messages.
