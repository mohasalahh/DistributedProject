
from enum import Enum
import uuid


class ImageOperation(Enum):
    EDGE_DETECTION = 1
    COLOR_INVERSION = 2
    CONTRAST_ADJUSTMENT = 3

class ImageProcessingTask:
    def __init__(self, operation_type: ImageOperation, image_path: str):
        self.id = str(uuid.uuid4())
        self.operation_type = operation_type
        self.image_path = image_path
    
    def get_save_path(self):
        return "processed_imgs/"+self.id+".png"