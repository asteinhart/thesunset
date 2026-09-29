"""
Upload every folder under tmp/ to S3 under an all_images/ prefix,
preserving each folder's name and internal structure.

Usage:
    python upload_all_images.py
"""

from pathlib import Path

from logger import logger
from utils import upload_to_s3

DIR = Path(__file__).parent.resolve()


def upload_all_images(
    tmp_dir: Path = DIR / "tmp",
    s3_prefix: str = "all_images",
    bucket: str = "thesunset",
) -> None:
    """
    Upload every folder found in tmp_dir to S3, keyed as
    {s3_prefix}/{folder_name}/{relative_path_within_folder}.
    """
    if not tmp_dir.exists():
        logger.error(f"Folder {tmp_dir} does not exist.")
        return

    folders = [f for f in tmp_dir.iterdir() if f.is_dir()]
    if not folders:
        logger.info(f"No folders found in {tmp_dir}.")
        return

    for folder in folders:
        for file_path in folder.rglob("*"):
            if not file_path.is_file():
                continue
            relative_path = file_path.relative_to(folder)
            s3_object = f"{s3_prefix}/{folder.name}/{relative_path.as_posix()}"
            upload_to_s3(str(file_path), s3_object, bucket)


if __name__ == "__main__":
    upload_all_images()
