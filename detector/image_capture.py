from datetime import datetime, timedelta
import time
from picamera import PiCamera
from utils import find_sunset_time


def capture_sunset_images() -> bool:
    """
    Capture images around sunset time.
    """
    # Find the sunset time

    today = datetime.now().strftime("%Y%m%d")
    sunrise = find_sunset_time()

    start_time = sunrise - timedelta(minutes=20)
    end_time = sunrise + timedelta(minutes=20)

    with PiCamera() as camera:
        camera.resolution = (1024, 768)
        while datetime.now() < end_time:
            if datetime.now() >= start_time:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                camera.capture(f"/tmp/{today}/sunset_{timestamp}.jpg")
            time.sleep(300)  # 5-minute intervals

    return True


# 0 5 * * * /usr/bin/python3 /path/to/capture.py  # Adjust time based on your location
