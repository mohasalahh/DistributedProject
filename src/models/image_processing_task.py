from enum import Enum
import uuid


class ImageOperation(Enum):
    """
    Enumeration representing different types of image processing operations.
    """
    EDGE_DETECTION = 1
    COLOR_INVERSION = 2
    CONTRAST_ADJUSTMENT = 3

class ImageProcessingTask:
    """
    Represents a task for processing an image.
    """

    def __init__(self, operation_type: ImageOperation, image_path: str):
        """
        Initializes an ImageProcessingTask object.

        Args:
            operation_type (ImageOperation): The type of image processing operation to perform.
            image_path (str): The path to the input image.
        """
        self.id = str(uuid.uuid4())  # Unique identifier for the task
        self.operation_type = operation_type  # Type of image processing operation
        self.image_path = image_path  # Path to the input image
    
    def get_save_path(self):
        """
        Generates the path where the processed image will be saved.

        Returns:
            str: The path to save the processed image.
        """
        return "processed_imgs/" + self.id + ".png"
