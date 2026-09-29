"""
Catch-up script for when the Pi loses wifi.

While offline, scheduler.py keeps capturing photos into tmp/<day>/ and
SunsetDetector still scores them and records the best image for each day in
tmp/scores.json, but every upload_to_s3() call silently fails (no network),
so those days never make it into the S3 scores.json or get a best_sunset
image uploaded.

Re-scoring every photo to find the best one again is slow on a Pi, so this
script instead trusts the already-computed tmp/scores.json: for each day
missing from S3, it uses that day's recorded best_image_time to find the
matching photo, converts it to webp, uploads it + metadata.json, and merges
that day's existing scores entry into the master scores.json in S3.
Already-uploaded days are left untouched.

Run on the Pi from the detector/ directory:
    source sunset/bin/activate && python3 catch_up.py [--dry-run]
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from logger import logger
from SunsetDetector import SunsetDetector
from utils import download_from_s3, upload_to_s3

DIR = Path(__file__).parent.resolve()
TMP_DIR = DIR / "tmp"
LOCAL_SCORES_PATH = TMP_DIR / "scores.json"


def load_local_scores() -> dict:
    if not LOCAL_SCORES_PATH.exists():
        raise RuntimeError(f"No local scores.json found at {LOCAL_SCORES_PATH}")
    with open(LOCAL_SCORES_PATH) as f:
        return json.load(f)


def get_uploaded_days() -> set:
    """Days already present in the merged scores.json in S3."""
    local_copy = TMP_DIR / "_catchup_remote_scores.json"

    if not download_from_s3(str(local_copy), "scores.json"):
        raise RuntimeError(
            "Could not download scores.json from S3 - check network/credentials "
            "before running catch-up (aborting to avoid blind re-uploads)."
        )

    with open(local_copy) as f:
        remote_scores = json.load(f)
    os.remove(local_copy)

    return set(remote_scores.keys())


def resolve_best_image(day: str, best_image_time: str) -> Path | None:
    """Find the captured photo matching a day entry's recorded best_image_time."""
    day_dir = TMP_DIR / day
    if not day_dir.exists():
        return None

    hhmm = datetime.strptime(best_image_time, "%I:%M %p").strftime("%H%M")
    day_nodash = day.replace("-", "")

    exact = list(day_dir.glob(f"{day_nodash}_{hhmm}.*"))
    if exact:
        return exact[0]

    # Fall back to matching just the time suffix, in case the date prefix
    # in the filename doesn't line up with the folder name.
    fallback = [
        f for f in day_dir.iterdir() if f.is_file() and f.stem.endswith(f"_{hhmm}")
    ]
    return fallback[0] if fallback else None


def merge_day_into_remote(day: str, day_entry: dict) -> None:
    local_copy = TMP_DIR / "_catchup_remote_scores.json"

    if not download_from_s3(str(local_copy), "scores.json"):
        raise RuntimeError(f"Could not download scores.json from S3 to merge {day}")

    with open(local_copy) as f:
        remote_scores = json.load(f)

    remote_scores[day] = day_entry

    with open(local_copy, "w") as f:
        json.dump(remote_scores, f, indent=4)

    upload_to_s3(str(local_copy), "scores.json")
    os.remove(local_copy)


def upload_day(day: str, day_entry: dict) -> bool:
    best_image = resolve_best_image(day, day_entry["best_image_time"])
    if not best_image:
        logger.error(
            f"Could not find a photo for {day} matching best_image_time "
            f"{day_entry['best_image_time']!r}"
        )
        return False

    num_images = len(
        [
            f
            for f in (TMP_DIR / day).iterdir()
            if f.suffix.lower() in (".jpg", ".jpeg", ".png")
        ]
    )

    # Reuse SunsetDetector's save() (webp conversion + best_sunset/metadata
    # upload) but skip choose_best_sunset() - we already know the answer.
    detector = SunsetDetector(images=str(TMP_DIR / day))
    detector.best_image = str(best_image)
    detector.metadata["best_image"] = str(best_image)
    detector.metadata["num_images"] = num_images

    if not detector.save():
        logger.error(f"Failed to upload best image/metadata for {day}")
        return False

    merge_day_into_remote(day, day_entry)
    return True


def main(dry_run: bool = False) -> None:
    local_scores = load_local_scores()
    uploaded_days = get_uploaded_days()
    missing_days = [d for d in local_scores if d not in uploaded_days]

    logger.info(
        f"Local scores.json has {len(local_scores)} days, "
        f"{len(missing_days)} missing from S3: {missing_days}"
    )

    if not missing_days:
        logger.info("Nothing to catch up on - every local day is already in S3.")
        return

    if dry_run:
        logger.info("Dry run - not uploading anything.")
        return

    succeeded, failed = [], []
    for day in missing_days:
        logger.info(f"Catching up {day}...")
        if upload_day(day, local_scores[day]):
            succeeded.append(day)
            logger.info(f"Done: {day}")
        else:
            failed.append(day)
            logger.error(f"Failed: {day}")

    logger.info(f"Catch-up complete. Succeeded: {succeeded}. Failed: {failed}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload missed sunset days to S3")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only report which days are missing from S3, don't upload",
    )
    args = parser.parse_args()
    main(dry_run=args.dry_run)
