# Calibration: identity, reference convention and physical accuracy

Finding the bytes, identifying their function, selecting a display convention and measuring physical accuracy are different achievements. This document keeps them separate. Source tags resolve in [provenance](provenance.md).

## Absolute odometer versus incremental distance

For both sample profiles the later maintainer-reported dashboard convention is:

```text
raw_odometer = BE24(1F4 B3:B5)
displayed_miles approximately raw_odometer / 1.61
```

The 2007 live comparison and the later 2003 follow-up are reported confirmations. Actual readings are excluded for privacy. A synthetic example, unrelated to either car, is raw 161,000 yielding 100,000 miles. The exact mile-to-kilometer conversion 1.609344 is not interchangeable with this empirical divisor. Calling the raw quantity exact whole SI kilometers was an earlier overstatement. [03-ODO, 07-ODO]

Incremental distance instead uses `0C8 B6`, modulo 256. Its original 2003 approximate scale is 10 m/tick, supported by the 200-tick road check against a 2.008 km nominal speed integral. The 2007 has 164 fine ticks between complete factory-odometer mile updates in 14 intervals across two drives:

```text
2003 distance_m approximately valid_fine_tick_delta * 10
2007 distance_m = valid_fine_tick_delta * 1609.344 / 164
               = valid_fine_tick_delta * 9.8130731707...
```

The 2007 expression uses the exact length of a mile after the empirical ticks-per-displayed-mile observation. It does not make the car's odometer GPS-accurate. A previous application's 256-ticks-per-mile or 16-bit accumulator rollover is not the wire-level B6 definition. Do not combine counter baselines across missing recordings or resets. [03-V3, 07-DISTANCE]

## Nominal speed channels

The 2003 primary field B at `0C8 B4:B5` uses a nominal raw/100 km/h convention. The earlier OBD-equivalent empirical raw*0.0098 path answers a different question: reproducing the integer OBD speed presentation. Never silently mix the two while integrating distance. [03-V2]

On the 2007, A at `0C8 B0:B1` and B at `B4:B5` both track motion. A is preferred for nominal odometer consistency. Applying raw/100 km/h and integrating the two private drives produced:

| Anonymous capture | Fine-counter km | Integral A km | Integral B km |
|---|---:|---:|---:|
| drive-a | 16.495776 | 16.466006 | 16.804771 |
| drive-b | 8.399991 | 8.392988 | 8.565633 |

A differs by -0.180% and -0.083%; B by +1.873% and +1.972%. Endpoint quantization and filtering remain. No GPS or tire-circumference ground truth is claimed. The affine A-to-B relationship generalizes to held-out data within its tested moving range, but does not identify factory source/consumer roles. [07-V13]

For secondary `0D4 B5:B6`, the fitted 2007 model is:

```text
alpha = exp(-0.01 / 0.281)
z[n] = alpha*z[n-1] + (1-alpha)*speed_B_raw[n]
predicted_secondary_raw = 1.000154636*z[n] - 53.084032
```

The fit uses nominal 10 ms source intervals, aligns to last preceding source at most 30 ms old, excludes the first five seconds and values at or below 1,000 raw. On common samples, smoothing versus pure-delay RMSE is 3.891/16.017 in drive-a and 4.323/18.301 in held-out drive-b. The offset is not valid at standstill. Use the actual observed channel; this model is an explanatory fit, not reconstructed firmware. [07-V13]

## Fuel counts: the factor of two

```text
raw = BE16(224 B2:B3)          # 16-bit, modulo 65536
normalized = raw >> 1        # 15-bit, modulo 32768
```

The raw values are even in checked recordings. A normalized increment represents two raw increments. For the later working factor:

```text
estimated_mL = valid_raw_delta * 0.105585
             = valid_normalized_delta * 0.21117
```

The parameter 0.21117 mL per normalized count is a working scale transferred from the 2003 research/maintainer calibration context. It is **not independently metered for the 2007** in the recovered evidence, not an OEM specification and not a general injector-flow constant. The original 2003 reference work supported an approximate 0.09 to 0.10 mL/raw scale before later working calibration. The old default 0.20 mL/normalized count must not be mistaken for a separate wire encoding. [03-MAP, 03-FUEL, 07-V13]

Drive-a and drive-b together contain 15,236 + 10,000 = 25,236 raw increments, or 12,618 normalized increments. The working factor would give 2,664.543 mL. That number is a **conditional calculation**, not measured 2007 consumption. The separate counter recount does not independently validate gallons or MPG.

Use one ordinarily driven, metered full-to-full interval with complete coverage to test volume calibration. Keep resets and missing trip intervals out of apparent consumption; otherwise a plausible fitted coefficient can conceal lost data. Refill shutoff variability and retained baseline uncertainty should accompany any new coefficient. No special aggressive driving is needed.

For a valid estimated flow `q` in liters/hour and nominal speed `v` in km/h, L/100 km is `100*q/v` only for nonzero v; at idle display L/h, not a divide-by-zero MPG. When q is zero during fuel cut, show a fuel-cut/coasting state rather than a spurious finite MPG. Any economy result inherits both distance and fuel calibration uncertainty.

## Throttle: empirical OBD-equivalent feedback

For **2007 `0A6 B3`**, within the observed raw range 8 to 208:

```text
relative throttle % approximately 0.0980247 + 0.4449886*B3  # OBD PID 45
absolute throttle % approximately 11.541592 + 0.3221345*B3 # OBD PID 11
```

The original fits use 51 stable relative and 53 stable absolute reference samples. Stable RMSE is 0.130923 and 0.130826 percentage points, respectively. The source CSV retains all 123 paired samples and stable/transition labels, allowing the reported stable regressions to be checked without the private raw drive logs. Samples outside the stable set are not silently discarded from the archive. [07-V08]

These ECU-reported percentages are not physical pedal positions. Pedal PIDs 49/4A/4B were unsupported in the reference attempt; manual requests for quarter/half/full pedal were not independently measured percentages. The fit was made with parked engine-off holds and warm idle, not a full loaded actuator calibration. Do not extrapolate or imply more accuracy than byte quantization and the reference timing permit.

B2 and B4 retain request-like names. The original roughly 50 ms derivative lag is a selected-sweep observation, not guaranteed actuator latency. Later state-dependent B4 evidence supersedes the idea that it is merely a fixed-offset copy of B2. [07-V12, 07-V13]

## Fuel sender and dimmer

B3/B4 in `0D4` are sender-related channels. The historical 2003 angle/voltage interpretation and a 2007 inverse regression do not establish a tank-volume curve. The earlier 2007 relationship `B3 approximately 133.642446 - 0.646609*B4` used a 15 ms earlier B4 sample at B3 change events; held-out drive-b RMSE was 0.511 raw. On a later higher-level capture, RMSE rose to 1.360 with +1.307 mean bias. Preserve both actual channels, account for slosh and use settled refill anchors before estimating volume. [03-MAP, 07-V13]

The dimmer is likewise a code, not photometric brightness. On the 2007, `E4` is `80|64`: a high-bit flag plus decimal level 100. Divide-by-255 would conflate the flag with level. The maximum-click/full-brightness interpretation is strongly inferred but does not establish every possible bit state. [07-V06, 07-V13]
