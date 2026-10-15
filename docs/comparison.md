# 2003 versus 2007: observed samples

These are two sample profiles, not a universal production-change list. Engine, options, market, module versions and tapping location could affect the inventory. No unsupported year-exclusive claim follows from an ID being absent in one capture.

| Area | 2003 observation | 2007 observation | Implementation consequence |
|---|---|---|---|
| Inventory | Six IDs | Ten IDs, adding `0A6`, `20C`, `2E4`, `405` | Select an explicit profile; do not guess every intermediate year. |
| RPM and temperatures | `12C`, directly OBD validated in original studies | Same locations supported by later traces; RPM also in `20C` | Do not divide CAN RPM by four or count the copy as another sensor. |
| Primary motion | `0C8 B4:B5` nominal speed; B0:B3 zero | Lower A at B0:B1 plus higher B at B4:B5 | Prefer lower A for 2007 odometer-consistent nominal display. |
| `0C8` integrity | No established nibble checksum | Nibble checksum validated | A shared blanket checksum rule rejects valid 2003 data. |
| Fine distance | Historical approximately 10 m/tick | 164 ticks per factory odometer mile | Constants are profile-specific; the counter itself is 8-bit. |
| Absolute odometer | Later maintainer report supports raw/1.61 miles | Live maintainer/dashboard comparison supports raw/1.61 miles | Keep raw and reference convention separate from physical kilometers. |
| Fuel accumulator | Even BE16, normalized raw>>1; later working factor | Same count convention; transferred volume factor not metered here | Factor of two is an encoding issue; volume calibration is separate. |
| Analog throttle | Not decoded in six-ID sample | `0A6 B3` OBD-equivalent feedback, B2/B4 request-like | No pedal-percent claim; keep empirical range limits. |
| DFCO | Fuel accumulator flattens in overrun | Dedicated `0A6 B0&02` strongly supported | Do not backport the 2007 bit to an absent ID. |
| Cruise | No clean MAIN decode from labeled test; no confirmed engagement field | MAIN, button enum and engagement supported | An earlier Cruise UI does not prove a 2003 CAN signal. |
| `188 B2&80` | D-associated candidate | Green D indication including bulb check in Park | Do not infer selector solely from this bit. |
| Oil/charging lamps | Lifecycle-based candidates | Synchronized lamp test strengthens identities, with slow mirrors | Confidence differs by year. |
| Doors/belt/trunk | Not independently decoded here | Closure/belt status in `405` | Gate freshness; absent frames do not mean closed/buckled. |
| Dimmer | Later software handles ordinary values and E4 specially | Low7 level plus high-bit full-bright override candidate | Keep raw; full-byte/255 is wrong for E4. |
| Maintenance Minder | No mapped oil-life field in sample | `20C B1`, dashboard-confirmed | Oil life is not a remaining mystery. |
| Power state | No full power-sleep model established | `20C` can outlive fast traffic; B0&02 is ON-associated | Neither traffic nor silence supplies a complete ACC/OFF state machine. |
| Initialization | No matching extra-ID finding | Conditional five-frame `2E4 B0=FF` burst | Not a universal ignition flag or measured sleep timeout. |

The shared layout of a field does not transfer every later semantic claim or calibration backward. Refer to the year-specific [2003](2003-findings.md) and [2007](2007-findings.md) confidence records. Historical side-by-side material is retained for traceability under [archive](../archive/README.md), but this comparison takes precedence.
