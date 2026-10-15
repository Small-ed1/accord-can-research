# Sanitized historical source: 07-V05

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# 2007 Accord CAN: residual decoding pass, v0.5

## Result

All **1,364,106 frames in six original logs** were reprocessed. Existing signal fields, previously tracked candidates, rolling counters and checksums were masked for the novel-field search. Among the ten 8-byte message layouts, 264 bit positions varied; 212 were covered by those masks. **52 varying positions in 16 bytes remained**. Another 376 bit positions never varied; they are unexcited/constant in these captures, not proven unused.

The useful new result is **three exact cross-message status relationships**, a repeatable initialization sentinel, separation of two superficially similar startup flags, and a much stronger quantitative relationship between the two sender-like bytes. No new physically named HVAC, hazard, lock or trunk signal is justified by these recordings.

These are source-derived findings and explicit inferences. No outside vehicle database was used. The existing fuel-volume, speed calibration, seatbelt-polarity and compressor-command caveats remain in force. This report does not change the vehicle or install a CarStats decoder.

## 1. Newly resolved shared status fields

B0 means the first byte. Normalize both sides to Boolean before comparing masks.

| Neutral signal | Higher-rate field | Mirror in 0x405 | Fresh comparisons agreeing | Asserted comparisons |
|---|---|---|---:|---:|
| Status A | `0x12C B6 & 0x10` | `B0 & 0x01` | 7,585 / 7,585 | 189 |
| Status B | `0x1F4 B0 & 0x02` | `B1 & 0x01` | 7,590 / 7,590 | 40 |
| Status C | `0x224 B6 & 0x02` | `B3 & 0x01` | 7,584 / 7,584 | 230 |

Each comparison uses the latest preceding source message at the actual 0x405 timestamp, with a maximum source age of 0.2 seconds. Five, zero and six startup samples respectively have no eligible preceding source and are excluded, not counted as agreement. Both set and clear states are tested. Complete per-capture counts are in `exact_status_mirrors.json`.

**What is established:** these fields carry the same observed Boolean information at the checked timestamps. They should not be counted as six independent controls or sensors. **What is not established:** the physical dashboard icon associated with each signal, or which module originates the shared state.

### Status A: timed/engine-start-sensitive warning candidate

In the long engine-off/key-ON sweep, A asserts at 589.304559s and clears at 609.302624s: **19.998065 seconds**. Engine RPM stays zero until 619.351731s, a further **10.049107 seconds**. During shorter starts A instead clears shortly after rotation first appears.

This rules out treating A as a universal “engine stopped” flag. A timed diagnostic/warning indication is a better hypothesis, but a specific MIL, pressure or charging label is not proven.

Raw examples: standing log lines 352,010 and 352,016 carry the asserted pair; line [absolute reading withheld] clears A while RPM remains zero.

### Status B: startup/self-test indication candidate

The higher-rate source asserts for **2.152135, 2.153089, 2.154493, 2.157532 and 2.154002 seconds** across five reinitializations. It completes this interval even when the engine has already started. The slower 0x405 view appears slightly longer because it refreshes less often.

This strongly supports a startup/self-test role. Do not assign ABS, VSA, SRS or DRL lamp names without observing the cluster. drive-b log lines 481 and 483 show the pair asserted.

### Status C: engine-start-related warning candidate

C stays asserted in the engine-off/key-ON phases and clears **0.481 to 0.761 seconds after first detected rotation** across four starts. `0x224 B6 & 0x02` and `0x405 B3 & 0x01` agree exactly at every fresh comparison.

The offset from rotation is repeatable enough to distinguish it from A; it does not identify a pressure switch, charging state or proven successful start. Startup log lines 423 and 461 show both fields asserted.

## 2. A tempting merge that the data rejects

`0x405 B2 & 0x80` and `0x405 B3 & 0x01` look almost identical at a glance. **They disagree in seven actual 0x405 frames.** Five are initialization frames. Two more occur during starts, with opposite ordering:

| Capture / elapsed time | B2 & 0x80 | B3 & 0x01 |
|---|---:|---:|
| Standing, 750.240309s | Clear | Set |
| Startup, 3.271804s | Set | Clear |

Those examples are original lines 432,053 and 640 respectively. Keep B2 bit7 as an independent unresolved status channel. Neither averaging over time nor a 99.9%-style overall agreement justifies merging it into C.

The other remaining engine-start-related field, `0x0D4 B2 & 0x80`, also differs during cranking and shutdown. Keep it separate from both C and the already-tracked `B2 & 0x40` compressor candidate.

## 3. Initialization marker in 0x2E4

In three reinitialization episodes, **B0 is FF for exactly five frames**, then returns to 00. The asserted intervals last **0.492924, 0.496560 and 0.492864 seconds**. The other six non-checksum bytes remain zero in all captures.

Treat this as one **initialization-sentinel candidate**, not eight separate switch bits. It appears at the standing log's third reinitialization and at the start of the drive-b and short startup recordings. It does not occur at the standing log's two shorter reinitializations, so it is not a universal ignition-transition detector. It also does not identify the transmitting module or prove a particular type of boot.

