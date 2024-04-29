import cv2
import numpy as np

from models.image_processing_task import ImageOperation

# MARK: - Helper Functions

def divide_image_into_arrays(image_path, x):
    """
    Divide the given image into x arrays horizontally.

    Parameters:
    - image_path (str): The path to the input image.
    - x (int): The number of arrays to divide the image into.

    Returns:
    - arrays_np (numpy.ndarray): An array of sub-images.
    """
    image = cv2.imread(image_path)

    # Get the dimensions of the image
    _, width, _ = image.shape

    # Calculate the size of each sub-image
    sub_image_width = width // x

    # Divide the image into x arrays
    arrays = []
    for i in range(x):
        # Calculate the starting and ending pixel indices for the current sub-image
        start_col = i * sub_image_width
        end_col = start_col + sub_image_width

        # Extract the sub-image
        sub_image = image[:, start_col:end_col, :]

        # Append the sub-image to the arrays list
        arrays.append(sub_image)

    # Convert the list of arrays into a single NumPy array
    arrays_np = np.array(arrays)

    return arrays_np

# MARK: - Operations

def edge_detection(chunk):
    """
    Apply edge detection to the given image chunk using the Canny algorithm.

    Parameters:
    - chunk (numpy.ndarray): The input image chunk.

    Returns:
    - edged_img (numpy.ndarray): The image with detected edges.
    """
    return cv2.Canny(chunk, 100, 200)

def color_inversion(chunk):
    """
    Invert the colors of the given image chunk.

    Parameters:
    - chunk (numpy.ndarray): The input image chunk.

    Returns:
    - inverted_img (numpy.ndarray): The image with inverted colors.
    """
    return cv2.bitwise_not(chunk)

def contrast_adjustment(chunk):
    """
    Adjust the contrast of the given image chunk using histogram equalization.

    Parameters:
    - chunk (numpy.ndarray): The input image chunk.

    Returns:
    - contrast_adjusted_img (numpy.ndarray): The image with adjusted contrast.
    """
    return cv2.equalizeHist(chunk)

def apply(operation: ImageOperation, img):
    """
    Apply the specified image processing operation to the given image.

    Parameters:
    - operation (ImageOperation): The image processing operation to apply.
    - img (numpy.ndarray): The input image.

    Returns:
    - processed_img (numpy.ndarray): The processed image.
    """
    if operation == ImageOperation.COLOR_INVERSION:
        return color_inversion(img)
    elif operation == ImageOperation.EDGE_DETECTION:
        return edge_detection(img)
    elif operation == ImageOperation.CONTRAST_ADJUSTMENT:
        return contrast_adjustment(img)

    return img
