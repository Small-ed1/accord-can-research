# Sanitized historical source: 03-V1

> **Historical evidence, not the current specification.** This source is retained to show the research path. Later corrections in [the current register](../../docs/corrections.md) take precedence. Source wording such as "confirmed", "production-ready" or "whole kilometers" may have been qualified or superseded. No safety qualification is implied.

> Privacy editing removes identifying readings, source payload examples, capture dates/times, routes, private IDs and paths. Relative experiment timing and quantitative findings are retained where possible. This is not a byte-identical original. References to historical companion files describe the source package; only files in this release manifest are included here.

---

# 2003 Accord CAN decoding :  [date withheld]

**RPM, vehicle speed, coolant temperature, and intake-air temperature are identified and checked against the supplied OBD recordings.** The gear fields and distance counters have strong internal evidence. Their confidence levels are kept separate from the OBD-validated measurements.

Vehicle context comes from the supplied CarStats configuration. These results describe this captured bus; they are not an OEM specification for every 2003 Accord.

## The usable signal map

All CAN IDs below are hexadecimal. **Bytes are numbered B0 through B7**, starting with the first payload byte. `BE16(a,b) = 256*a + b`.

| Signal | CAN ID | Bytes | Decode | Evidence |
|---|---|---|---|---|
| Engine RPM | `0x12C` | B4–B5 | `256*B4 + B5` RPM | 872 OBD comparisons; mean absolute error **0.423 RPM** |
| Coolant temperature | `0x12C` | B0 | `B0 - 40` °C | **227/230 exact**; remaining errors 1–2°C |
| Intake-air temperature | `0x12C` | B1 | approximately `B1 - 40` °C | **93/93 within 1°C**; 52 exact |
| Speed, matched to OBD | `0x0C8` | B4–B5 | `raw = 256*B4 + B5`; continuous estimate `raw*0.0098` km/h | Integer equivalent `floor(raw*49/5000)` matches **454/458** OBD readings exactly |

For mph, divide km/h by `1.609344`. For °F, use `°C*1.8 + 32`.

Both messages broadcast approximately every **10 ms**, or 100 Hz. This is the frame rate; individual temperature measurements change more slowly. The RPM formula already produces RPM: applying the OBD PID's division by four here would be incorrect.

An actual frame from the recording, `12C#[raw payload withheld]`, decodes to 88°C coolant, approximately 43°C intake air, and `0x031A = 794` RPM.

## Why speed has two conversions

`0x0C8` B4–B5 is unmistakably the speed signal, but the OBD speed and the CAN distance signals use different conventions in this recording.

- **OBD-matched speed:** `raw*0.0098` km/h. Applying integer truncation reproduces 454 of 458 PID speed readings exactly. The other four are off by 1 km/h. This coefficient is an empirical calibration, not a manufacturer-supplied definition or a GPS calibration.
- **Native CAN distance convention:** `raw*0.01` km/h. Integrating this gives **8.59551 km**, matching the separate distance counter's **860 ticks**, approximately **8.60 km**. Four complete intervals between odometer-message updates each cover **1.60882–1.61038 km**, approximately one mile, using this convention.

Thus the OBD-matched speed is 2% below the native CAN distance convention, before integer truncation. Do not silently use the two conversions interchangeably. The DBC exports `Speed_OBDScale` using `0.0098`; the CSV files preserve the raw value and both conversions. The precise factory meaning of this difference remains unverified.

The full drive reaches 4,242 RPM. Its largest speed raw value is 9,842: 96.4516 km/h on the OBD-matched continuous scale, or 98.42 km/h on the native distance scale. The largest sampled OBD speed is 96 km/h; OBD sampling is much slower than CAN.

## Additional signals with supporting evidence

These are **inferred mappings**, without an independent OBD gear, odometer, or fuel-quantity reference.

