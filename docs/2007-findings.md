# 2007 Accord: current publication register

**Profile:** Honda Accord EX 2.4 L automatic, one research vehicle. Ten observed standard IDs at 500 kbit/s. Byte numbering is zero-based. This is a capture-specific profile, not proof of year-exclusive messages.

## Evidence layers

The baseline, standing checklist, labeled follow-ups, residual audit, body/dimmer test, lamp test, throttle reference, two focused fuel studies, DFCO study, dynamics study and final follow-through are preserved in sanitized research appendices. Later discriminating observations take precedence over earlier speculation. [07-V01 through 07-V13]

For this publication, five recovered raw files were freshly recounted: 1,449,999 frames, 1,389,504 applicable checksums, all passing. The other 60,495 frames are `1F4`, where this checksum is not applicable. Two later focused captures add 12,113 separately checked `224` packets. This does not independently repeat every fit in the historical studies. [PUBLIC-AUDIT]

The earlier v0.5 audit's 52 residual varying bit positions and 376 constant positions are historical masks, not today's count of unknown sensors. Many of those bits were subsequently identified as warning lamps, oil life and body states. The v1.2 and v1.3 frame totals overlap earlier recordings; never add them as independent experiments.

## Signal tables

The [JSON](../data/accord_2007.json), [CSV](../data/accord_2007_signals.csv) and [DBC](../dbc/accord_2007_research.dbc) also include every unmapped region and protocol field. An experimental name below describes observed behavior, not a final OEM semantic identity.

### `0x0A6`: Throttle and fuel-cut related
Nominal broadcast rate: 100 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `FuelCutStatus` | `(B0 >> 1) & 0x1` | bool | high | 07-V11 |
| `ThrottleRequestLikeB2` | `B2` | raw | experimental | 07-V13 |
| `ThrottleFeedbackB3` | `B3` | raw | obd-calibrated | 07-V08 |
| `ThrottleRequestLikeB4` | `B4` | raw | experimental | 07-V13 |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x0C8`: Vehicle motion and distance
Nominal broadcast rate: 100 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `SpeedA` | `BE16(B0:B1) * 0.01` | km/h nominal | high | 07-V13 |
| `SpeedB` | `BE16(B4:B5) * 0.01` | km/h nominal | high | 07-V13 |
| `DistanceTicksRaw` | `B6` | tick | high | 07-DISTANCE |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x0D4`: Meter controls, sender and secondary motion
Nominal broadcast rate: 100 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `LightingMode` | `(B0 >> 0) & 0x3` | code | high | 07-V03 |
| `ParkingBrake` | `(B0 >> 2) & 0x1` | bool | high | 07-V03 |
| `CruiseMain` | `(B0 >> 5) & 0x1` | bool | high | 07-V03 |
| `CruiseButton` | `(B0 >> 6) & 0x3` | code | high | 07-V03 |
| `AccessoryControlCandidate` | `(B2 >> 6) & 0x1` | bool | experimental | 07-V13 |
| `OilWarningStatus` | `(B2 >> 7) & 0x1` | bool | high | 07-V07 |
| `FuelSenderRelatedB3` | `B3` | raw | high-related-raw | 07-V13 |
| `FuelSenderRelatedB4` | `B4` | raw | high-related-raw | 07-V13 |
| `SecondarySpeedRaw` | `BE16(B5:B6)` | raw | high-related-raw | 07-V13 |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x12C`: Engine and status
Nominal broadcast rate: 100 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `CoolantTemperature` | `B0 -40` | degC | high | 07-V01 |
| `IntakeAirTemperature` | `B1 -40` | degC approx | high | 07-V01 |
| `EngineRPM` | `BE16(B4:B5)` | rpm | high | 07-V01 |
| `ServiceBrake` | `(B6 >> 0) & 0x1` | bool | high | 07-V03 |
| `CruiseEngaged` | `(B6 >> 3) & 0x1` | bool | high | 07-V04 |
| `MILStatus` | `(B6 >> 4) & 0x1` | bool | high | 07-V07 |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x188`: Transmission and selector
Nominal broadcast rate: 100 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `ReportedGear` | `B0` | code | high | 07-V03 |
| `TargetGear` | `B1` | code | high | 07-V03 |
| `DIndicatorStatus` | `(B2 >> 7) & 0x1` | bool | high | 07-V07 |
| `SelectorCode` | `B3` | code | high | 07-V03 |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x1F4`: Meter status and odometer
Nominal broadcast rate: 25 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `ABSStartupWarningStatus` | `(B0 >> 1) & 0x1` | bool | high | 07-V07 |
| `WiperMode` | `(B0 >> 3) & 0x3` | code | high | 07-V03 |
| `LeftTurnRequest` | `(B0 >> 5) & 0x1` | bool | high | 07-V03 |
| `RightTurnRequest` | `(B0 >> 6) & 0x1` | bool | high | 07-V03 |
| `DimmerLevelCode` | `(B1 >> 0) & 0x7f` | raw | working-interpretation | 07-V13 |
| `DimmerOverrideCandidate` | `(B1 >> 7) & 0x1` | bool | strong-inference | 07-V13 |
| `OdometerRaw` | `BE24(B3:B5)` | raw odometer count | maintainer-confirmed-scale | 07-ODO |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x20C`: ON-associated state, maintenance and RPM copy
Nominal broadcast rate: 50 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `IgnitionOnAssociated` | `(B0 >> 1) & 0x1` | bool | high | 07-V13 |
| `OilLifePercent` | `B1` | percent | maintainer-confirmed | 07-OILLIFE |
| `EngineRPMCopy` | `BE16(B4:B5)` | rpm | high | 07-V01 |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x224`: Fuel-use counter and engine status
Nominal broadcast rate: 10 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `FuelAccumulatorRaw` | `BE16(B2:B3)` | raw fuel tick | high | 07-V13 |
| `ChargingWarningStatus` | `(B6 >> 1) & 0x1` | bool | high | 07-V07 |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x2E4`: Initialization sentinel
Nominal broadcast rate: 10 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `InitializationSentinelRaw` | `B0` | code | observed-behavior | 07-V13 |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

