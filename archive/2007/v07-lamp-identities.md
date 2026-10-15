# Sanitized historical source: 07-V07

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# 2007 Accord cluster-warning video + CAN correlation (v0.7)

This package analyzes `cluster_lamps.log` (49,362 8-byte CAN frames, 86.187 seconds, ten 11-bit IDs) against the user-supplied `[source media withheld]` (81.6 seconds, 30 fps), with spot-checks over seven earlier [date withheld] logs and the separate [date withheld] body/dimmer log. The actual capture is **passive**. The video elapsed clock aligns to the CAN log at video_time = CAN_elapsed + about 3.18 seconds; the video file creation timestamp is not used as an acquisition timestamp.

## Confirmed empirical mappings

| Indicator | Faster field | Slower status mirror in `405` | Evidence |
|---|---|---|---|
| Check-engine/MIL | `12C B6 & 0x10` | `405 B0 & 0x01` | first engine-start OFF, plus KOEO 20s timeout OFF; 8803/8803 source-fresh mirror matches |
| ABS lamp / bulb check | `1F4 B0 & 0x02` | `405 B1 & 0x01` | yellow ABS icon extinguishes at ~2.15s self-test, 8810/8810 mirror matches |
| Battery / charging warning | `224 B6 & 0x02` | `405 B3 & 0x01` | battery icon OFF at video ~14.43s as CAN bit clears, 8802/8802 mirror matches |
| Oil-pressure warning | `0D4 B2 & 0x80` | `405 B2 & 0x80` **delayed on some starts** | oil-can icon OFF at video ~14.73s, 8804/8810 mirror matches; six fast-clear/slow-still-on startup exceptions |
| Green D / Drive indicator | `188 B2 & 0x80` | none established | lit during startup in P (bulb check), dark after ~2s; do not use alone as D selector |

**IMPORTANT:** A lamp state is not a quantitative sensor. The oil bit is not PSI; battery bit is not alternator volts; ABS bit does not establish wheel speed or ABS system health. The MIL bit turns off ~20s into ignition ON even with RPM zero, so MIL OFF does not mean there are no stored/pending trouble codes. Keep the physical selector from `188 B3`.

## First-start time alignment

`cluster_lamps.log`: RPM becomes nonzero at t=10.753s, MIL clears at 10.763s, battery clears at 11.254s, oil clears at 11.562s. In the video, the same indicator lamps extinguish at approximately 13.93s, 14.43s and 14.73s, respectively. Second key ON at log t~53.2s, and MIL times out at t=73.239s with zero RPM; in video MIL disappears at t~76.433s while battery and oil remain lit.

## Broader validation

Comparison against nine CAN captures yields **0 mismatches for MIL (8,803 aligned 405 frames), ABS (8,810) and battery (8,802)**, excluding samples without a recent source message. The 405 oil bit agrees in **8,804 of 8,810** aligned frames, with six one- or two-refresh startup lag events. Use the faster 0D4 signal as the oil lamp source, and treat 405 as a slower representation. See `verification.json` for per-file counts and all exceptions.

## Still not proven

The captured video shows other startup indicators (SRS, side-airbag-off, key/immobilizer, maintenance wrench). This pair of files does not establish a CAN field for those lamps. `2E4 B0` remains a timed initialization marker of unknown module origin. Do not repeat prior switch tests merely to retest them; seek new bus access or properly synchronized fault-free diagnostic observation if necessary.

Files: `signal_updates.json`, `events.csv`, `video_alignment.json`, `verification.json`.

