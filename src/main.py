

import cv2
from models.image_processing_task import ImageOperation, ImageProcessingTask
from worker import WorkerThread


if __name__ == "__main__":
    src_path = "./uploaded_imgs/img.jpeg"
    new_task = ImageProcessingTask(ImageOperation.COLOR_INVERSION, src_path)

    worker_thread = WorkerThread(new_task)
    worker_thread.start()