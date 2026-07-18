# External YOLO Test Set

An independent, held-out detection test set used **only** for final evaluation (the
detection leaderboard in the thesis). None of its recordings appear in the detection
or frame-classification datasets, so it measures true out-of-distribution
performance.

## Contents

| Property | Value |
|----------|-------|
| Total images | 362 |
| Total annotated instances | 1,743 |
| Average instances per image | 4.8 |
| Classes | `invigilator`, `normal`, `suspicious_moving` |
| Image resolution | 1280 × 1280 (stretch-resized) |
| Annotation format | COCO JSON |
| Source | Roboflow project `testing-dataset`, version 1 (`test_only`) |
| License | CC BY 4.0 |

> As with the detection set, the COCO file lists a placeholder category at id `0`
> (`normal-y93p`); the real classes are id `1` `invigilator`, id `2` `normal`,
> id `3` `suspicious_moving`.

## Why the priors differ on purpose

This set has a deliberately different class distribution from the training data — a
robustness check rather than an in-distribution split:

| Class | Share here | Share in detection training |
|-------|-----------|------------------------------|
| `invigilator` | 20.4% | 3.2% |
| `normal` | 55.2% | 78.6% |
| `suspicious_moving` | 24.4% | 18.3% |

The average number of objects per image (4.8) is far lower than in the training set
(~11.3), reflecting smaller rooms with less crowding. A detector that has simply
memorised the training prior will tend to under-predict `invigilator` here, which is
exactly what this set is designed to expose.

## Usage

Use this set for **evaluation only** — never for training, validation, or model
selection.

## File naming

Images use meaningful serial names of the form `external_test_{NNNN}.jpg`
(e.g. `external_test_0001.jpg`). These match the `file_name` fields inside
`_annotations.coco.json`. The original Roboflow file names are preserved in
[`name_mapping.csv`](name_mapping.csv).

## Layout after download

```
external_test_set/
├── annotations/
│   └── test/_annotations.coco.json   (in Git)
├── name_mapping.csv                   (in Git)
└── test/   *.jpg                       (from Zenodo)
```
