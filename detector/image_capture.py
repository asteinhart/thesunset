from datetime import datetime
import time

from picamera2 import Picamera2
from libcamera import controls
from pathlib import Path
import os

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
        with Picamera2() as camera:
            camera.configure(
                camera.create_still_configuration(main={"size": (3280, 2464)})
            )
            camera.set_controls({"AwbMode": controls.AwbModeEnum.Daylight})

            camera.start()
            while datetime.now(tz=datetime.now().astimezone().tzinfo) < end_time:
                if datetime.now(tz=datetime.now().astimezone().tzinfo) >= start_time:
                    timestamp = datetime.now(
                        tz=datetime.now().astimezone().tzinfo
                    ).strftime("%Y%m%d_%H%M")
                    camera.capture_file(export_path / today / f"{timestamp}.jpg")
                time.sleep(frequency)

    return True
