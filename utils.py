import PIL
import cv2
import matplotlib.pyplot as plt


def resize_image(image_path, target_size):
    """
    Resize an image to the target size while maintaining aspect ratio using cv2.

    Args:
        image_path (str): Path to the image to resize.
        target_size (tuple): The target size as (width, height).

    Returns:
        numpy.ndarray: The resized image as a cv2 image.
    """
    # Read the image using cv2
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image at {image_path}")

    height, width = image.shape[:2]
    target_width, target_height = target_size

    # Calculate the aspect ratio
    aspect_ratio = width / height

    if target_width / target_height > aspect_ratio:
        new_width = int(target_height * aspect_ratio)
        new_height = target_height
    else:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)

    # Resize the image using cv2
    resized_image = cv2.resize(
        image, (new_width, new_height), interpolation=cv2.INTER_AREA
    )

    return resized_image


def show_image(image):
    """
    Displays an image using OpenCV.

    Args:
        Image (numpy.ndarray): The image to display.
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.show()
