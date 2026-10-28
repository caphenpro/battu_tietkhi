# Changelog

Notable changes to `battu-tietkhi` are documented here.

## 1.2.3 — 2026-10-28

### Fixed
- Correct the solar-term time estimate near the start/end of the Gregorian year, including Lập Xuân (315°) and Đông Chí (270°).

### Tests and release process
- Add regression tests for precise lunar months, leap months, and the special 2033 calendar.
- Run unit tests across Python 3.9–3.13 before building a release.
- Validate the source distribution and wheel with `twine check`.
- Verify the GitHub release tag matches the package version before publishing to PyPI.