| Signal | Location | Interpretation and limits |
|---|---|---|
| Current gear | `0x188` B0 | `1–5` track forward gears; `0` appears in park; **`7` means shifting/engaging** in this capture |
| Target gear | `0x188` B1 | Changes to the requested forward gear before B0 reports the completed gear; `6` briefly appears while the selector passes R |
| Selector | `0x188` B3 | Strong candidate mapping: `1=P`, `2=R`, `4=N`, `8=D`, `0=transition` |
| Distance counter | `0x0C8` B6 | Modulo-256 counter; accumulate `(new-old)&255`; approximately 0.01 km/tick in the native distance convention |
| Secondary speed | `0x0D4` B5–B6 | Big-endian speed-related value, correlation 0.999900 with the primary speed raw value; exact source and calibration unresolved |
| Odometer-like value | `0x1F4` B3–B5 | Big-endian raw value rises from **[absolute reading withheld] to [absolute reading withheld]**; update spacing tracks one-mile milestones |
| Running accumulator | `0x224` B2–B3 | Big-endian raw value increases while the engine runs, including when stationary; possibly fuel/injection related |

There are **38 runs of current-gear code 7**, totaling 4,297 frames. Every entry into code 7 coincides with a target-gear change. Code 7 occurs during forward upshifts and downshifts; it should not be displayed as reverse. Target code 6 and selector R were observed only briefly during the P–R–N–D sweep, with no reverse driving reference.

The odometer candidate still needs a simultaneous dashboard reading to confirm its absolute units and offset. B2 of that message is always zero, so this recording cannot establish whether it belongs to a wider field. The proposed B3–B5 extraction is provisional.

The `0x224` accumulator is zero in the engine-off capture, rises 544→630 during idle, 908→1136 during the RPM test, and 1458→15388 during the drive. Its relationship to engine activity is established; a conversion to liters or fuel flow is not. The DBC deliberately retains raw counts.

## Counters and checksum

Every captured ID has a two-bit rolling counter:

```python
counter = (data[7] >> 6) & 3
```

Each message ID advances independently through `0,1,2,3`. There are **zero observed counter discontinuities** across all four captures.

For `0x0D4`, `0x12C`, `0x188`, and `0x224`, the low nibble of B7 is a checksum:

```python
expected = (
    -sum((b >> 4) + (b & 0x0F) for b in data[:7])
    - (data[7] >> 4)
) & 0x0F
valid = (data[7] & 0x0F) == expected
```

This passes **576,806 of 576,806 applicable frames**, including the separate engine-off, idle, and RPM-test captures. No CAN-ID contribution is needed for this observed checksum. The low nibble is always zero on `0x0C8` and `0x1F4`; this formula is not claimed for those two IDs.

## Timestamp alignment and validation

CAN timestamps are absolute Unix epoch timestamps. The supplied sync note ties them to UTC−05:00. The OBD logger source identifies `poll_finished_ts`/`ts` as the end-of-poll wall-clock time, with `logged_ts` recorded later.

The comparison uses the latest CAN frame at or before:

```text
OBD poll_finished_ts - 0.090 seconds
```

The 90 ms offset was selected using RPM during an earlier driving interval. It reflects the empirical relationship between OBD reporting time and the CAN signal, and is **only a comparison alignment**. Original CAN timestamps are preserved in every output. It is not a reason to delay a live CAN display.

During the overlap, OBD wall time minus monotonic time varies by only about 93 microseconds, with one system boot ID. There is no evidence of a clock step within that overlap. Median OBD poll duration is 432 ms; using poll start instead of poll completion minus 90 ms produces a worse RPM comparison.

The earlier selection interval is approximately [wall-clock time withheld]–[wall-clock time withheld]; the later validation interval is approximately [wall-clock time withheld]–[wall-clock time withheld]. Both contain vehicle movement and gear changes, preventing the long idle portion from dominating the validation.

| Check | All matched samples | Later active interval |
|---|---|---|
| RPM | 872 samples; MAE 0.423 RPM; 95th-percentile error 3 RPM | 115 samples; MAE **0.730 RPM**; maximum 9 RPM |
| Integer OBD speed equivalent | 454/458 exact; maximum error 1 km/h | **102/106 exact**; maximum error 1 km/h |
| Coolant | 227/230 exact; MAE 0.017°C | 45 samples; MAE 0.044°C |
| Intake air | 93 samples; MAE 0.441°C; maximum 1°C | 18 samples; MAE 0.333°C |

Considering only nonzero OBD speeds, 184/188 comparisons match exactly. In the later active interval, 91/95 nonzero readings match exactly. The remaining errors are still only 1 km/h.

