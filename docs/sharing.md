# Sharing Accord CAN research

Introduce the observed 2003 and 2007 four-cylinder automatic profiles to people who can use the findings or independently check them. Link the repository and one relevant example, then ask for a specific confirmation or counterexample. These are research profiles from two vehicles, with no reuse license applied.

The initial technical announcement was [published in r/CarHacking](https://www.reddit.com/r/CarHacking/comments/1x6ga82/2003_and_2007_honda_accord_fcan_research_and_dbcs/) on 15 October 2026 with the Original Project flair and the synthetic overview graphic. The versions below remain available for future use where appropriate; avoid reposting the unchanged announcement.

## Technical community announcement draft

**Suggested title:** 2003 and 2007 Honda Accord F-CAN research and DBCs, looking for independent validation

I've published the F-CAN findings from the 2003 and 2007 four-cylinder automatic Accords used while developing CarStats:

https://github.com/Small-ed1/accord-can-research

There are separate DBC, JSON and CSV maps for each observed vehicle, evidence and corrections, and a Python standard-library offline decoder/auditor. Confirmed, inferred and unknown fields stay distinguished.

One useful detail: engine RPM is the big-endian integer at `0x12C B4:B5`, without the OBD-style division by four. The documentation also separates the year-specific checksum and distance conventions, raw versus normalized fuel counts, and throttle feedback from request-like channels.

I'm looking for independent confirmations or counterexamples on another vehicle. For the 2007, the most useful new evidence would be a diagnostic reference for `0x224 B1`, metered validation of fuel-counter volume, or a synchronized reference for the accessory/clutch-control candidate. An anonymous summary with the exact field, vehicle configuration and independent reference would help.

These aren't Honda OEM DBCs or a complete specification for every Accord. The published tools are offline-only, and the repository excludes raw trips and identifying vehicle readings. Please use the issue templates for reviewed summaries. The material is publicly readable; no reuse license has been applied.

## Accord owner community announcement draft

**Suggested title:** CAN signal research for two 2003 and 2007 four-cylinder automatic Accords

I've published the CAN signal research behind my CarStats work on a 2003 and a 2007 four-cylinder automatic Accord:

https://github.com/Small-ed1/accord-can-research

It includes findings for engine RPM, temperatures, motion, selector/status and other observed fields, separate year-specific research maps, and notes explaining what is still uncertain. The DBC files and an offline example are linked near the top of the README.

I'm especially interested in hearing from anyone who has independently checked the same signals on another Accord. A confirmation or counterexample, with generic year/engine/transmission/market details and the reference used, would help establish which findings carry across vehicles. The 2007 fuel-volume scale and `0x224 B1` identity still need independent evidence.

This isn't a tuning package, a replacement for the factory cluster, or a claim that all seventh-generation Accords match these two samples. Please share an anonymous summary rather than VINs, mileage, route information or raw driving logs. No reuse license has been applied.

## Where to share

Start with one relevant community and answer technical questions before expanding to another. These are candidate destinations, not records of submitted posts.

| Audience | Candidate | Fit and posting check |
|---|---|---|
| CAN and vehicle-network researchers | [r/CarHacking](https://www.reddit.com/r/CarHacking/) | Its visible rules allow vehicle-network projects and tools; ordinary project reposts require 90 days, while project updates are exempt. The feed has an Original Project flair. Read the live rules and submission form before posting. |
| Owners of similar Accords | [Drive Accord](https://www.driveaccord.net/) | Seek the relevant seventh-generation section and tailor the owner draft. The forum section and current posting rules could not be verified during preparation; confirm them before submitting. |

The [r/CarHacking rules](https://www.reddit.com/r/CarHacking/) were checked on 15 October 2026. Rules and flair availability can change. A community's general subject fit does not guarantee moderator approval of a particular post. Do not present this research as OEM documentation or as open source.

## Social preview image

The [PNG card](assets/social-preview.png) is installed as the repository's custom social preview. It is 1280 × 640 pixels and under 1 MB. The [editable SVG](assets/accord-can-overview.svg) also appears in the README. It uses a synthetic frame, contains no vehicle photography, and can be rendered with:

```sh
rsvg-convert --output docs/assets/social-preview.png docs/assets/accord-can-overview.svg
```

To replace the repository's link-preview image in GitHub, open Settings → General → Social preview → Edit → Upload an image, choose the PNG, and confirm the result. GitHub documents the image requirements and upload flow in [social-preview guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview). Committing the PNG alone does not set that repository setting. The original `v0.1.0` tag/assets are unchanged; these introduction materials are on `main`.

## Check whether sharing helped

Use [Insights → Traffic](https://github.com/Small-ed1/accord-can-research/graphs/traffic) to compare visitors, clones and referring sites after sharing. GitHub's [traffic view](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository) covers the past 14 days. Note where and when a post was actually submitted; overlapping windows and your own visits make small changes hard to attribute precisely.

After a few days, look for substantive issue reports and independent checks as well as views. Publish a follow-up when new evidence changes a finding, and link the correction. Avoid repeated announcements that add no new information.
