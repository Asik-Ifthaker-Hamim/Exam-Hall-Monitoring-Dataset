# Changelog

All notable changes to this dataset release are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions correspond to
the Zenodo record versions.

## [1.0.0] — 2026-07-04

Initial release.

### Added
- **Detection dataset** — 2,020 images, 22,828 boxes, COCO format, three classes
  (`invigilator`, `normal`, `suspicious_moving`); train/valid/test = 1,420/397/203.
- **Frame-classification dataset** — 7,772 frames from 36 recordings, binary
  `normal`/`suspicious` labels, with a `recording_id` group id in `labels.csv` for
  leakage-free group-aware cross-validation.
- **External YOLO test set** — 362 images, 1,743 boxes, held out for detector
  evaluation only.
- Documentation, per-dataset READMEs, ethics & consent statement, citation files
  (`CITATION.cff`, `CITATION.bib`), and SHA-256 checksums.
- `scripts/download_data.py` (fetch + verify from Zenodo) and
  `scripts/build_release.py` (rebuild renamed images + labels).
- Images archived on Zenodo under DOI
  [10.5281/zenodo.21432043](https://doi.org/10.5281/zenodo.21432043) (embargoed until
  publication).

[1.0.0]: https://doi.org/10.5281/zenodo.21432043
