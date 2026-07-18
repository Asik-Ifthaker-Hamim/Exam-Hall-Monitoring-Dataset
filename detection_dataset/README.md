# Detection Dataset

Bounding-box object-detection dataset used to train the YOLO-family detectors
(Approach A in the thesis). Every person in each frame is annotated with one of
three behaviour classes.

## Contents

| Property | Value |
|----------|-------|
| Total images | 2,020 |
| Total annotated instances | 22,828 |
| Classes | `invigilator`, `normal`, `suspicious_moving` |
| Image resolution | 1280 × 1280 (stretch-resized) |
| Annotation format | COCO JSON (one file per split) |
| Dataset-level augmentation | None |
| Splits (train / valid / test) | 1,420 / 397 / 203 |
| Instances (train / valid / test) | 16,047 / 4,486 / 2,295 |
| Source | Roboflow project `real-time-monitoring-system-3`, version 3 |
| License | CC BY 4.0 |

> **Note on COCO categories.** The exported COCO files list four categories. Id `0`
> (`no_cheating-TfLz`) is a Roboflow super-category placeholder and carries no
> annotations. The three real classes are id `1` `invigilator`, id `2` `normal`,
> and id `3` `suspicious_moving`.

## Class definitions

| Class | Annotation rule |
|-------|-----------------|
| `invigilator` | A proctor who is standing or walking in the hall. |
| `normal` | A student who is seated and is not showing unusual upper-body motion. |
| `suspicious_moving` | A student visibly moving in a way consistent with copying, note-passing, or another rule-breaking act. |

## Annotation & quality

Frames were sliced from the source recordings and annotated by human annotators in
**Roboflow** (project `real-time-monitoring-system`, version 3): a bounding box was
drawn around every person on screen and assigned one of the three behaviour classes
using the rules in [Class definitions](#class-definitions).

**Inter-annotator agreement.** Annotation reliability was measured with Cohen's
Kappa, κ = (P_o − P_e) / (1 − P_e), where P_o is the observed agreement between two
annotators and P_e is the agreement expected by chance. A random subset of **500
object instances** was independently re-labelled into the three classes by a second
annotator following the same guidelines:

| Observed (P_o) | Expected (P_e) | Cohen's κ | Interpretation (Landis & Koch) |
|:--:|:--:|:--:|:--|
| 0.821 | 0.315 | **0.739** | Substantial agreement |

## Class imbalance

The distribution is strongly imbalanced, reflecting real exam halls (most people
are quiet seated students): approximately **78.6% `normal`, 18.3%
`suspicious_moving`, 3.2% `invigilator`** (imbalance ratio ≈ 24.7). The imbalance
was left untouched at the data level and handled during training. Splits were
stratified so class proportions are preserved across train/valid/test.

## Layout after download

`scripts/download_data.py` populates the image folders so they sit next to the
annotations already in this repo:

```
detection_dataset/
├── annotations/
│   ├── train/_annotations.coco.json   (in Git)
│   ├── valid/_annotations.coco.json   (in Git)
│   └── test/_annotations.coco.json    (in Git)
├── train/   *.jpg   (from Zenodo)
├── valid/   *.jpg   (from Zenodo)
└── test/    *.jpg   (from Zenodo)
```

## File naming

Images use meaningful serial names of the form `detection_{split}_{NNNN}.jpg`
(e.g. `detection_train_0001.jpg`, `detection_valid_0001.jpg`,
`detection_test_0001.jpg`). These names match the `file_name` fields inside each
`_annotations.coco.json`, so the annotations stay valid. The original Roboflow file
names are preserved in [`name_mapping.csv`](name_mapping.csv).

## Image quality

All 2,020 images fall in the "good" quality tier (surveillance-imagery thresholds
for sharpness, brightness, contrast, and SNR), a consequence of the iPhone 15
acquisition sensor. Variability across the set is dominated by scene content and
lighting rather than sensor noise.
