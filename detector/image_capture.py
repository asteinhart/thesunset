from datetime import datetime
import time

from picamera2 import PiCamera2
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
        with PiCamera2() as camera:
            camera.configure(
                camera.create_still_configuration(main={"size": (3280, 2464)})
            )
            camera.start()
            while datetime.now() < end_time:
                if datetime.now() >= start_time:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                    camera.capture_file(export_path / today / f"{timestamp}.jpg")
                time.sleep(frequency)

    return True
