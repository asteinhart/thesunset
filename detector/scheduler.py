import schedule
import time
from datetime import timedelta, datetime
import os
from pathlib import Path

from SunsetDetector import SunsetDetector
from image_capture import capture_images
from logger import logger
from utils import determine_start_end_time, tmp_cleanup, find_sunset_time

DIR = Path(__file__).parent.resolve()


def run(take_image: bool = True, testing: bool = False) -> bool:
    """
    Main function to run the sunset detection and image capture process.
    """
    logger.info("Running thesunset")
    start_time, sunset, end_time = determine_start_end_time(when="today")

    logger.info(
        f"Sunset is at {sunset}. Taking pictures from {start_time} to {end_time}"
    )

    if testing:
        logger.info("TESTING: running now")
        start_time = datetime.now(tz=datetime.now().astimezone().tzinfo) + timedelta(
            seconds=5
        )
        end_time = start_time + timedelta(minutes=2)
        logger.info(f"Testing mode: Taking pictures from {start_time} to {end_time}")

    if take_image:
        logger.info("Taking pictures")
        if not os.path.exists(DIR / "tmp"):
            os.makedirs(DIR / "tmp")
        capture_images(
            source="rpi",
            frequency=31 if testing else 300,
            export_path=DIR / "tmp",
            start_time=start_time,
            end_time=end_time,
        )

    logger.info(
        f"Finished taking pictures, running SunsetDetector on images in {DIR / 'tmp'}"
    )
    detector = SunsetDetector(images=DIR / "tmp" / str(start_time.date()))
    detector.run()

    # Clean up temporary files
    # if not testing:
    #     logger.info("Cleaning up temporary files")
    #     tmp_cleanup(tmp_dir=DIR / "tmp/")
    #     logger.info("Temporary files cleaned up.")

    schedule_next_run()


def schedule_next_run(testing: bool = False) -> bool:
    """
    Schedule the next run of the sunset detection process.
    """

    if testing:
        logger.info("testing. scheduling run for 5 seconds")
        schedule.clear()
        schedule.every(5).seconds.do(run)
        return True

    sunset = find_sunset_time()

    if datetime.now(tz=datetime.now().astimezone().tzinfo) > sunset:
        logger.info("Sunset has already passed for today. Scheduling for tomorrow.")
        when = "tomorrow"
    else:
        when = "today"
    logger.info(f"Scheduling next run for {when}")

    start_time, sunset, end_time = determine_start_end_time(when=when)
    logger.info(
        f"The sunset tomorrow is at {sunset}. Taking pictures from {start_time} to {end_time}"
    )
    schedule.clear()
    schedule.every().day.at((start_time - timedelta(minutes=3)).strftime("%H:%M")).do(
        run, testing=testing
    )
    logger.info(
        f"Scheduled next run at {(start_time - timedelta(minutes=1)).strftime('%H:%M')}"
    )

    return True


def main(testing: bool = False) -> None:
    """
    Main entry point for the sunset detection application.

    """

    if testing:
        # Run immediately for testing purposes
        logger.info("Running thesunset immediately for testing")
        schedule_next_run(testing=True)
    else:
        schedule_next_run()

    while True:
        logger.info("Checking for scheduled runs...")
        if schedule.run_pending():
            logger.info("Scheduled run executed")
        else:
            logger.info("No scheduled run found")
        time.sleep(60)


if __name__ == "__main__":
    main(testing=False)  # Set to False for production use
