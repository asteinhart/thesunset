import PIL
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
import pytz
import os
import shutil
import boto3
from datetime import datetime, timedelta
from botocore.exceptions import NoCredentialsError
from env import (
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
)
from pathlib import Path
from logger import logger
import psutil
import gc

DIR = Path(__file__).parent.resolve()


def upload_to_s3(local_file: str, s3_object: str, bucket: str = "thesunset") -> bool:
    """
    Upload a file to an S3 bucket using access keys

    :param local_file: Path to local file
    :param bucket: Target S3 bucket name
    :param s3_object: Custom object name (optional)
    :return: True if successful, False otherwise
    """
    # Create session with explicit credentials
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
    )

    s3 = session.client("s3")

    try:
        s3.upload_file(
            Filename=local_file,
            Bucket=bucket,
            Key=s3_object or local_file,  # Use local path if no custom name
        )
        logger.info(
            f"✅ Successfully uploaded {local_file} to {bucket} at {s3_object or local_file}"
        )
        return True
    except FileNotFoundError:
        logger.error(f"❌ File {local_file} not found")
    except NoCredentialsError:
        logger.error("❌ AWS credentials were invalid or not found")
    except Exception as e:
        logger.error(f"❌ Upload failed: {str(e)}")
    return False


def download_from_s3(
    local_file: str,
    s3_object: str,
    bucket: str = "thesunset",
) -> bool:
    """
    Download a file from an S3 bucket using access keys

    :param s3_object: S3 object name to download
    :param local_file: Path to save the downloaded file
    :param bucket: Source S3 bucket name
    :return: True if successful, False otherwise
    """
    # Create session with explicit credentials
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
    )

    s3 = session.client("s3")

    try:
        s3.download_file(Bucket=bucket, Key=s3_object, Filename=local_file)
        logger.info(f"✅ Successfully downloaded {s3_object} to {local_file}")
        return True
    except FileNotFoundError:
        logger.error(f"❌ Local path {local_file} not found")
    except NoCredentialsError:
        logger.error("❌ AWS credentials were invalid or not found")
    except Exception as e:
        logger.error(f"❌ Download failed: {str(e)}")
    return False


# def cv2_resize_image(image_path: str, target_size: tuple):
#     """
#     Resize an image to the target size while maintaining aspect ratio using cv2.

#     Args:
#         image_path (str): Path to the image to resize.
#         target_size (tuple): The target size as (width, height).

#     Returns:
#         numpy.ndarray: The resized image as a cv2 image.
#     """
#     # Read the image using cv2
#     image = cv2.imread(image_path)
#     if image is None:
#         raise ValueError(f"Could not read image at {image_path}")

#     height, width = image.shape[:2]
#     target_width, target_height = target_size

#     # Calculate the aspect ratio
#     aspect_ratio = width / height

#     if target_width / target_height > aspect_ratio:
#         new_width = int(target_height * aspect_ratio)
#         new_height = target_height
#     else:
#         new_width = target_width
#         new_height = int(target_width / aspect_ratio)

#     # Resize the image using cv2
#     resized_image = cv2.resize(
#         image, (new_width, new_height), interpolation=cv2.INTER_AREA
#     )

#     return resized_image


# def cv2_show_image(image):
#     """
#     Displays an image using OpenCV.

#     Args:
#         Image (numpy.ndarray): The image to display.
#     """
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     plt.imshow(image)
#     plt.show()


def find_sunset_time(
    city_name: str = "Brooklyn",
    region_name: str = "New York",
    timezone_name: str = "America/New_York",
    latitude: float = 40.723258099845616,
    longitude: float = -73.94263482667436,
    date: datetime = None,
) -> datetime:
    """Find the sunset time for a given city using the Astral library.
    Args:
        city_name (str): Name of the city.
        region_name (str): Name of the region.
        timezone_name (str): The timezone name (e.g., 'America/New_York').
        latitude (float): Latitude of the city.
        longitude (float): Longitude of the city.
        date (datetime, optional): The date for which to find the sunset time. Defaults to the current date.
    """
    if date is None:
        # Get current date in the target timezone instead of naive local time
        target_tz = pytz.timezone(timezone_name)
        date = datetime.now(target_tz).date()
    elif hasattr(date, "date"):
        # If datetime object passed, extract just the date part
        date = date.date()

    city = LocationInfo(
        name=city_name,
        region=region_name,
        timezone=timezone_name,
        latitude=latitude,
        longitude=longitude,
    )

    s = sun(city.observer, date=date, tzinfo=pytz.timezone(city.timezone))
    sunset = s["sunset"]

    return sunset.astimezone(pytz.timezone(city.timezone))


def determine_start_end_time(
    when: str = "today", before_sun: int = 40, after_sun: int = 30
) -> tuple:
    """
    Determine the start and end time for capturing images.
    """
    if when == "today":
        date = datetime.now()
    elif when == "tomorrow":
        date = datetime.now() + timedelta(days=1)

    sunset = find_sunset_time(date=date)
    start_time = sunset - timedelta(minutes=before_sun)
    end_time = sunset + timedelta(minutes=after_sun)

    return start_time, sunset, end_time


def tmp_cleanup(tmp_dir: Path = DIR / "tmp/") -> None:
    """
    Clean up temporary files in the specified directory.

    Args:
        tmp_dir (str): The path to the temporary directory to clean up.
    """

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
        print(f"Temporary directory {tmp_dir} cleaned up.")
    else:
        print(f"Temporary directory {tmp_dir} does not exist.")


def upload_folder_s3(
    folder_path: Path = DIR / "tmp/",
    s3_folder: str = "images/",
    bucket: str = "thesunset",
) -> bool:
    """
    Save a folder to S3.

    Args:
        folder_path (Path): The path to the folder to upload.
        bucket (str): The target S3 bucket name.
        s3_folder (str): The S3 folder path where files will be uploaded.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not os.path.exists(folder_path):
        logger.error(f"Folder {folder_path} does not exist.")
        return False

    for filename in os.listdir(folder_path):
        local_file = folder_path / filename
        s3_object = f"{s3_folder}{filename}"
        upload_to_s3(str(local_file), s3_object, bucket)

    return True


def check_system_resources():

    # Force garbage collection
    gc.collect()

    # Check memory
    memory = psutil.virtual_memory()
    logger.info(
        f"Memory usage: {memory.percent}% (Available: {memory.available / 1024 / 1024:.1f} MB)"
    )

    # Check disk space
    disk = psutil.disk_usage("/")
    logger.info(f"Disk usage: {disk.percent}% (Free: {disk.free / 1024 / 1024:.1f} MB)")

    if memory.percent > 85:
        logger.warning("High memory usage detected!")
        return False

    return True
