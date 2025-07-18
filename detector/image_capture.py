from datetime import datetime
import time

from picamera2 import Picamera2
from libcamera import controls
from pathlib import Path
import os
from utils import logger

DIR = Path(__file__).parent.resolve()


def initialize_camera(max_retries: int = 3, retry_delay: int = 5) -> Picamera2:
    """
    Initialize camera with retry logic and error handling
    """
    camera = None

    for attempt in range(max_retries):
        try:
            logger.info(f"Camera initialization attempt {attempt + 1}/{max_retries}")

            # Create camera instance
            camera = Picamera2()

            # Configure camera
            config = camera.create_still_configuration(main={"size": (3280, 2464)})
            camera.configure(config)

            # Set camera controls
            camera.set_controls({"AwbMode": controls.AwbModeEnum.Daylight})

            # Start camera
            camera.start()

            # Test capture to ensure camera is working
            logger.info("Testing camera with a test capture...")
            time.sleep(2)  # Give camera time to initialize

            logger.info("Camera initialized successfully!")
            return camera

        except Exception as e:
            logger.error(
                f"Camera initialization attempt {attempt + 1} failed: {str(e)}"
            )

            # Clean up failed camera instance
            if camera:
                try:
                    camera.stop()
                    camera.close()
                except Exception:
                    pass
                camera = None

            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("All camera initialization attempts failed!")
                raise Exception(
                    f"Failed to initialize camera after {max_retries} attempts"
                )

    return camera


def capture_single_image(
    camera: Picamera2, filepath: Path, max_retries: int = 3
) -> bool:
    """
    Capture a single image with retry logic
    """
    for attempt in range(max_retries):
        try:
            camera.capture_file(str(filepath))
            logger.info(f"Image captured successfully: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Image capture attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(1)  # Brief delay before retry
            else:
                logger.error(f"Failed to capture image after {max_retries} attempts")
                return False
    return False


def capture_images(
    start_time: datetime,
    end_time: datetime,
    source: str = "rpi",
    frequency: int = 2,
    export_path: Path = DIR / "tmp",
) -> bool:
    """
    Capture images around sunset time with robust error handling
    """

    today = start_time.strftime("%Y-%m-%d")
    os.makedirs(export_path / today, exist_ok=True)

    if source == "rpi":
        camera = None

        try:
            # Initialize camera with retry logic
            camera = initialize_camera()

            logger.info("Camera started successfully")
            logger.info(f"Capturing images from {start_time} to {end_time}")
            logger.info(
                f"Current time: {datetime.now(tz=datetime.now().astimezone().tzinfo)}"
            )

            successful_captures = 0
            failed_captures = 0

            while datetime.now(tz=datetime.now().astimezone().tzinfo) < end_time:
                current_time = datetime.now(tz=datetime.now().astimezone().tzinfo)

                if current_time >= start_time:
                    timestamp = current_time.strftime("%Y%m%d_%H%M")
                    filepath = export_path / today / f"{timestamp}.jpg"

                    logger.info(f"Capturing image at {timestamp}")

                    if capture_single_image(camera, filepath):
                        successful_captures += 1
                    else:
                        failed_captures += 1

                        # If we have too many failed captures in a row, try to reinitialize camera
                        if failed_captures >= 3:
                            logger.warning(
                                "Multiple capture failures detected, attempting camera reinitialization..."
                            )
                            try:
                                camera.stop()
                                camera.close()
                                time.sleep(2)
                                camera = initialize_camera()
                                failed_captures = (
                                    0  # Reset counter after successful reinit
                                )
                            except Exception as e:
                                logger.error(
                                    f"Camera reinitialization failed: {str(e)}"
                                )
                                return False
                else:
                    logger.info("Waiting for the right time to capture images...")

                time.sleep(frequency)

            logger.info(
                f"Image capture completed. Successful: {successful_captures}, Failed: {failed_captures}"
            )

        except Exception as e:
            logger.error(f"Fatal error during image capture: {str(e)}")
            return False

        finally:
            # Always clean up camera resources
            if camera:
                try:
                    camera.stop()
                    camera.close()
                    logger.info("Camera resources cleaned up")
                except Exception as e:
                    logger.error(f"Error cleaning up camera: {str(e)}")

    return True
