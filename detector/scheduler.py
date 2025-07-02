import schedule
import time
from datetime import timedelta
import os
from pathlib import Path

from SunsetDetector import SunsetDetector
from image_capture import capture_images
from logger import logger
from utils import determine_start_end_time, tmp_cleanup

DIR = Path(__file__).parent.resolve()


def run(take_image: bool = True) -> bool:
    logger.info("Running thesunset")
    start_time, sunset, end_time = determine_start_end_time(when="today")

    logger.info(
        f"Sunset is at {sunset}. Taking pictures from {start_time} to {end_time}"
    )
    if take_image:
        logger.info("Taking pictures")
        if not os.path.exists(DIR / "tmp"):
            os.makedirs(DIR / "tmp")
        capture_images(
            source="rpi",
            frequency=120,
            export_path=DIR / "tmp",
            start_time=start_time,
            end_time=end_time,
        )

    logger.info(
        f"Finished taking pictures, running SunsetDetector on images in {DIR / 'tmp'}"
    )
    detector = SunsetDetector(images=DIR / "tmp")
    detector.run()

    tmp_cleanup(tmp_dir=DIR / "tmp")

    schedule_next_run()


def schedule_next_run(testing: bool = False) -> bool:

    if testing:
        logger.info("testing. scheduling run for 5 seconds")
        schedule.clear()
        schedule.every(5).seconds.do(run)
        return True

    start_time, sunset, end_time = determine_start_end_time(when="tomorrow")
    logger.info(
        f"The sunset tomorrow is at {sunset}. Taking pictures from {start_time} to {end_time}"
    )
    schedule.clear()
    schedule.every().day.at((start_time - timedelta(minutes=1)).strftime("%H:%M")).do(
        run
    )
    logger.info(
        f"Scheduled next run at {(start_time - timedelta(minutes=1)).strftime("%H:%M")}"
    )

    return True


def main():
    schedule_next_run()

    while True:
        logger.info("Checking for scheduled runs...")
        if schedule.run_pending():
            logger.info("Scheduled run executed")
        else:
            logger.info("No scheduled run found")
        time.sleep(60)


if __name__ == "__main__":
    main()
