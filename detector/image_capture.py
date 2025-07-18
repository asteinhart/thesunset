from datetime import datetime
import time

from picamera2 import Picamera2
from libcamera import controls
from pathlib import Path
import os
from utils import logger

DIR = Path(__file__).parent.resolve()


def capture_images(
    start_time: datetime,
    end_time: datetime,
    source: str = "rpi",
    frequency: int = 2,
    export_path: Path = DIR / "tmp",
) -> bool:
    """
    Capture images around sunset time with a given
    """

    today = start_time.strftime("%Y-%m-%d")

    os.makedirs(export_path / today, exist_ok=True)

    if source == "rpi":

        camera = Picamera2()
        camera.configure(camera.create_still_configuration(main={"size": (3280, 2464)}))
        camera.set_controls({"AwbMode": controls.AwbModeEnum.Daylight})

        camera.start()

        logger.info("Camera started")
        logger.info(f"Capturing images from {start_time} to {end_time}")
        logger.info(f"now is {datetime.now(tz=datetime.now().astimezone().tzinfo)}")

        while datetime.now(tz=datetime.now().astimezone().tzinfo) < end_time:
            logger.info("Waiting for the right time to capture images...")
            if datetime.now(tz=datetime.now().astimezone().tzinfo) >= start_time:
                timestamp = datetime.now(
                    tz=datetime.now().astimezone().tzinfo
                ).strftime("%Y%m%d_%H%M")
                logger.info(f"Capturing image at {timestamp}")
                camera.capture_file(export_path / today / f"{timestamp}.jpg")
            time.sleep(frequency)

        logger.info("Image capture completed.")
        camera.stop()

    return True
