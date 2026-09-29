"""
Zip every folder under tmp/ and upload it to S3 under an all_images/
prefix as a single {folder_name}.zip object.

Usage:
    python upload_all_images.py
"""

import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import boto3
from env import AWS_ACCESS_KEY, AWS_SECRET_KEY
from logger import logger
from utils import upload_to_s3

DIR = Path(__file__).parent.resolve()


def get_existing_folders(s3_prefix: str, bucket: str) -> set[str]:
    """
    List the folder names that already have a {name}.zip uploaded under
    s3_prefix/ in the bucket (e.g. all_images/2026-09-28.zip -> "2026-09-28").
    Returns an empty set if the prefix doesn't exist yet (first run).
    """
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
    )
    s3 = session.client("s3")

    existing = set()
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=f"{s3_prefix}/"):
        for obj in page.get("Contents", []):
            key_name = obj["Key"].removeprefix(f"{s3_prefix}/")
            if key_name.endswith(".zip"):
                existing.add(key_name.removesuffix(".zip"))

    return existing


def zip_and_upload_folder(
    folder: Path, s3_prefix: str, bucket: str, s3_client
) -> None:
    with tempfile.TemporaryDirectory() as scratch_dir:
        zip_path = str(Path(scratch_dir) / f"{folder.name}.zip")
        # Images are already compressed (JPEG/PNG), so skip DEFLATE:
        # it just burns CPU for no size savings.
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_STORED) as zf:
            for file_path in folder.rglob("*"):
                if file_path.is_file():
                    zf.write(file_path, file_path.relative_to(folder))

        s3_object = f"{s3_prefix}/{folder.name}.zip"
        upload_to_s3(zip_path, s3_object, bucket, s3_client)


def upload_all_images(
    tmp_dir: Path = DIR / "tmp",
    s3_prefix: str = "all_images",
    bucket: str = "thesunset",
    max_workers: int = 2,
) -> None:
    """
    Zip every folder found in tmp_dir and upload it to S3 as
    {s3_prefix}/{folder_name}.zip. Folders that already have a zip
    uploaded under s3_prefix are skipped. Multiple folders are
    zipped and uploaded concurrently.
    """
    if not tmp_dir.exists():
        logger.error(f"Folder {tmp_dir} does not exist.")
        return

    folders = [f for f in tmp_dir.iterdir() if f.is_dir()]
    if not folders:
        logger.info(f"No folders found in {tmp_dir}.")
        return

    existing_folders = get_existing_folders(s3_prefix, bucket)

    folders_to_upload = []
    for folder in folders:
        if folder.name in existing_folders:
            logger.info(f"Skipping {folder.name}, already uploaded to S3.")
            continue
        folders_to_upload.append(folder)

    if not folders_to_upload:
        return

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
    )
    s3_client = session.client("s3")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                zip_and_upload_folder, folder, s3_prefix, bucket, s3_client
            ): folder
            for folder in folders_to_upload
        }
        for future in as_completed(futures):
            folder = futures[future]
            try:
                future.result()
                logger.info(f"Finished uploading {folder.name}.")
            except Exception as e:
                logger.error(f"Failed to upload {folder.name}: {e}")


if __name__ == "__main__":
    upload_all_images()
