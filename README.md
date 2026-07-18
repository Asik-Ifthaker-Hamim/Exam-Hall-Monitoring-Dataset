# Exam-Hall Monitoring Dataset

A dataset for **automated suspicious-behaviour monitoring in examination halls**,
released alongside the undergraduate thesis *"A Dual-Stream YOLO Cascade with
Attention-Guided Lightweight Frame Classification for Real-Time Suspicious
Behavior Detection in Examination Halls"* (Department of Computer Science and
Engineering, International Islamic University Chittagong, 2026).

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21432043.svg)](https://doi.org/10.5281/zenodo.21432043)

> **Private / embargoed.** This dataset is kept **private until the associated paper
> is published.** Do not redistribute the data or the download links before the
> public release. The Zenodo archive should be created under an embargo (or as a
> restricted record) and opened only on publication.

> **Human subjects notice.** These images were recorded in real university
> examination halls with the informed consent of the students shown. Please read
> [`ETHICS_AND_CONSENT.md`](ETHICS_AND_CONSENT.md) **before** downloading or using
> the data. The dataset is provided for research and education only and must not be
> used to identify, profile, or discipline any individual.

---

## Overview

The release contains **three complementary, non-overlapping datasets** built from a
single field-collection campaign in 15 classrooms, all captured on a wall/ceiling
mounted iPhone 15 in a CCTV-like configuration. No source recording appears in more
than one dataset, so the external test set is a genuinely out-of-distribution
benchmark.

| # | Dataset | Task | Format | Images / Frames | Annotations | Classes |
|---|---------|------|--------|-----------------|-------------|---------|
| 1 | [`detection_dataset/`](detection_dataset/) | Object detection | COCO | 2,020 | 22,828 boxes | `invigilator`, `normal`, `suspicious_moving` |
| 2 | [`frame_classification_dataset/`](frame_classification_dataset/) | Frame (scene) classification | ImageFolder | 7,772 | per-frame label | `normal`, `suspicious` |
| 3 | [`external_test_set/`](external_test_set/) | Detection — held-out test only | COCO | 362 | 1,743 boxes | `invigilator`, `normal`, `suspicious_moving` |

Each dataset has its own README with the full class definitions, split protocol,
and known caveats.

## Repository layout

```
exam-hall-monitoring-dataset/
├── README.md                      # this file
├── LICENSE                        # CC BY 4.0
├── CITATION.cff                   # machine-readable citation (GitHub "Cite this repository")
├── CITATION.bib                   # BibTeX for the dataset and the thesis
├── ETHICS_AND_CONSENT.md          # consent, privacy, and acceptable-use statement
├── scripts/
│   ├── download_data.py           # fetch + verify the image archives from Zenodo
│   └── build_release.py           # (maintainers) rebuild renamed images + labels
├── detection_dataset/
│   ├── README.md
│   ├── annotations/{train,valid,test}/_annotations.coco.json
│   └── name_mapping.csv           # original Roboflow name -> new serial name
├── frame_classification_dataset/
│   ├── README.md
│   ├── labels.csv                 # filepath, label, recording_id (group id), frame_index
│   └── name_mapping.csv           # original recording-prefixed name -> new serial name
└── external_test_set/
    ├── README.md
    ├── annotations/test/_annotations.coco.json
    └── name_mapping.csv
```

Image files use meaningful, serially-numbered names that encode their folder
(`detection_train_0001.jpg`, `external_test_0001.jpg`, `normal_00001.jpg`, …); the
original source names are preserved in each dataset's `name_mapping.csv`.

**Only the labels/annotations live in this Git repository** (they are small and
benefit from version control). The image files are large (~9 GB total) and are
archived separately on Zenodo — see below.

## Downloading the data

The image files are hosted on Zenodo, which mints a permanent DOI for citation.
After cloning this repository, run:

```bash
python scripts/download_data.py --all            # all three datasets
python scripts/download_data.py frame_classification   # or one at a time
```

The script downloads the per-dataset archives, verifies their SHA-256 checksums,
and extracts the images so that the folder layout matches the annotations in this
repo. See [`scripts/download_data.py`](scripts/download_data.py) for the Zenodo
record configuration.

> **Maintainer:** set the Zenodo record ID and file checksums at the top of
> `scripts/download_data.py` and update the DOI badge above once the archive is
> published. SHA-256 sums for the built archives are in
> [`CHECKSUMS.txt`](CHECKSUMS.txt).

### For maintainers: rebuilding the archives

The image archives uploaded to Zenodo are produced by
[`scripts/build_release.py`](scripts/build_release.py) from the raw source data. It
renames every image to its serial name, rewrites the COCO annotations and
`labels.csv` to match, and writes three zips:
`detection_dataset_images.zip`, `frame_classification_images.zip`, and
`external_test_set_images.zip`. Upload those three files to Zenodo (as an
**embargoed / restricted** record until the paper is published).

## Class labels at a glance

| Class | Where | Meaning |
|-------|-------|---------|
| `invigilator` | detection, external test | A proctor standing or walking in the hall. |
| `normal` | all three | A seated student showing no unusual upper-body motion (frame set: a scene with no suspicious activity). |
| `suspicious_moving` / `suspicious` | all three | A student visibly moving in a way consistent with copying, note-passing, or another rule-breaking act (frame set: a scene containing such activity). |

## Consent, privacy, and acceptable use

Recordings were collected with the informed consent of over 200 students via a
Google Form describing the study, storage, and withdrawal process, and with the
cooperation of the institution. Raw video was never distributed; only the released
frames and their labels are shared. The full statement — including the acceptable-use
conditions you agree to by downloading — is in
[`ETHICS_AND_CONSENT.md`](ETHICS_AND_CONSENT.md).

## License

All images and annotations are released under the
[**Creative Commons Attribution 4.0 International (CC BY 4.0)**](LICENSE) license.
You may share and adapt the material for any purpose, including commercially,
provided you give appropriate credit (see [Citation](#citation)) **and** comply
with the acceptable-use terms in `ETHICS_AND_CONSENT.md`.

## Citation

If you use this dataset, please cite both the dataset and the thesis. BibTeX
entries are in [`CITATION.bib`](CITATION.bib); a machine-readable version is in
[`CITATION.cff`](CITATION.cff).

```
Hamim, A. M. A. I., Mohaimin, A., Ishmum, A. F., As-ad, J., & Khaliluzzaman, M.
(2026). Exam-Hall Monitoring Dataset: detection, frame-classification, and
external test sets for automated examination-hall suspicious-behaviour
monitoring [Data set]. International Islamic University Chittagong.
```

## Authors and contact

- A. M. Asik Ifthaker Hamim (C221012)
- Abdul Mohaimin (C221199)
- Al Fahim Ishmum (C221031)
- Jamil As-ad (Co-supervisor, Lecturer)
- Md. Khaliluzzaman (Supervisor, Associate Professor)

Produced in the Department of Computer Science and Engineering, International
Islamic University Chittagong, Chittagong, Bangladesh.

For questions or data-removal requests, please open an issue or contact the
authors.
