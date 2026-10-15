# 2003 Accord: current publication register

**Profile:** Honda Accord EX, K24A4, automatic. Six observed standard IDs at 500 kbit/s. This profile is independent of the 2007 profile. Byte numbering is zero-based. Source codes resolve in [provenance](provenance.md).

## Evidence and confidence

The original CAN/OBD baseline contains 809,393 frames. Four labeled follow-ups add 158,845, giving 968,238 frames represented by the v3 handoff. Its later injector-reference test is additional supporting evidence with separate coverage, not a reason to silently inflate this total. The baseline reports 576,806 applicable checksum passes; four follow-up logs also passed applicable checks and preserved per-ID rolling sequences. These are **historical reported results**, not a fresh raw-2003 recount in this publication.

RPM was matched to 872 OBD readings with mean absolute error 0.423 rpm. Coolant matched exactly in 227 of 230 comparisons; intake air was within 1 degree C for all 93 comparisons. An empirical speed presentation `floor(raw*49/5000)` matched 454 of 458 OBD speed readings exactly. That presentation is separate from nominal native `raw/100` km/h. [03-V2, 03-V3]

The labeled tests establish service brake, parking brake, lighting mode, full selector, reverse status, wiper modes and left/right turn requests. A/C-related behavior was exercised, but the bit is not a physical-compressor-engagement measurement. The oil and charging indications remain more weakly established on this sample than the later 2007 lamp tests. [03-V3, 03-MAP]

## Signal tables

The tables below contain semantic fields, including qualified candidates. All bit masks, enums, raw remainders and detailed caveats are also in [JSON](../data/accord_2003.json), [CSV](../data/accord_2003_signals.csv) and the [DBC](../dbc/accord_2003_research.dbc).

