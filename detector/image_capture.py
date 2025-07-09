from datetime import datetime
import time

from picamera import PiCamera
from pathlib import Path
import os

DIR = Path(__file__).parent.resolve()


def capture_images(
    start_time: datetime,
    end_time: datetime,
    source: str = "rpi",
    frequency: int = 300,
    export_path: Path = DIR / "tmp",
) -> bool:
    """
    Capture images around sunset time with a given
    """

    today = start_time.strftime("%Y%m%d")

    os.makedirs(export_path / today, exist_ok=True)

    if source == "rpi":
        with PiCamera() as camera:
            camera.resolution = (1024, 768)
            while datetime.now() < end_time:
                if datetime.now() >= start_time:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                    camera.capture(export_path / f"{timestamp}.jpg")
                time.sleep(frequency)

    return True
