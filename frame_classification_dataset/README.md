# Frame-Classification Dataset

Single-label video frames used to train the scene-level frame classifiers
(Approach B in the thesis, including the custom **ExamNet-Lite** model). Each frame
carries one binary label describing whether the scene contains suspicious activity.

## Contents

| Property | Value |
|----------|-------|
| Total frames | 7,772 |
| Classes | `normal` (4,160), `suspicious` (3,612) |
| Class balance | ≈ 1.15 : 1 (normal : suspicious) |
| Source recordings | 36 recording prefixes |
| Label format | Directory-based (ImageFolder) + `labels.csv` |
| Source videos | Disjoint from the detection and external-test sets |
| License | CC BY 4.0 |

> This corresponds to the frame dataset described in the thesis (reported there as
> ~7,771 frames from 35 recordings; the small difference is due to a few very short
> edge recordings). The figures above reflect exactly what ships in the release.

## Layout after download

The images use the standard **ImageFolder** convention — the parent directory name
is the label:

```
frame_classification_dataset/
├── labels.csv           (in Git — see below)
├── normal/       *.jpg  (from Zenodo)
└── suspicious/   *.jpg  (from Zenodo)
```

## `labels.csv` (included in this repo)

A manifest of every frame, so you can build splits without touching the images:

| Column | Description |
|--------|-------------|
| `filepath` | Path relative to this folder, e.g. `normal/normal_00001.jpg`. |
| `label` | `normal` or `suspicious`. |
| `recording_id` | **Group id** — the source recording the frame came from (e.g. `additional_vid1`). |
| `frame_index` | Frame number within the recording. |

## File naming

Images use meaningful serial names of the form `{label}_{NNNNN}.jpg`
(e.g. `normal_00001.jpg`, `suspicious_00001.jpg`). Within each class the serial is
assigned in `(recording_id, frame_index)` order, so a recording's frames stay
contiguous. The original recording-prefixed file names are preserved in
[`name_mapping.csv`](name_mapping.csv) if you need to trace a frame back to its
source. Because the recording is no longer encoded in the file name, **always use
the `recording_id` column from `labels.csv` for group-aware splitting.**

## Group-aware splitting (important)

Frames from the same recording are highly correlated. To avoid **data leakage**,
splits must keep every frame of a given `recording_id` on the same side of the
split (group-aware / group-stratified cross-validation). Do **not** split frames
randomly across recordings — doing so inflates measured performance because near-
duplicate frames from one recording would appear in both train and test.

Some recordings contribute frames to both classes (activity changes over the course
of a session), so labels are effectively per-frame; the `recording_id` is the unit
you group on, not the label.

Example (scikit-learn):

```python
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

df = pd.read_csv("labels.csv")
y = (df["label"] == "suspicious").astype(int)
groups = df["recording_id"]
sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
for fold, (tr, te) in enumerate(sgkf.split(df, y, groups)):
    ...  # no recording_id appears in both tr and te
```

## Preparation notes

Recordings were decoded to frames and labelled by end-to-end visual inspection.
An earlier perceptual-hash deduplication step was **removed** because it discarded
~78% of frames and destabilised the class balance and cross-validation folds; it
was replaced by uniform temporal sub-sampling capped at 200 frames per recording in
the thesis experiments. The released frames are the pre-cap collection — apply the
cap yourself from `labels.csv` if you want to reproduce the thesis folds exactly.

Image-quality statistics match the detection set (≈122 mean brightness, ≈63 mean
contrast on a 0–255 scale), as expected from the shared capture hardware.
