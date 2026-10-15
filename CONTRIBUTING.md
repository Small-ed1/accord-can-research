# Contributing evidence

Use the issue templates to report a decode or correction. Give generic year/engine/transmission/market context, exact CAN ID, zero-based byte/bit extraction, a proposed meaning, confidence, independent reference and known counterexamples. Never upload identifying vehicle or route information.

Distinguish an observed raw change from a validated physical identity, and identity from a calibrated scale. State whether a result is from a labeled action, OBD comparison, held-out regression, later maintainer report, or an implementation assumption. Include negative results and tested ranges. Do not upgrade another model year merely because the byte layout matches.

Keep legacy corrections visible. Add a source tag and changelog entry; update JSON, CSV, documentation and DBC consistently. Run the tests. Preserve each message's complete non-overlapping bit coverage and retain unknown raw regions. Do not rename a candidate to a definitive physical quantity without new evidence.

Use passive observation, existing safely acquired records and ordinary stationary checks. Do not induce faults, manipulate safety systems, operate a computer while driving or send experimental frames onto a road vehicle. This repository does not accept an active vehicle-control path as part of its decoder tools.

Source captures remain separately held. An aggregate result without public raw data must say so. No legal or engineering conclusion follows solely from a checksum pass or signal correlation. No reuse license is applied; see LICENSING.md.