### `0x405`: Slow status mirrors and body closures
Nominal broadcast rate: 3.333 Hz. Physical transmitting module is not independently established.

| Field | Location and extraction | Unit | Evidence status | Source |
|---|---|---|---|---|
| `MILMirror` | `(B0 >> 0) & 0x1` | bool | high | 07-V07 |
| `ABSWarningMirror` | `(B1 >> 0) & 0x1` | bool | high | 07-V07 |
| `DriverBeltUnbuckledStatus` | `(B2 >> 2) & 0x1` | bool | high | 07-V06 |
| `ParkingBrakeMirror` | `(B2 >> 5) & 0x1` | bool | high | 07-V03 |
| `OilWarningMirror` | `(B2 >> 7) & 0x1` | bool | high | 07-V07 |
| `ChargingWarningMirror` | `(B3 >> 0) & 0x1` | bool | high | 07-V07 |
| `IlluminationActiveCandidate` | `(B3 >> 3) & 0x1` | bool | strong-inference | 07-V03 |
| `FrontLeftDoorOpen` | `(B4 >> 5) & 0x1` | bool | high | 07-V04 |
| `FrontRightDoorOpen` | `(B4 >> 6) & 0x1` | bool | high | 07-V04 |
| `RearLeftDoorOpen` | `(B4 >> 7) & 0x1` | bool | high | 07-V04 |
| `RearRightDoorOpen` | `(B5 >> 0) & 0x1` | bool | high | 07-V04 |
| `TrunkOpen` | `(B5 >> 1) & 0x1` | bool | high | 07-V06 |

Every raw remainder and protocol field is retained in the JSON, CSV and DBC, including constant/unexcited regions.

## Throttle feedback, demand-like channels and fuel cut

`0A6 B3` is the actual-throttle-feedback equivalent calibrated against OBD PID 11 absolute throttle and PID 45 relative throttle. It is not accelerator pedal percentage. The tested range is raw 8 through 208, under parked engine-off holds and warm idle, with transitions excluded. Both stable-fit RMSE values are approximately 0.131 percentage points; response under every on-road load was not calibrated. [07-V08]

B2 and B4 remain separate request-like raw channels. In a labeled engine-off pedal sweep B2 leads B3 by approximately five packets, about 50 ms. During three high-load upshifts B2 stays at 208 while B3 drops to approximately 68 to 71; the feedback dips start about 549 to 619 ms after target-shift requests. Therefore B2 cannot be declared the final actuator command. B4 remains high through those events. [07-V12]

A fixed B2-to-B4 subtraction fails: with B2 fixed at 208, B4 is 199 in 430 stopped-engine standing frames, 188 to 196 in 2,437 running drive-a frames, and 189 to 195 in 353 drive-b frames. Preserve the channels rather than manufacture a pedal gauge. [07-V13]

`0A6 B0 & 02` has high-confidence DFCO interpretation: 21 events and 694 interior fuel-counter samples show zero increments. Ten warm zero-request exits cluster around 1,200 rpm. This is observed exit behavior, not a universal cold/warm entry threshold, a full PCM strategy, or proof that every transient fuel-cut mode has been identified. [07-V11]

## Motion and fuel sender behavior

Let A=`BE16(0C8 B0:B1)` and B=`BE16(0C8 B4:B5)`. Training on drive-a gives `B approximately 1.020582138*A - 0.069633682`. With the coefficients unchanged, 44,994 held-out moving drive-b samples have RMSE 0.442 raw counts and maximum absolute error 1.332. The test range is A greater than 1,000. This supports scaled representations of one motion quantity, not independent wheel speeds. Lower A is the preferred nominal odometer-consistent channel. [07-V13]

