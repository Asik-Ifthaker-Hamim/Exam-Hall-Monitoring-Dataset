<div align="center">

# Exam-Hall Monitoring Dataset

**Detection, frame-classification, and external test sets for automated
suspicious-behaviour monitoring in examination halls.**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21432043.svg)](https://doi.org/10.5281/zenodo.21432043)
[![Data: Zenodo](https://img.shields.io/badge/data-Zenodo-1682D4.svg)](https://doi.org/10.5281/zenodo.21432043)

Released alongside the undergraduate B.Sc. thesis *"A Dual-Stream YOLO Cascade with
Attention-Guided Lightweight Frame Classification for Real-Time Suspicious Behavior
Detection in Examination Halls"* — Department of Computer Science and Engineering,
International Islamic University Chittagong, 2026.

</div>

> [!IMPORTANT]
> **Embargoed until publication.** This dataset is private until the associated
> paper is published. The images are under embargo on Zenodo; please do not
> redistribute the data or download links before the public release.

> [!WARNING]
> **Human-subjects data.** These images show identifiable people, recorded in real
> examination halls with informed consent. Read
> [`ETHICS_AND_CONSENT.md`](ETHICS_AND_CONSENT.md) **before** using the data. It is
> for research and education only and must never be used to identify, profile, or
> discipline any individual.

---

## Contents

- [Overview](#overview)
- [The three datasets](#the-three-datasets)
- [Repository layout](#repository-layout)
- [Download the images](#download-the-images)
- [Quick start](#quick-start)
- [Class labels](#class-labels)
- [Consent, privacy & ethics](#consent-privacy--ethics)
- [License](#license)
- [Citation](#citation)
- [Authors](#authors)

---

## Overview

This release contains **three complementary, non-overlapping datasets** built from a
single field-collection campaign across 15 classrooms. All footage was captured on a
wall- or ceiling-mounted camera in a CCTV-like configuration, spanning varied room
sizes, seating layouts, and lighting. **No source recording appears in more than one
dataset**, so the external test set is a genuinely out-of-distribution benchmark.

Only the **annotations, labels, and documentation** live in this Git repository
(~5 MB). The **images (~9 GB)** are archived on Zenodo and fetched with a script —
see [Download the images](#download-the-images).

## The three datasets

| # | Dataset | Task | Format | Images | Annotations | Classes |
|:-:|---------|------|:------:|:------:|-------------|---------|
| 1 | [`detection_dataset/`](detection_dataset/) | Object detection | COCO | 2,020 | 22,828 boxes | `invigilator`, `normal`, `suspicious_moving` |
| 2 | [`frame_classification_dataset/`](frame_classification_dataset/) | Scene classification | ImageFolder | 7,772 | per-frame label | `normal`, `suspicious` |
| 3 | [`external_test_set/`](external_test_set/) | Detection (test only) | COCO | 362 | 1,743 boxes | `invigilator`, `normal`, `suspicious_moving` |

Each folder has its own README with full class definitions, the split protocol, and
known caveats. In short:

- **Detection** — every person boxed and labelled; train/valid/test = 1,420 / 397 / 203.
- **Frame classification** — one binary label per frame; a `recording_id` group id in
  `labels.csv` enables leakage-free, group-aware cross-validation.
- **External test set** — held out for detector evaluation only, with a deliberately
  different class prior as a robustness check.

**Annotation quality.** Labels were checked for reliability with Cohen's Kappa
between two independent annotators: **κ = 0.739** (substantial) on the detection
data and **κ = 0.832** (almost-perfect) on the frame-classification data. See each
dataset's README for the mechanism and full figures.

## Repository layout

```
Exam-Hall-Monitoring-Dataset/
├── README.md                      ← you are here
├── LICENSE                        ← CC BY 4.0
├── CITATION.cff / CITATION.bib    ← how to cite
├── CHECKSUMS.txt                  ← SHA-256 of the Zenodo archives
├── ETHICS_AND_CONSENT.md          ← consent, privacy & acceptable use
├── scripts/
│   ├── download_data.py           ← fetch + verify images from Zenodo
│   └── build_release.py           ← (maintainers) rebuild renamed images + labels
├── detection_dataset/
│   ├── README.md
│   ├── annotations/{train,valid,test}/_annotations.coco.json
│   └── name_mapping.csv
├── frame_classification_dataset/
│   ├── README.md
│   ├── labels.csv                 ← filepath, label, recording_id, frame_index
│   └── name_mapping.csv
└── external_test_set/
    ├── README.md
    ├── annotations/test/_annotations.coco.json
    └── name_mapping.csv
```

Image files use meaningful, serially-numbered names that encode their folder —
`detection_train_0001.jpg`, `external_test_0001.jpg`, `normal_00001.jpg`, … — and the
original source names are preserved in each dataset's `name_mapping.csv`.

## Download the images

The images are hosted on Zenodo
([DOI 10.5281/zenodo.21432043](https://doi.org/10.5281/zenodo.21432043)). Clone the
repo and run the download script — it fetches each archive, verifies its SHA-256
checksum, and extracts the images to match the annotations:

```bash
git clone https://github.com/Asik-Ifthaker-Hamim/Exam-Hall-Monitoring-Dataset.git
cd Exam-Hall-Monitoring-Dataset

python scripts/download_data.py --all                  # all three datasets
python scripts/download_data.py frame_classification   # or one at a time
```

> [!NOTE]
> The images are embargoed on Zenodo until the paper is published; the download
> script will only succeed once the files are open. No extra dependencies are
> required — the script uses only the Python standard library.

## Quick start

**Detection / external test (COCO)** — load with `pycocotools`:

```python
from pycocotools.coco import COCO

coco = COCO("detection_dataset/annotations/train/_annotations.coco.json")
img = coco.loadImgs(coco.getImgIds()[0])[0]          # -> {'file_name': 'detection_train_0001.jpg', ...}
anns = coco.loadAnns(coco.getAnnIds(imgIds=img["id"]))
# Real classes are ids 1 (invigilator), 2 (normal), 3 (suspicious_moving);
# id 0 is an empty Roboflow placeholder super-category.
```

**Frame classification** — use `labels.csv` and split **by recording** to avoid leakage:

```python
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

df = pd.read_csv("frame_classification_dataset/labels.csv")
y = (df["label"] == "suspicious").astype(int)
groups = df["recording_id"]                          # keep each recording on one side

for train_idx, test_idx in StratifiedGroupKFold(5, shuffle=True, random_state=42).split(df, y, groups):
    ...  # no recording_id appears in both train and test
```

## Class labels

| Class | Appears in | Meaning |
|-------|-----------|---------|
| `invigilator` | detection, external test | A proctor standing or walking in the hall. |
| `normal` | all three | A seated student with no unusual upper-body motion (frame set: a scene with no suspicious activity). |
| `suspicious_moving` / `suspicious` | all three | A student moving in a way consistent with copying, note-passing, or another rule-breaking act (frame set: a scene containing such activity). |

## Consent, privacy & ethics

Recordings were collected with the **informed consent** of the participating students
via a Google Form describing the study, storage, and withdrawal process, and with the
cooperation of the institution. Anyone who did not consent to being recorded was
**excluded**, and their images were removed before release. Raw video was never
distributed — only the released frames and labels are shared, with no names, IDs, or
other personal identifiers attached.

Full details, including the acceptable-use terms you agree to by downloading, are in
[`ETHICS_AND_CONSENT.md`](ETHICS_AND_CONSENT.md).

## License

Images and annotations are released under the
[**Creative Commons Attribution 4.0 International (CC BY 4.0)**](LICENSE) license —
you may share and adapt the material, including commercially, provided you give
appropriate [credit](#citation) **and** honour the acceptable-use terms in
[`ETHICS_AND_CONSENT.md`](ETHICS_AND_CONSENT.md).

## Citation

Please cite **both** the dataset and the thesis. Ready-to-use entries are in
[`CITATION.bib`](CITATION.bib) (BibTeX) and [`CITATION.cff`](CITATION.cff)
(GitHub's *Cite this repository*).

<p align="justify">
Hamim, A. M. A. I., Mohaimin, A., Ishmum, A. F., As-ad, J., &amp; Khaliluzzaman, M.
(2026). <em>Exam-Hall Monitoring Dataset: Detection, Frame-Classification, and
External Test Sets for Automated Examination-Hall Suspicious-Behaviour
Monitoring</em> [Data set]. Zenodo.
<a href="https://doi.org/10.5281/zenodo.21432043">https://doi.org/10.5281/zenodo.21432043</a>
</p>

## Authors

Department of Computer Science and Engineering, International Islamic University
Chittagong (IIUC), Chittagong, Bangladesh.

- A. M. Asik Ifthaker Hamim
- Abdul Mohaimin
- Al Fahim Ishmum
- Jamil As-ad — *Co-supervisor (Lecturer)*
- Md. Khaliluzzaman — *Supervisor (Associate Professor)*

For questions or **data-removal requests**, please
[open an issue](https://github.com/Asik-Ifthaker-Hamim/Exam-Hall-Monitoring-Dataset/issues/new/choose)
or contact the authors.
