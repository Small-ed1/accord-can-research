# Corrections and precedence

Read current year-specific JSON/docs first, then later focused evidence, then historical appendices. Archived confidence wording and formulas are retained to explain the research path; they do not override this register. No historical DBC is included as a current import target.

| Earlier interpretation | Current disposition | Basis |
|---|---|---|
| RPM at `0D4`, speed at `12C` in informal notes | RPM is `12C B4:B5`; primary motion is `0C8` | OBD-validated 2003 map and 2007 traces |
| `0D4 B3/B4` as longitudinal dynamics | Sender-related raw pair | Refueling context, inverse relation and slower B3 update behavior |
| Raw odometer equals exact whole kilometers | Later displayed-mile convention is raw/1.61 | Maintainer/dashboard follow-ups; actual readings withheld |
| Use 256 ticks per mile from earlier software | Not the wire-level fine-distance calibration | B6 is modulo256; 2003 approximately10m/tick, 2007 164 ticks/displayed mile |
| One fuel count means the same raw value everywhere | Raw BE16 and raw>>1 normalized conventions differ by two | Existing decoder normalization and observed even counters |
| Transferred 2007 gallons/MPG are measured | Volume factor remains provisional | No matching complete metered interval in recovered evidence |
| Gear code7 always means a moving shift, or Reverse | Transition/unsettled status, including some Reverse engagement; code6 is settled Reverse | Labeled stationary selector holds |
| `188 B2&80` always proves selector=D | 2007 green D indicator includes bulb check in Park | Lamp/startup observations |
| Warning candidates A/B/C are generic engine-stopped bits | MIL/ABS/charging statuses have distinct startup lifecycles | Later synchronized lamp test |
| `0D4 B2&40` means a rotating compressor | Control/permission candidate; can be asserted at fresh zero RPM | Long stopped-engine intervals |
| 43 accessory comparisons are independent experiments | 39 came from one standing capture; windows about2.4s | v1.3 qualification of v1.2 evidence |
| Throttle B2 is final actuator command or exact pedal% | Request-like raw channel; remains high through B3 feedback reductions | High-load shift events and absent pedal reference |
| B4 is just B2 minus a constant | State-dependent separate raw information | Fixed-B2 comparisons across engine states |
| Two `0C8` speeds are independent wheel speeds | Closely scaled motion representations | Held-out affine fit |
| Secondary speed is simply delayed | Smoothing fits the tested moving range much better | Held-out model comparison |
| 100Hz sender message means100 independent B3 updates/s | Observed B3 output grid is about5Hz | 4,917 checked inter-change intervals |
| `1F4 B1` is unsigned0..255 optical brightness | Raw/low7 level plus a possible full-brightness flag | E4 split and maximum-click behavior |
| `20C B1` is still unidentified | Maintenance Minder oil life | Maintainer/dashboard confirmation |
| Any CAN traffic means ignitionON | `20C` can continue when fast traffic stops | Partial-network standing interval |
| `2E4 FF` is a universal ignition/cold-boot flag | Conditional initialization burst | Present after one long gap, absent after shorter gaps |
| 52 remaining bits equal52 unsolved physical sensors | Historical residual mask count, substantially superseded | Later warnings/body/oil-life findings |
| `224 B1` is BARO/LTFT/MAP/fuel level | No defensible identity established | Focused studies and counterexamples |

The 2003 oil/charging candidates do not automatically inherit the stronger 2007 lamp confirmation. The earlier 2003 Cruise page does not establish cruise CAN feedback. Constant/unexcited payload regions remain raw; they are not declared OEM-reserved.