`0D4 B5:B6` is better explained by smoothing than by a pure time delay. A first-order 0.281 s smoothing model gives held-out RMSE 4.323 raw counts versus 18.301 for the optimized pure-delay alternative. These empirical coefficients do not recover Honda firmware or establish the consuming subsystem. [07-V13]

`0D4 B3` changes on a roughly 200 ms grid despite its 100 Hz message. All 4,917 examined inter-change intervals shorter than five seconds were within 0.882 ms of an integer multiple of 200 ms. B4 can change in adjacent 10 ms frames. These are output-update observations, not a measurement of internal sensor sampling. The inverse relationship and refueling-associated ranges support a sender-related pair; tank volume is not calibrated. [07-V13]

## Controls and indicators

Lighting, parking brake, selector, wipers, and turn-request extraction follow the separately validated locations listed in the tables. `0D4 B0 & 20` is cruise MAIN, while `B0 & C0` is the button enum `00` none, `40` SET/DECEL, `80` RESUME/ACCEL, `C0` CANCEL. `12C B6 & 08` is engagement. Main, buttons, engagement, actual road speed and stored setpoint are different quantities. No numerical cruise setpoint has been decoded. [07-V03, 07-V04]

The lamp test supports MIL at `12C B6 & 10`, ABS startup indication at `1F4 B0 & 02`, charging warning at `224 B6 & 02`, oil-pressure warning at `0D4 B2 & 80`, and green D indication at `188 B2 & 80`. The D lamp can assert for about two seconds in Park during bulb check. The MIL may clear after approximately 20 seconds with the engine still stopped. Those patterns disprove treating these bits as unconditional selector-D or engine-stopped flags. ABS fault-present behavior was not deliberately induced. [07-V07]

`405` contains slower mirrors and closure states. The oil-warning mirror was delayed at some starts, producing six mismatches in 8,810 fresh-source comparisons. Prefer the fast source for display. Door masks are FL `B4&20`, FR `B4&40`, RL `B4&80`, RR `B5&01`; trunk is `B5&02`. Driver belt status `B2&04` is set for unbuckled in the later parked polarity check. A raw buckle input versus ECU-derived warning, and the chime pattern, remain unseparated. Missing `405` data is not evidence of a closed door or buckled belt. [07-V04, 07-V06, 07-V07]

## Accessory and ignition cautions

`0D4 B2 & 40` remained set while fresh RPM was zero for spans of 7.271, 19.721, 14.202 and 13.942 seconds. The maximum age of the preceding RPM sample was below 8.5 ms. The bit therefore cannot prove compressor rotation or current mechanical accessory load. Request, permission or an electrical clutch command remain possible. [07-V13]

The earlier 43 parked edge comparisons showed mean fuel rates 4.167 versus 2.985 raw ticks/s, about +39.6% when set. However, 39 comparisons came from one standing capture, with roughly 2.4 s windows. This is associated behavior, not 43 independent experiments, an accessory horsepower estimate or a fixed fuel surcharge. Repeating the same unlabeled A/C-button sweep will not settle the physical meaning. [07-V12, 07-V13]

Fresh `20C B0 & 02` indicates an ON-associated state; fresh clear means not ON-associated, with ACC versus OFF unresolved. During a 27.690 s gap in `0D4` traffic, 1,382 `20C` frames continued with this bit clear and no other captured ID transmitting. Bus traffic alone does not mean ignition ON, and silence does not supply a fresh OFF value. [07-V13]

The `2E4 B0=FF` five-packet burst appeared at three initializations, including after a measured 28.058 s gap, and was absent after shorter gaps of 1.938 and 1.327 s. Pre-recording histories of other starts were unknown. This does not identify a module, cold-boot rule, sleep timeout or reliable universal power-state flag. [07-V13]

## Cruise and transmission dynamics

Six engaged intervals totaled 577.293 s. Observed engagement response after SET/RESUME was 159 to 215 ms, cancellation 41 to 48 ms, and a brake-associated cancellation about 20 ms. Cruise engagement can coexist with DFCO. These are observed message timing relationships, not safety guarantees or command latency specifications. [07-V12]

Across 74 clean reported shifts, median status durations were 1.055 s for 1-to-2, 0.975 for 2-to-3, 1.005 for 3-to-4, 0.980 for 4-to-5, 0.700 for 5-to-4, 0.880 for 4-to-3, and 0.860 for 3-to-2. They measure reported status sequences, not clutch torque-transfer duration. A fifth-gear near-rigid band around 21.177 rpm per nominal km/h is an inferred coupling observation, not a decoded torque-converter-clutch bit. [07-V12]

## Remaining scope

Maintenance Minder oil life is settled as `20C B1` by a maintainer/dashboard comparison; do not list it as unknown. The absolute odometer divisor 1.61 and fine counter's 164 ticks per odometer mile are likewise settled within their stated reference convention. `224 B1`, fuel-volume metering, physical sender calibration, pedal/final actuator identity, cruise setpoint, converter/input speed and full power-sleep behavior remain open. See [the complete remaining register](unresolved.md).
