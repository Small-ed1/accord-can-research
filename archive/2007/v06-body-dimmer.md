# Sanitized historical source: 07-V06

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# 2007 Accord: body-control and dimmer capture, revision 0.6

## Result

One new high-confidence body-state field, one resolved seatbelt polarity, and a materially improved but partly provisional dimmer interpretation.

Source: `raw.log`, SHA-256 `[original source hash withheld]`. All byte indexes below are zero-based.
This is an offline evidence update. No vehicle messages were transmitted and no CarStats software was installed.

## Capture audit

The log contains **158,096 frames**, **10 CAN IDs**, and **264.178055 seconds** of recording.
Recorded local time, from file timestamps: **[date withheld], [wall-clock time withheld] to [wall-clock time withheld] [timezone withheld]**.

All 151,492 applicable Honda payload checksums pass. The 6,604 frames of 0x1F4 are excluded from that checksum formula.
There are no malformed lines, backwards timestamps or observed modulo-four counter discontinuities. This is not a mathematical guarantee that no frames were ever lost.
A separate streaming parser independently verified every frame count, payload checksum, counter sequence and key transition sequence.

The existing speed field stays zero, the fine-distance byte stays 0x49, and the selector stays in its established Park encoding.
RPM stays between 772 and 825.

## 1. New trunk-open field

**0x405 B5 & 0x02: set = trunk open; clear = closed.**

| Elapsed seconds | Observed transition | Raw-log line |
|---:|---|---:|
| 16.425669 | Closed to open | 9,832 |
| 25.726172 | Open to closed | 15,401 |
| 32.625156 | Closed to open | 19,530 |
| 40.124704 | Open to closed | 24,017 |

These are two distinct open/close cycles, matching the requested trunk sequence and the user's report.
The open spans are approximately 9.301 and 7.500 seconds at observed frame times.
B5 has only 0x00 and 0x02 in this capture: 824 and 56 frames respectively.
The driver's door remains separately reported open during both cycles, then closes at 46.124530 seconds.
The rear-right door's already-known B5 & 0x01 does not change.

This bit was constant zero in all six captures audited by v0.5.
The new raw recording reveals it because the whole payload was preserved.
Confidence is high for the observed physical function and polarity; the originating module is not identified.
Read only fresh status messages. Missing traffic must not imply that the trunk is closed.

## 2. Driver seatbelt polarity

**0x405 B2 & 0x04: clear when buckled; set when unbuckled in this capture.**

The user explicitly started buckled and then removed the belt.
The first 0x405 frame at 0.226339 seconds has the bit clear (raw-log line 139).
It becomes set at **8.626021 seconds** (line 5,165) and stays set to the end.
The driver-door bit then sets at 11.326011 seconds, matching the reported action order.

The underlying field was already associated with the driver's seatbelt.
This new initial-state annotation resolves its observed polarity.
It does not distinguish a direct buckle-switch message from an ECU-derived warning/status signal or establish every chime behavior.

## 3. Dimmer with exterior lights on

The lighting enum enters parking at 234.978516 seconds and low beams at 234.988334.
The illumination-active bit follows at 235.118777 seconds.

The dimmer byte is **0x1F4 B1**:

| Observed phase | Elapsed start | Raw byte | Low seven bits | Bit 7 |
|---|---:|---:|---:|---:|
| Exterior lights off | 0.025898 | 100 / 0x64 | 100 | 0 |
| Lights on, initial setting | 234.978751 | 77 / 0x4D | 77 | 0 |
| Minimum plateau | 240.098218 | 24 / 0x18 | 24 | 0 |
| Middle plateau | 248.978136 | 48 / 0x30 | 48 | 0 |
| Maximum plateau | 255.138398 | 228 / 0xE4 | 100 | 1 |

There are 41 byte transitions and 35 distinct raw values.
The minimum, middle and maximum plateaus last about 8.000, 5.840 and 9.000 seconds at native 0x1F4 frame times.
The final byte **0xE4 = 0x80 | 0x64**, suggesting a low-seven-bit level code plus a maximum-brightness/override flag.

Working interpretation:

```python
dimmer_level_code = payload_1f4[1] & 0x7F
dimmer_maximum_override_candidate = bool(payload_1f4[1] & 0x80)
```

The level is a raw code, not a measured percentage of light output.
24 is the observed minimum of this particular sweep, not a universal calibrated endpoint.
The high bit changes once, at the last maximum position, and remains set until recording ends.
Its exact meaning, such as a detent versus override request, remains a candidate rather than a fully closed decode.
Do not treat the full raw byte as a 0..255 brightness percentage.

## 4. Other actions and unresolved fields

Horn, HVAC temperature, vent modes, windows and moonroof are recorded as completed physical tests in the user's order.
Window order is FL, FR, RR, RL.
The roughly ten-second spacing is not a set of precise independent timestamps.
No exact time is assigned to an individual action that lacks its own observable marker.

No additional independently identifiable status field for these controls emerges from the payload scan.
This conclusion is limited to this recording and its ten captured message IDs; it does not prove that every network or diagnostic response lacks those states.

0x0D4 B2 is **0x40 in all 26,419 frames**.
Consequently the previous compressor/accessory candidate provides no new transition evidence for the reported HVAC changes.
0x20C B1 remains 0x4D (77); 0x224 B1 remains 0xF3 (243). Their meanings remain unknown.
The sender-like 0x0D4 B3/B4 continue to fluctuate. Those fluctuations are not relabeled as horn or window commands.

## 5. Scope of the scan and monitor limitation

Every byte of all ten IDs was inspected, including bits that were constant in v0.5 and fields excluded from its novel-field search.
With the old exclusion masks applied, this capture's changing residuals are the already-tracked B3/B4 analogue regions plus the new trunk bit.
The dimmer was separately inspected because the old inventory excluded the whole byte as an already-tracked field.

The earlier targeted live command omits **0x405 B5** and **0x1F4 B1**.
It would therefore miss the trunk finding and dimmer sweep even with its corrected input parser.
That was a limited watchlist, not an exhaustive unknown-bit monitor.
The unfiltered raw recording preserved both findings; no repeat of this action sequence is required.

## 6. Files

- `capture_audit.json`: source identity, counts and independent verification.
- `signal_updates.json`: field expressions, confidence, transitions and limitations.
- `action_inventory.json`: user-reported order and observed CAN timing anchors.
- `all_byte_audit.json`: all 80 byte positions, variation and previous-constant comparisons.
- `all_nonprotocol_change_events.json`: every B0..B6 byte-change event with elapsed time and raw-log line.
- `unchanged_candidates.json`: unchanged fields and negative/inconclusive results.

The original raw log is unchanged and is not duplicated inside this evidence archive.

