# Source register and attribution

Source tags identify evidence editions, not additional independent datasets. Archive files are privacy-edited transcriptions; their original calendar dates, private filenames, identifying readings and original-source hashes are not published. Later current definitions override earlier source wording. Publication date is 15 October 2026.

## 2003 sources

| Tag | Source and scope | Public representation |
|---|---|---|
|03-V1|Original 809,393-frame CAN/OBD baseline report|[Baseline narrative](../archive/2003/v1-baseline.md)|
|03-V2|Consolidated deeper baseline interpretation, confidence and negative results|[v2 narrative](../archive/2003/v2-baseline-followup.md)|
|03-V3|Four labeled follow-ups, controls/selector/reverse/fuel, combined 968,238-frame handoff|[v3 narrative](../archive/2003/v3-labeled-findings.md)|
|03-MAP|Full mapping workbook:46 signal rows, byte layouts, enums, warning candidates, fuel/protocol/source notes|[All nine sheets](../archive/2003/workbook/all-sheets.json), separate CSVs in the same directory|
|03-PATCH|Later API/scanner implementation reference; ordinary dimmer 0..99 and special E4 handling|Editorial description in[current 2003 findings](2003-findings.md); original application patch not distributed|
|03-FUEL|Cumulative-fuel implementation normalizes BE16 by right-shifting one bit; historical default 0.20 mL/normalized count and later working factor near 0.21117|[Calibration history](calibration.md); original application patch not distributed|
|03-ODO|Later maintainer/dashboard follow-up after the earlier software review, supporting raw/1.61 miles|Reported confirmation, absolute example withheld; not a new public reference experiment|

The older v5 application review documented an odometer mismatch before the later clarification. It is not treated as a current signal specification. A later driving-summary report used a maintainer-supplied working fuel factor near 0.211 mL/normalized count; that use itself was not an independent fuel-volume experiment. General CarStats UI builds, installation history and unrelated vehicle maintenance are outside this CAN-findings publication.

## 2007 sources

| Tag | Evidence edition | Public narrative |
|---|---|---|
|07-V01|Initial drive baseline, core messages, initial scale limits|[v0.1](../archive/2007/v01-baseline.md)|
|07-V02|Standing sequence, Reverse6, resets and standby traffic|[v0.2](../archive/2007/v02-standing.md)|
|07-V03|Recovered labeled checklist, controls, button enum, ordered stationary actions|[v0.3](../archive/2007/v03-labeled-controls.md)|
|07-V04|Four follow-ups: door positions, MAX-A/C, startup and second drive|[v0.4](../archive/2007/v04-followups.md)|
|07-V05|Six-log residual audit, historical 80-byte masks, startup candidates and mirrors|[v0.5](../archive/2007/v05-residual-audit.md)|
|07-V06|Body/dimmer capture, trunk, belt polarity, maximum-brightness behavior|[v0.6](../archive/2007/v06-body-dimmer.md)|
|07-V07|Synchronized cluster-lamp interpretation and mirror qualifications|[v0.7](../archive/2007/v07-lamp-identities.md)|
|07-V08|Parked throttle OBD-reference calibration and stable/transition pairs|[v0.8](../archive/2007/v08-throttle-reference.md)|
|07-V09|First focused 224capture and B1 transition|[v0.9](../archive/2007/v09-focused-fuel-field.md)|
|07-V10|Second focused 224capture and cross-reference exclusions|[v1.0](../archive/2007/v10-focused-comparison.md)|
|07-V11|DFCO events, fuel-counter alignment and observed exit behavior|[v1.1](../archive/2007/v11-fuel-cut.md)|
|07-V12|Cruise, shift/coupling, throttle intervention and accessory associations|[v1.2](../archive/2007/v12-dynamics.md)|
|07-REGISTER|Full 15-group register before final follow-through|[Pre-v1.3 register](../archive/2007/remaining-register-before-v13.md)|
|07-V13|Final follow-through, held-out speed/filter checks, sender cadence and stopped-engine accessory counterexamples|[v1.3](../archive/2007/v13-followthrough.md)|
|07-ODO|Maintainer live dashboard comparison supporting divisor 1.61|Reported in07-REGISTER; identifying sample withheld|
|07-DISTANCE|164 fine ticks per factory odometer mile in 14 complete intervals across two drives|07-REGISTER and current calibration; absolute endpoints withheld|
|07-OILLIFE|Maintainer/dashboard identification of 20C B1 as Maintenance Minder oil life|07-REGISTER and current maps|
|PUBLIC-AUDIT|New publication-time raw-log integrity recount and focused 224checks|[Aggregate audit](../evidence/independent_raw_audit.json), [focused audit](../evidence/independent_224_audit.json)|

The [evidence edition manifest](../evidence/source-editions.json) maps selected public aggregate/reference files to source tags. The [release manifest](../MANIFEST.sha256) hashes only actual public files. Withheld originals are not recoverable from those hashes and are not included in a nested archive.

## External references

The original 2003 workbook cites Honda service-information material, including a multiplex data list, charging circuit, gauge circuit and navigation/trip-computer description. Those documents supplied architectural context and named physical functions; they did not publish the CAN byte positions claimed by this project. Their links are retained in the[historical source sheet](../archive/2003/workbook/evidence-sources.csv). No manual page or illustration is redistributed.

The 2007 v1.3 report cites the Accord Sedan owner's manual, printed page 71, for maximum-click cancellation of reduced night brightness. This is physical-behavior context, not manufacturer confirmation of 1F4 B1 bit7. The CAN interpretation remains strongly inferred from the capture, and this preparation did not repeat a manual-to-vehicle measurement.

The new tooling/documentation references official technical documentation:

*Linux SocketCAN:* https://docs.kernel.org/networking/can.html

*cantools DBC/database API:* https://cantools.readthedocs.io/en/latest/

*GitHub CLI repository creation:* https://cli.github.com/manual/gh_repo_create

External documentation describes tools or physical functions; all CAN locations, mappings and confidence decisions here remain project research claims. No Honda affiliation or endorsement is implied.