The speed coefficient was chosen from the earlier interval with the RPM-derived timing offset fixed. Quantized OBD values allow a narrow range of equally good coefficients, so `0.0098` should remain labeled an empirical calibration. Temperature identity is well supported, but coolant validation spans only 88–91°C and intake air differs from OBD by up to 1°C.

The recorded OBD response bytes were independently decoded for RPM, speed, coolant, intake air, throttle, engine load, and MAP. They agree with the telemetry's stored physical values, within floating-point precision.

## Capture inventory and quality

| File | Frames | Duration | Local time, [date withheld] |
|---|---:|---:|---|
| `keyon-engine-off.log` | 2,248 | 5.156 s | [wall-clock time withheld]–[wall-clock time withheld] |
| `idle.log` | 8,700 | 19.990 s | [wall-clock time withheld]–[wall-clock time withheld] |
| `rpm-test.log` | 15,229 | 34.987 s | [wall-clock time withheld]–[wall-clock time withheld] |
| `2003-drive-a.log` | 783,216 | 1,799.975 s | [wall-clock time withheld]–[wall-clock time withheld] |
| **Total** | **809,393** | | |

There are six distinct standard CAN IDs, all with eight-byte payloads. The supplied interface snapshot reports 500 kbit/s and listen-only mode. IDs `0x0C8`, `0x0D4`, `0x12C`, and `0x188` run at approximately 100 Hz; `0x1F4` at 25 Hz; `0x224` at 10 Hz. The largest observed same-ID gap is approximately 101 ms on the 10 Hz message.

The OBD archive supplies **2,666 valid sample records** overlapping the drive, from **[wall-clock time withheld] to [wall-clock time withheld]**. It provides no matching OBD reference for the three earlier short CAN captures. Only the [date withheld] telemetry is used for this alignment; older dates are outside the CAN recording period.

The engine-off CAN file ends with 3,088 NUL padding bytes, which are excluded. The [date withheld] OBD file has three malformed JSONL records, also excluded; all are outside the retained overlap. There are no malformed CAN frame lines after excluding the engine-off padding. The before-drive interface snapshot cannot establish error/drop totals for the entire later drive; counter continuity and observed inter-frame gaps are the available in-capture checks.

## What remains unresolved

No defensible direct CAN mapping was established for analog throttle position, MAP, engine load, voltage, ignition advance, fuel trims, or oxygen-sensor readings. Screening bytes, individual bits, nibbles, and adjacent big-endian words mostly produces indirect correlations with RPM or speed. Those are not sufficient to relabel a field as another sensor.

Several status bits, `0x0D4` B3/B4, and parts of `0x1F4`/`0x224` remain raw. Useful next references would be a dashboard odometer reading, explicitly labeled brake/turn/cruise/A/C changes, stable reverse engagement, and a fuel-consumption reference. For CarStats, the validated RPM/speed/temperature fields can form the initial CAN input; the unresolved engine quantities still need their OBD source.

## Files in the package

- `accord_2003_observed.dbc`: importable signal layout for all six messages, with validated, inferred, and raw fields labeled in names/comments. The DBC does not calculate or enforce checksum validity; the CSV exports include that result.
- `signal_map.json`: byte extraction rules, conversion factors, confidence labels, checksum, and counter definitions.
- `decoded_streams/*.csv.gz`: **all 809,393 frames**, split by CAN ID, retaining capture name, original epoch timestamp, payload, decoded fields, counter, and applicable checksum validation.
- `drive_decoded_10hz.csv`: 17,999 convenience snapshots; each CAN message's original source timestamp is included. Values are carried forward only from earlier received frames.
- `obd_can_matched_pairs.csv`: 2,111 comparisons with source line numbers, CAN payloads, timestamps, decoded values, errors, and validation phase. Speed appears twice to show both continuous and integer equivalents.
- `can_obd_validation.png`: RPM, speed, temperature, and gear evidence plots. Plotted CAN traces use the 10 Hz snapshots; metrics use full-rate CAN frames.
- Inventory, screening, summary, and validation JSON files: detailed counts, rejected lines, metrics, and source hashes.
- `analysis/*.py`, `reproduce.py`, and `README.md`: reproducible analysis from the two original archives.

Only physical signals supported by the comparisons are treated as OBD-validated. Gear and distance interpretations remain explicit inferences, and uncalibrated accumulators remain raw.

