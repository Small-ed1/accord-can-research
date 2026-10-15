# Privacy review and excluded material

## Publication policy

This release publishes findings, uncertainty and selected experimental evidence. It does not publish the owner's vehicle-use history. Vehicle model years, generic trim/engine/transmission context, message layouts, formulas, anonymous capture labels and relevant experiment metrics are retained because they are needed to interpret the work.

## Removed or withheld

Personal names, account handles, contact details, locations/route names, local machine usernames and hostnames, private filesystem paths, connection details, private conversation/file identifiers, absolute odometer readings, wall-clock capture dates/times and original source hashes are removed from the curated outputs where encountered. Identifying filenames are replaced by neutral research aliases; generic test labels may remain. Unknown fields remain documented without invented labels.

All original raw CAN logs and full chronological driving grids are withheld. These can reveal driving patterns even without GPS. Photos, videos, screenshots and original workbook binaries are withheld, avoiding visible plates/VINs, home/route scenery, faces, audio, EXIF data and document-author metadata. Relevant workbook text is re-exported without its binary metadata. No proprietary manual, diagnostic software package, ECU firmware or key/transponder data is bundled.

Raw `1F4` odometer examples and observed values in its B3:B5 byte-audit slots are removed. Merely deleting a printed mileage while preserving those three bytes would still reveal the reading. The canonical DBC preserves the field layout and uses synthetic examples instead of the cars' actual totals.

## What remains intentionally

Relative event intervals, aggregate counts, regression coefficients, controlled stationary OBD pairs, generic status transitions, raw sender/throttle ranges and uncertainty notes remain. These support the technical findings without supplying complete trip traces. The 2003/2007 sample pairing and distinctive research can still be recognizable to someone already familiar with the project. Public account identity, contributor identity and future commits can also create links. This is a reviewed, privacy-reduced publication, not a guarantee of irreversible anonymity.

## Review method

The release was built into a new directory rather than cleaning an existing Git history. Archive members were inspected/selected before copying. The publication scan checks for local paths, user identifiers, private URLs/file IDs, capture epochs and timestamps, raw odometer examples, unexpected media/binaries and known source-specific strings. Human review of the curated documents supplements pattern matching. The original raw inputs stay outside the release directory and ZIP.

The imported ZIP included no `.git` history. Repository creation starts a fresh private history with a project display name and the owner's GitHub no-reply author email; the [publishing guide](../PUBLISHING.md) describes maintenance and releases. Hosting under an identifying account can reveal authorship regardless of file sanitization. Existing public copies or earlier commits, if any, are not removed by creating this repository.

Before public publication, the reachable history, current tracked files, issue text, release assets, commit identities and Actions output were reviewed. Pattern checks found no credential patterns, known private paths, private conversation links or unexpected raw/media files. The source-aware review of the original imported material remains separately recorded in the [privacy report](../evidence/privacy-review.json). The repository, releases, history, issues and Actions logs are public; the owning account and no-reply commit identity remain visible. Pattern checks and document review cannot guarantee anonymity or detect every possible secret.

## Contributor rules

Do not attach an unreviewed driving log, VIN, plate, exact odometer, screenshot/video or personal route. Share an anonymous test summary and the smallest redacted excerpt needed. Recheck bytes, filenames, archive metadata, timestamps and commit author fields. Do not use the synthetic examples to represent observations they did not contain. Keep removed-source metadata and originals in private storage, not in a hidden folder inside a public repository.
