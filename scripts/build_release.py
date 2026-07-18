#!/usr/bin/env python3
"""Build the release: rename images to meaningful serial names and sync labels.

Source data (raw, messy Roboflow hashes / recording-prefixed frames) is turned into
clean, serially-numbered files whose names encode their folder/split:

    detection:      detection_{train|valid|test}_{NNNN}.jpg
    external test:  external_test_{NNNN}.jpg
    frame:          {normal|suspicious}_{NNNNN}.jpg

For the COCO datasets the `file_name` fields inside `_annotations.coco.json` are
rewritten to the new names, so annotations stay valid. For the frame dataset a
fresh `labels.csv` is written that keeps the `recording_id` group column (needed for
leakage-free splitting) alongside the new and original names.

Outputs
-------
* Small metadata is written INTO this repository (git-tracked):
    detection_dataset/annotations/{split}/_annotations.coco.json
    detection_dataset/name_mapping.csv
    external_test_set/annotations/test/_annotations.coco.json
    external_test_set/name_mapping.csv
    frame_classification_dataset/labels.csv
    frame_classification_dataset/name_mapping.csv
* Image archives (for Zenodo) are written to OUTPUT_DIR as .zip files.

Usage
-----
    python scripts/build_release.py --metadata-only     # fast: just sync labels
    python scripts/build_release.py --zip-only          # build the Zenodo .zips
    python scripts/build_release.py                     # both

Edit the SOURCE_* paths below to point at your raw data before running.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from pathlib import Path

# --------------------------------------------------------------------------- #
# Source locations (raw data) — EDIT to match your machine.
# --------------------------------------------------------------------------- #
REPO_ROOT = Path(__file__).resolve().parents[1]
THESIS_ROOT = REPO_ROOT.parent  # "D:/Hamim/thesis dataset"

SOURCE_DETECTION_ZIP = THESIS_ROOT / "real-time-monitoring-system 3.v3-final_dataset.coco.zip"
SOURCE_EXTERNAL_ZIP = THESIS_ROOT / "testing dataset.v1-test_only.coco.zip"
SOURCE_FRAME_DIR = THESIS_ROOT / "final" / "new dataset"  # contains normal/ and suspicious/

OUTPUT_DIR = THESIS_ROOT / "release_zenodo"  # where the Zenodo .zip archives are written

DET_SPLITS = ("train", "valid", "test")
FRAME_CLASSES = ("normal", "suspicious")


# --------------------------------------------------------------------------- #
# Detection / external-test (COCO) helpers.
# --------------------------------------------------------------------------- #
def _coco_rename_map(images: list[dict], prefix: str) -> dict[str, str]:
    """old file_name -> new file_name, serial assigned by sorted original name."""
    ordered = sorted(images, key=lambda im: im["file_name"])
    mapping = {}
    for i, im in enumerate(ordered, start=1):
        ext = Path(im["file_name"]).suffix.lower() or ".jpg"
        mapping[im["file_name"]] = f"{prefix}_{i:04d}{ext}"
    return mapping


def build_coco_dataset(src_zip: Path, splits, prefix_for, repo_dir: Path,
                       arc_root: str, do_zip: bool):
    """Rewrite COCO annotations with new names; optionally build the image zip."""
    all_rows = []  # (split, old_name, new_name)
    zf_out = None
    if do_zip:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        zip_path = OUTPUT_DIR / f"{arc_root}_images.zip"
        zf_out = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_STORED)  # jpgs already compressed

    with zipfile.ZipFile(src_zip) as zin:
        names = set(zin.namelist())
        for split in splits:
            ann_name = f"{split}/_annotations.coco.json"
            coco = json.loads(zin.read(ann_name))
            rename = _coco_rename_map(coco["images"], prefix_for(split))

            for im in coco["images"]:
                old = im["file_name"]
                new = rename[old]
                im["file_name"] = new
                all_rows.append((split, old, new))

            # Write updated annotations into the repo.
            out_ann = repo_dir / "annotations" / split / "_annotations.coco.json"
            out_ann.parent.mkdir(parents=True, exist_ok=True)
            out_ann.write_text(json.dumps(coco), encoding="utf-8")

            # Copy images into the zip under the new names.
            if zf_out is not None:
                for old, new in [(o, n) for s, o, n in all_rows if s == split]:
                    member = f"{split}/{old}"
                    if member not in names:
                        raise FileNotFoundError(f"{member} missing in {src_zip.name}")
                    zf_out.writestr(f"{arc_root}/{split}/{new}", zin.read(member))

    if zf_out is not None:
        zf_out.close()

    # Mapping CSV (git-tracked).
    with (repo_dir / "name_mapping.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["split", "original_filename", "new_filename"])
        w.writerows(sorted(all_rows))
    print(f"  {arc_root}: {len(all_rows)} images renamed across {len(splits)} split(s)")


# --------------------------------------------------------------------------- #
# Frame-classification helpers.
# --------------------------------------------------------------------------- #
def build_frame_dataset(do_zip: bool):
    repo_dir = REPO_ROOT / "frame_classification_dataset"
    frame_re = re.compile(r"^(.*)_(\d+)\.jpg$", re.I)

    records = []  # (label, original_name, recording_id, frame_index)
    for label in FRAME_CLASSES:
        d = SOURCE_FRAME_DIR / label
        for fn in sorted(p.name for p in d.iterdir() if p.suffix.lower() == ".jpg"):
            m = frame_re.match(fn)
            rec = m.group(1) if m else fn
            idx = int(m.group(2)) if m else -1
            records.append((label, fn, rec, idx))

    # Assign per-label serial, ordered by (recording_id, frame_index) so a
    # recording's frames stay contiguous and the numbering is meaningful.
    labels_rows, map_rows = [], []
    zf_out = None
    if do_zip:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        zf_out = zipfile.ZipFile(OUTPUT_DIR / "frame_classification_images.zip",
                                 "w", zipfile.ZIP_STORED)

    for label in FRAME_CLASSES:
        items = sorted([r for r in records if r[0] == label], key=lambda r: (r[2], r[3]))
        for i, (lab, old, rec, idx) in enumerate(items, start=1):
            new = f"{label}_{i:05d}.jpg"
            labels_rows.append([f"{label}/{new}", label, rec, idx])
            map_rows.append([f"{label}/{old}", f"{label}/{new}", rec, idx])
            if zf_out is not None:
                zf_out.writestr(f"frame_classification_dataset/{label}/{new}",
                                (SOURCE_FRAME_DIR / label / old).read_bytes())

    if zf_out is not None:
        zf_out.close()

    with (repo_dir / "labels.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["filepath", "label", "recording_id", "frame_index"])
        w.writerows(labels_rows)
    with (repo_dir / "name_mapping.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["original_filepath", "new_filepath", "recording_id", "frame_index"])
        w.writerows(map_rows)
    print(f"  frame_classification: {len(labels_rows)} frames renamed")


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--metadata-only", action="store_true",
                    help="only rewrite annotations/labels, skip building zips")
    ap.add_argument("--zip-only", action="store_true",
                    help="only build image zips (assumes metadata already synced)")
    args = ap.parse_args()

    do_meta = not args.zip_only
    do_zip = not args.metadata_only

    print("Detection dataset:")
    build_coco_dataset(
        SOURCE_DETECTION_ZIP, DET_SPLITS,
        prefix_for=lambda s: f"detection_{s}",
        repo_dir=REPO_ROOT / "detection_dataset",
        arc_root="detection_dataset", do_zip=do_zip,
    )
    print("External test set:")
    build_coco_dataset(
        SOURCE_EXTERNAL_ZIP, ("test",),
        prefix_for=lambda s: "external_test",
        repo_dir=REPO_ROOT / "external_test_set",
        arc_root="external_test_set", do_zip=do_zip,
    )
    print("Frame-classification dataset:")
    build_frame_dataset(do_zip=do_zip)

    if do_zip:
        print(f"\nZenodo archives written to: {OUTPUT_DIR}")
    if do_meta:
        print("Repo metadata (annotations / labels.csv / name_mapping.csv) updated.")


if __name__ == "__main__":
    main()