### `0x0C8`: Vehicle motion and distance
Nominal broadcast rate: 100 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `SpeedB` | `BE16(B4:B5) * 0.01` | km/h nominal | high | 03-V3 |
| `DistanceTicksRaw` | `B6` | tick | high | 03-V3 |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x0D4`: Meter controls, sender and secondary motion
Nominal broadcast rate: 100 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `LightingMode` | `(B0 >> 0) & 0x3` | code | high | 03-V3 |
| `ParkingBrake` | `(B0 >> 2) & 0x1` | bool | high | 03-V3 |
| `AccessoryControlCandidate` | `(B2 >> 6) & 0x1` | bool | experimental | 03-V3 |
| `OilWarningCandidate` | `(B2 >> 7) & 0x1` | bool | candidate | 03-MAP |
| `FuelSenderRelatedB3` | `B3` | raw | high-related-raw | 03-V3 |
| `FuelSenderRelatedB4` | `B4` | raw | high-related-raw | 03-V3 |
| `SecondarySpeedRaw` | `BE16(B5:B6)` | raw | high-related-raw | 03-V3 |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x12C`: Engine and status
Nominal broadcast rate: 100 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `CoolantTemperature` | `B0 -40` | degC | obd-validated | 03-V2 |
| `IntakeAirTemperature` | `B1 -40` | degC approx | obd-validated | 03-V2 |
| `EngineRPM` | `BE16(B4:B5)` | rpm | obd-validated | 03-V2 |
| `ServiceBrake` | `(B6 >> 0) & 0x1` | bool | high | 03-V3 |
| `MILStatus` | `(B6 >> 4) & 0x1` | bool | strong-inference | 03-MAP |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x188`: Transmission and selector
Nominal broadcast rate: 100 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `ReportedGear` | `B0` | code | high | 03-V3 |
| `TargetGear` | `B1` | code | high | 03-V3 |
| `DRangeCandidate` | `(B2 >> 7) & 0x1` | bool | candidate | 03-V3 |
| `SelectorCode` | `B3` | code | high | 03-V3 |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x1F4`: Meter status and odometer
Nominal broadcast rate: 25 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `WiperMode` | `(B0 >> 3) & 0x3` | code | high | 03-V3 |
| `LeftTurnRequest` | `(B0 >> 5) & 0x1` | bool | high | 03-V3 |
| `RightTurnRequest` | `(B0 >> 6) & 0x1` | bool | high | 03-V3 |
| `DimmerRaw` | `B1` | raw | working-interpretation | 03-PATCH |
| `OdometerRaw` | `BE24(B3:B5)` | raw odometer count | maintainer-confirmed-scale | 03-ODO |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x224`: Fuel-use counter and engine status
Nominal broadcast rate: 10 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `FuelAccumulatorRaw` | `BE16(B2:B3)` | raw fuel tick | high | 03-V3 |
| `ChargingWarningCandidate` | `(B6 >> 1) & 0x1` | bool | candidate | 03-MAP |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

## State interpretation

Lighting uses the low two bits of `0D4 B0`: 0 off, 1 parking, 2 low, 3 high. With parking brake applied, the observed combined byte proceeds `04,05,06,07`; the separate parking-brake mask is `04`. These are reported switch/control states, not lamp-current measurements.

`188 B0` reports 0 for Park/Neutral status, 1 through 5 forward gears, 6 settled Reverse, and 7 transition/engaging. `B1` is the target and can change first. `B3` distinguishes the selector: `01=P`, `02=R`, `04=N`, `08=D`, `20=D3`, `40=2`, `80=1`; `00` is a transition/unknown state. The D-associated `B2 & 80` was set in D in the labeled test, but its internal meaning is unresolved on the 2003. It is not proven to be a converter-clutch or shift-interlock signal.

For `1F4 B0`, the ordinary observed base is `04`; wiper contributions are `00` off, `08` intermittent, `10` slow and `18` fast/manual-up. Left adds `20` and right adds `40`. Mask the components instead of decoding the whole byte by a short lookup table. Mist/pull-back and intermittent delay were not independently represented. Hazards did not produce a separately established code; `60` must not be invented as a hazard state.

## Later qualifications to the September handoff

The earliest odometer description called `1F4 B3:B5` whole kilometers. A later maintainer/dashboard report supports division by **1.61** for displayed miles; the absolute observation is withheld. This publication retains raw in the DBC and marks the conversion's provenance. The older v5 software review still had an odometer mismatch and predates that follow-up. Neither exact 1.609344 substitution nor a legacy software 256-ticks-per-mile setting should override the observed convention. [03-ODO]

The fine-distance field is a separate 8-bit counter. The original road test recorded 200 ticks and a nominal speed integral of 2.008 km, supporting approximately 10 m/tick. This is not a 16-bit counter and must not inherit an application accumulator's rollover size. A freshly metered/GPS validation was not performed here. [03-V3]

Later software implemented ordinary dimmer values around 0 through 99 with special `E4` full-bright handling. That is an implementation/source-history update to the older raw-only B1 description, not a newly instrumented optical calibration. The 2003 DBC deliberately retains the complete byte. [03-PATCH]

The historical fuel-sender interpretation associates B3 with an angle-like gauge quantity and approximates B4 volts with `5*B4/255`. The manual reference points and inverse behavior support that hypothesis, but there is no paired electrical calibration or tank-shape curve in this public evidence. Accordingly, the canonical files preserve both as raw sender-related channels. Never equate B3 directly with tank percent. [03-MAP]

## Fuel and secondary speed

`224 B2:B3` is a fuel-use accumulator, even-valued in the checked studies. It responds to load, tracks injector-duration reference behavior, and can flatten during overrun fuel cut. Normalizing by a right shift changes the numerical volume factor by two. Earlier estimates around 0.09 to 0.10 mL per raw count and an initial software default of 0.20 mL per normalized count are historical settings, not separate simultaneous scales. The later working value is approximately 0.21117 mL per normalized count; a matching 2007 metered interval is still absent. See [calibration](calibration.md). [03-FUEL, 03-MAP]

The `0D4 B5:B6` speed-related channel lagged the primary in the fuel-road test by about 0.26 s at best alignment, with median aligned bias around -0.78 km/h. Its exact source/filter remains unestablished for the 2003. The later 2007 fitted filter must not be asserted as this vehicle's recovered algorithm. [03-MAP]

## What was not found

No clean independent rear-defrost, recirculation or cruise-MAIN status was recovered in the labeled 2003 six-ID tests. A software Cruise page does not establish CAN engagement feedback. Throttle position, MAP, calculated load, voltage, ignition advance, fuel trims and oxygen/A-F values were not defensibly mapped in this six-ID capture set. They may require diagnostics, a different network, or local measurements; this is an absence of a decode, not proof of universal absence.

`224 B1`, the precise D-associated flag meaning, a rare `1F4 B2=04` transient, and physical fuel-sender/volume scales remain qualified or unresolved. Preserve all raw regions. The [sanitized 46-row original workbook map](../archive/2003/workbook/signal-map.csv) retains the historical inventory without silently rewriting its claims.