drive-b raw line 138: `2E4#[raw payload withheld]`. The complete intervals and source lines are in `startup_events.json`.

## 4. Analogue fields: remove redundant hypotheses

### Sender-like pair: 0x0D4 B3 and B4

The earlier map already suspected a fuel sender/level relationship. This pass strengthens the **relationship**, not the physical units.

At native B3 change events, a model trained only on the drive-a recording is:

```
B3 ~= 133.642446 - 0.646609 * B4_at_15ms_earlier
```

B3 updates are quantized around a 0.2-second refresh; B4 changes much more frequently. Comparing simultaneous values at arbitrary points obscures the relationship.

| Evaluation | Change samples | RMSE, raw B3 units | R-squared |
|---|---:|---:|---:|
| Training: drive-a | 3,108 | 0.560 | 0.987680 |
| Held-out: drive-b | 1,745 | 0.511 | 0.989824 |

The drive-b data was not used to choose the slope/intercept or 15ms lookback. The error can still reach about 2.9 raw units, so this is **an approximate relationship, not an exact replacement decoder**.

This is strong evidence for two related representations of one underlying quantity. Retain the earlier fuel-sender identity as a hypothesis; the recordings do not establish litres, percent, voltage or resistance. No new tank calibration was performed.

### Speed-like pair: 0x0D4 B5:B6

This was already tracked as a speed candidate. A native-time regression corroborates it as approximately the higher `0x0C8 B4:B5` speed channel delayed **0.27 seconds**, with an offset near **-52 raw counts**. Correlation is about 0.99997 in each drive above 1,000 raw speed counts. The respective best-fit residual errors are 16.15 and 18.31 raw counts.

That removes another plausible “new sensor” from the search. Do not use the fitted offset near standstill or mistake a raw-channel fit for GPS calibration.

## 5. Remaining independent candidates

**0x188 B2 & 0x80:** a D-indicator/request interpretation is stronger than “actual gear.” Away from transition edges it tracks the D selector, but it also asserts during startup in P. Four starts show a 2.0s assertion; an immediate-crank start shows 0.4s. The actual D lamp still needs observation. Keep the already-established B3 selector decoder.

**0x20C B1:** 80 for the complete first drive; 79 for all five later recordings. No within-file change. There is not enough variation to identify its quantity or units.

**0x224 B1:** only 243, 244 and 245 occur, with a few slow changes in both directions. It is not a monotonic fuel-use counter. Temperature, fuel, pressure and other labels remain unproven.

**Constant fields:** retain them in raw recording. A bit that never changes is not evidence that the associated function cannot exist on this bus.

## 6. What the exclusion pass rules out for these captures

After known/tracked fields are masked:

- The hazards/dimmer region after the right-turn test changes only the sender-like B3/B4 pair.
- The lock/unlock region after the final driver-door pulse changes only B4's ongoing analogue noise.
- Section 2, between the 154.133s and 510.350s markers, changes only B3/B4 among the residual fields. The known wiper field and previously tracked compressor candidate were deliberately excluded from the new-field search.
- The later door and MAX A/C recordings add no new independently varying residual status bit.

No clean new binary HVAC, washer, hazard or lock state is supported. This is a limit of the **ten captured IDs and exercised actions**, not proof about every possible vehicle message, multiplexing scheme, network or diagnostic response. Exact individual actuation timestamps are still not supplied by the ordered checklist.

## 7. Smallest useful next experiment

A synchronized video of the **instrument cluster**, alongside the passive CAN log: key ON with engine stopped for **25 seconds**, then start and idle. Include a clearly visible initial marker in the video and log.

That one observation can attach actual lamp labels to A, B, C, B2 bit7 and the proposed D-indicator bit. It is more discriminating than another unlabeled road drive-a. Record in Park, stationary. No disconnects, warning-fault creation or CAN injection is needed.

## 8. Reproducibility and limits

Six-source inventory: 2312.512 seconds of recorded time, not a continuous session. All 1,364,106 lines parse as eight-byte frames from the same ten IDs. **1,307,199 applicable checksum checks pass**; 0x1F4 is excluded from that checksum formula. The observed rolling-counter discontinuities remain 0, 33, 1, 0, 1 and 0 by capture, including reinitializations; they are not automatically lost-frame counts.

The JSON files preserve the exact exclusion masks, every residual event, source line numbers, hashes, fit methodology, and contradictory examples. Counter resets, gaps and source freshness are never treated as proof of a physical state. The raw logs remain authoritative and unchanged.

Files: `capture_audit.json`, `mask_inventory.json`, `exact_status_mirrors.json`, `startup_events.json`, `analogue_relationships.json`, `residual_signal_map.json`, `residual_events_native.json`, `ruled_out_and_limits.json`, `verification.json`.

The package is an **offline evidence map**, not an installed decoder, an OEM DBC, or certification of warning-lamp meanings.

