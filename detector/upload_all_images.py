"""
Upload every folder under tmp/ to S3 under an all_images/ prefix,
preserving each folder's name and internal structure.

Usage:
    python upload_all_images.py
"""

from pathlib import Path

import boto3
from env import AWS_ACCESS_KEY, AWS_SECRET_KEY
from logger import logger
from utils import upload_to_s3

DIR = Path(__file__).parent.resolve()


def get_existing_folders(s3_prefix: str, bucket: str) -> set[str]:
    """
    List the folder names that already exist under s3_prefix/ in the bucket
    (e.g. all_images/2026-09-28/ -> "2026-09-28"). Returns an empty set if
    the prefix doesn't exist yet (first run).
    """
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
    )
    s3 = session.client("s3")

    existing = set()
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(
        Bucket=bucket, Prefix=f"{s3_prefix}/", Delimiter="/"
    ):
        for prefix in page.get("CommonPrefixes", []):
            folder_name = prefix["Prefix"].removeprefix(f"{s3_prefix}/").rstrip("/")
            existing.add(folder_name)

    return existing


def upload_all_images(
    tmp_dir: Path = DIR / "tmp",
    s3_prefix: str = "all_images",
    bucket: str = "thesunset",
) -> None:
    """
    Upload every folder found in tmp_dir to S3, keyed as
    {s3_prefix}/{folder_name}/{relative_path_within_folder}.
    Folders that already exist in S3 under s3_prefix are skipped.
    """
    if not tmp_dir.exists():
        logger.error(f"Folder {tmp_dir} does not exist.")
        return

    folders = [f for f in tmp_dir.iterdir() if f.is_dir()]
    if not folders:
        logger.info(f"No folders found in {tmp_dir}.")
        return

    existing_folders = get_existing_folders(s3_prefix, bucket)

    for folder in folders:
        if folder.name in existing_folders:
            logger.info(f"Skipping {folder.name}, already uploaded to S3.")
            continue

        for file_path in folder.rglob("*"):
            if not file_path.is_file():
                continue
            relative_path = file_path.relative_to(folder)
            s3_object = f"{s3_prefix}/{folder.name}/{relative_path.as_posix()}"
            upload_to_s3(str(file_path), s3_object, bucket)


if __name__ == "__main__":
    upload_all_images()
