# 0.1.0 research publication

First consolidated privacy-reviewed publication for the observed 2003 and 2007 Accord four-cylinder automatic F-CAN profiles.

Includes separate JSON/CSV/DBC maps, all payload-bit regions including raw unknowns, year-specific protocol rules, calibration caveats, a complete 15-group 2007 remaining-signal register, sanitized historical studies and selected aggregate/reference evidence. All 46 original 2003 workbook signal rows are retained as historical source text with current corrections separately documented.

Adds a dependency-free offline decoder/auditor, synthetic regression tests and structural DBC checks. The completed suite has 34 passing tests with cantools 45.0.0, including strict import of both DBCs and 4,144 synthetic third-party decode comparisons. Audits reject empty inputs and close source files reliably. CI validates Python 3.10 and 3.14 with and without the optional importer, and checks release hashes and manifest coverage.

The original publication preparation freshly recounted 1,449,999 recovered 2007 full-CAN frames with 1,389,504 applicable checksum passes and no failures, plus 12,113 separately checked focused 224 packets. Repository completion did not rerun unavailable private captures. See docs/verification.md for exact scope and limitations.

Corrects legacy RPM/speed notes, odometer and fine-distance conventions, raw-versus-normalized fuel scaling, gear7 interpretation, D-lamp bulb check, warning lifecycles, throttle request/feedback distinctions, accessory-bit semantics, speed filtering and partial-network power interpretation.

No original trip logs, absolute odometer readings, capture wall-clock timestamps, route names, account/device identifiers, source media or proprietary software/manuals are included. No vehicle commands were sent. Fuel volume, remaining physical identities and profile generalization retain their stated uncertainty.

Published as a research prerelease in a private GitHub repository. No reuse license is applied. The 15-group 2007 register and the separate 2003 questions remain explicitly open where new independent measurements are needed; no physical identities or calibrations were invented to close them.
