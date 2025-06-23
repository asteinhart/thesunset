import cv2
import numpy as np
from PIL import Image


class SunsetDetector:
    """
    A class to detect sunsets in images using color analysis.
    """

    def __init__(self, method: str = "pil"):
        if method == "pil":
            self.detector = sunset_detector_pil
        elif method == "cv2":
            self.detector = sunset_detector_cv2
        else:
            raise ValueError("Method must be either 'pil' or 'cv2'.")

    def ingest_sunsets(self, folder_path: str):
        """
        Ingests sunset images from a folder and prepares them for detection.

        :param folder_path: Path to the folder containing sunset images
        """
        import os

        image_paths = [
            f
            for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        for image_path in image_paths:
            image = Image.open(f"{folder_path}/{image_path}")
            self.detect(image)

    def detect(self, image: Image.Image) -> float:
        """
        Detects if an image likely depicts a sunset based on color analysis.

        :param image: PIL Image object
        :return: A float score indicating the likelihood of a sunset
        """
        return self.detector(image)

    def choose_best_sunset(self, folder_path: str) -> str:
        """
        Choose the best sunset image based on color analysis.

        :param folder_path: Path to the folder containing images
        :return: The filename of the best sunset image
        """
        best_image = None
        best_score = 0.0

        import os

        image_paths = [
            f
            for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        for image_path in image_paths:
            image = Image.open(f"{folder_path}/{image_path}")
            score = self.detect(image)

            if score > best_score:
                best_score = score
                best_image = image_path

        return best_image


def sunset_detector_pil(image: Image.Image) -> float:
    """
    return the RGB values of each pixel in the image.
    """
    image = image.convert("RGB")  # Ensure the image is in RGB mode
    colors = image.getdata()
    # average R value
    average_r = sum(color[0] for color in colors) / len(colors)
    average_g = sum(color[1] for color in colors) / len(colors)
    average_b = sum(color[2] for color in colors) / len(colors)
    print(f"Average RGB: ({average_r}, {average_g}, {average_b})")

    return average_r


def sunset_detector_cv2(image: np.ndarray) -> float:
    """
    Detects if an image likely depicts a sunset based on color analysis.
    """

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

    print(f"Red1 mask sum: {np.sum(mask_red1)}")
    print(f"Red2 mask sum: {np.sum(mask_red2)}")
    print(f"Orange mask sum: {np.sum(mask_orange)}")
    print(f"Yellow mask sum: {np.sum(mask_yellow)}")

    combined_mask = mask_red1 + mask_red2 + mask_orange + mask_yellow

    # Calculate the percentage of sunset-colored pixels
    sunset_pixel_count = np.sum(combined_mask > 0)
    total_pixels = image.shape[0] * image.shape[1]
    sunset_percentage = sunset_pixel_count / total_pixels
    print(f"Sunset pixel percentage: {sunset_percentage:.2%}")

    return sunset_percentage
