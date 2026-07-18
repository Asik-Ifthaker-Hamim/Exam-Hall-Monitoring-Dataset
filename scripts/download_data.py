#!/usr/bin/env python3
"""Download and verify the Exam-Hall Monitoring Dataset image archives from Zenodo.

The annotations/labels live in this Git repository; the image files are archived on
Zenodo (which mints a citable DOI). This script fetches the per-dataset image
archives, checks their SHA-256 sums, and extracts them next to the annotations.

Usage
-----
    python scripts/download_data.py --all
    python scripts/download_data.py frame_classification
    python scripts/download_data.py detection external_test

Only the Python standard library is used, so no `pip install` is needed.

Maintainer TODO
---------------
Fill in ZENODO_RECORD_ID and, for each dataset, the exact `filename` and `sha256`
of the archive you uploaded to Zenodo. Until then the script will print the values
it expects and exit.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
import zipfile
from pathlib import Path

# --------------------------------------------------------------------------- #
# Configuration — EDIT THIS after publishing the Zenodo record.
# --------------------------------------------------------------------------- #
ZENODO_RECORD_ID = "21432043"

REPO_ROOT = Path(__file__).resolve().parents[1]

# Each archive already contains its dataset-root folder (e.g.
# `detection_dataset/train/...`), so all three extract to the repo root and merge
# cleanly with the annotations already tracked in Git.
# `sha256 = None` disables verification (not recommended).
DATASETS = {
    "detection": {
        "filename": "detection_dataset_images.zip",
        "sha256": "c887a3fe9650b6a977cb00f37277dece5604e10013574e17cbac8bdfff25abb9",
        "extract_to": REPO_ROOT,
    },
    "frame_classification": {
        "filename": "frame_classification_images.zip",
        "sha256": "dcb392d01b7aad99dfa63d394c049f599fd9b254052a92c9bc74e4df4dbc4e53",
        "extract_to": REPO_ROOT,
    },
    "external_test": {
        "filename": "external_test_set_images.zip",
        "sha256": "28c5f55f1823542d84767b0d4f04bd135d40754b24e011425ee87428c16a09d8",
        "extract_to": REPO_ROOT,
    },
}


def zenodo_url(filename: str) -> str:
    return f"https://zenodo.org/records/{ZENODO_RECORD_ID}/files/{filename}?download=1"


def sha256sum(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def download(url: str, dest: Path) -> None:
    print(f"  downloading {url}")

    def _hook(count, block_size, total):
        if total > 0:
            pct = min(100, count * block_size * 100 // total)
            print(f"\r    {pct:3d}%", end="", flush=True)

    urllib.request.urlretrieve(url, dest, _hook)  # noqa: S310 (trusted host)
    print()


def fetch(name: str, keep_archive: bool) -> None:
    cfg = DATASETS[name]
    if ZENODO_RECORD_ID == "XXXXXXX":
        print(
            f"[{name}] Zenodo record not configured yet.\n"
            f"        Expected archive: {cfg['filename']}\n"
            f"        Extract to      : {cfg['extract_to']}\n"
            f"        Set ZENODO_RECORD_ID (and the sha256) at the top of this script."
        )
        return

    dest_dir: Path = cfg["extract_to"]
    dest_dir.mkdir(parents=True, exist_ok=True)
    archive = dest_dir / cfg["filename"]

    print(f"[{name}] -> {dest_dir}")
    if not archive.exists():
        download(zenodo_url(cfg["filename"]), archive)
    else:
        print(f"  using cached {archive.name}")

    expected = cfg["sha256"]
    if expected:
        print("  verifying checksum ...")
        actual = sha256sum(archive)
        if actual.lower() != expected.lower():
            archive.unlink(missing_ok=True)
            sys.exit(f"  CHECKSUM MISMATCH for {archive.name}\n"
                     f"    expected {expected}\n    got      {actual}")
        print("  checksum OK")
    else:
        print("  WARNING: no sha256 configured; skipping verification")

    print("  extracting ...")
    with zipfile.ZipFile(archive) as z:
        z.extractall(dest_dir)
    print("  done")

    if not keep_archive:
        archive.unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("datasets", nargs="*", choices=list(DATASETS), metavar="DATASET",
                    help="one or more of: " + ", ".join(DATASETS))
    ap.add_argument("--all", action="store_true", help="download every dataset")
    ap.add_argument("--keep-archive", action="store_true",
                    help="keep the downloaded .zip after extraction")
    args = ap.parse_args()

    targets = list(DATASETS) if args.all else args.datasets
    if not targets:
        ap.error("specify one or more datasets, or --all")

    for name in targets:
        fetch(name, keep_archive=args.keep_archive)


if __name__ == "__main__":
    main()
