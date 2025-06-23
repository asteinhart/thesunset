import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import os
from detector.logger import logger
from datetime import date
from utils import find_sunset_time, upload_to_s3
import json


class SunsetDetector:
    """
    A class to detect sunsets in images using color analysis.
    """

    def __init__(
        self,
        detect_method: str = "red",
        images: Path = None,
        best_image: Path = None,
        save_method: str = "s3",
        today: str = date.today().strftime("%Y-%m-%d"),
    ):
        self.images = Path(images) if isinstance(images, str) else images
        self.best_image = best_image
        self.sunset_time = find_sunset_time().strftime("%Y-%m-%d_%H:%M:%S")
        self.today = today
        self.metadata = {
            "sunset_time": self.sunset_time,
            "today": self.today,
            "detect_method": detect_method,
            "save_method": save_method,
            "num_images": 0,
            "best_image": best_image,
        }
        self.change_detect_method(detect_method)
        self.change_save_method(save_method)

        self.scores = {}

    def __repr__(self):
        return f"SunsetDetector({self.metadata})"

    def choose_best_sunset(self) -> bool:
        """
        Choose the best sunset image based on color analysis.

        :param folder_path: Path to the folder containing images
        :return: The filename of the best sunset image
        """
        best_image = None
        best_score = 0.0

        image_paths = [
            f
            for f in os.listdir(self.images)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        logger.info(f"Found {len(image_paths)} images in {self.images}")
        self.metadata["num_images"] = len(image_paths)
        logger.info(
            f"Scoring images for sunset detection using {self.detect.__name__} method."
        )

        for image_path in image_paths:
            score = self.detect(self.images / image_path)
            logger.debug(f"Image: {image_path}, Score: {score}")
            self.scores[image_path] = score

            if score > best_score:
                best_score = score
                best_image = image_path

        logger.info(f"Best image found: {best_image} with score: {best_score:.2f}")
        self.best_image = self.images / best_image
        self.metadata["best_image"] = str(self.best_image)

        return True

    def _sunset_detector_red(self, image: Path) -> float:
        """
        return the RGB values of each pixel in the image.
        """
        try:
            img_path = Path(image)
            img = Image.open(img_path)
        except (TypeError, Exception) as e:
            logger.error(f"Invalid image path provided: {e}")
            return 0.0

        img = img.convert("RGB")  # Ensure the image is in RGB mode
        colors = img.getdata()
        # average R value
        average_r = sum(color[0] for color in colors) / len(colors)
        average_g = sum(color[1] for color in colors) / len(colors)
        average_b = sum(color[2] for color in colors) / len(colors)
        logger.debug(f"Average RGB: ({average_r}, {average_g}, {average_b})")

        return average_r

    def _sunset_detector_cv2(self, image: Path) -> float:
        """
        Detects if an image likely depicts a sunset based on color analysis.
        """

        try:
            image = cv2.imread(str(image))
            if image is None:
                raise ValueError("Image not found or invalid format.")
        except Exception as e:
            logger.error(f"Error reading image: {e}")
            return 0.0

        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define color ranges for sunset hues (adjust as needed)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        lower_orange = np.array([10, 100, 100])
        upper_orange = np.array([25, 255, 255])
        lower_yellow = np.array([25, 100, 100])
        upper_yellow = np.array([40, 255, 255])

        mask_red1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
        mask_orange = cv2.inRange(hsv_img, lower_orange, upper_orange)
        mask_yellow = cv2.inRange(hsv_img, lower_yellow, upper_yellow)

        combined_mask = mask_red1 + mask_red2 + mask_orange + mask_yellow

        # Calculate the percentage of sunset-colored pixels
        sunset_pixel_count = np.sum(combined_mask > 0)
        total_pixels = image.shape[0] * image.shape[1]
        sunset_percentage = sunset_pixel_count / total_pixels
        logger.debug(f"Sunset pixel percentage: {sunset_percentage:.2%}")

        return sunset_percentage

    def _sunset_detector_saturation(self, image: Path) -> float:
        """
        Detects the saturation of an image to determine if it likely depicts a sunset.
        Higher saturation indicates more vivid colors, which is typical for sunsets.

        :param image_path: Path to the image file
        :return: A float score indicating the saturation level
        """
        try:
            image = cv2.imread(str(image))
            if image is None:
                raise ValueError("Image not found or invalid format.")
        except Exception as e:
            logger.error(f"Error reading image: {e}")
            return 0.0

        # Read the image and convert to HSV to analyze
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        saturation = np.mean(hsv[:, :, 1])
        return saturation  # Higher = more vivid colors

    def change_detect_method(self, detect_method: str) -> None:
        """
        Change the detection method.

        :param method: The new method to use ('red', 'cv2', or 'saturation')
        """
        if detect_method == "red":
            self.detect = self._sunset_detector_red
        elif detect_method == "cv2":
            self.detect = self._sunset_detector_cv2
        elif detect_method == "saturation":
            self.detect = self._sunset_detector_saturation
        else:
            raise ValueError("Method must be either 'red', 'cv2' or 'saturation'")
        logger.info(f"Detection method changed to {detect_method}.")

    def _save_s3(self) -> bool:
        """
        Save the best sunset image to an S3 bucket.

        :param save_path: Path where the best image will be saved
        :return: True if successful, False otherwise
        """
        save_path = f"{self.today}/best_sunset.jpg"
        # Placeholder for S3 saving logic
        logger.info(f"Saving best image to S3 at {save_path}")
        if not self.best_image:
            logger.error("No best image found to save.")
            return False
        upload_to_s3(self.best_image, s3_object=save_path)

        # upload metadata to s3
        metadata_path = f"tmp/{self.today}/metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=4)
        upload_to_s3(metadata_path, s3_object=f"{self.today}/metadata.json")

        return True

    def _save_local(self) -> bool:
        """
        Save the best sunset image to a local path.

        :param save_path: Path where the best image will be saved
        :return: True if successful, False otherwise
        """
        if not self.best_image:
            logger.error("No best image found to save.")
            return False

        save_path = f"tmp/{self.today}/best_sunset.jpg"
        save_dir = os.path.dirname(save_path)

        # Create directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        try:
            img = Image.open(self.best_image)
            img.save(save_path)
            logger.info(f"Best image saved to {save_path}")

            # upload metadata to s3
            metadata_path = f"tmp/{self.today}/metadata.json"
            if not os.path.exists(os.path.dirname(f"tmp/{self.today}")):
                os.makedirs(os.path.dirname(f"tmp/{self.today}"))

            with open(metadata_path, "w") as f:
                json.dump(self.metadata, f, indent=4)

            logger.info(f"Metadata saved to {metadata_path}")

            return True
        except Exception as e:
            logger.error(f"Error saving best image: {e}")
            return False

    def change_save_method(self, save_method: str):
        """
        Change the save method.

        :param save_method: The new save method to use ('s3' or 'local')
        """
        if save_method == "s3":
            self.save = self._save_s3
            self.metadata["save_method"] = "s3"
        elif save_method == "local":
            self.save = self._save_local
            self.metadata["save_method"] = "local"
        else:
            raise ValueError("Save method must be either 's3' or 'local'")
        logger.info(f"Save method changed to {save_method}.")

    def run(self) -> bool:
        """
        Run the sunset detection process.

        :return: True if successful, False otherwise
        """
        if not self.images:
            logger.error("No images provided for sunset detection.")
            return False

        if not self.choose_best_sunset():
            logger.error("Failed to choose the best sunset image.")
            return False

        if not self.save():
            logger.error("Failed to save the best sunset image.")
            return False

        logger.info("Sunset detection and saving completed successfully.")

        return True
