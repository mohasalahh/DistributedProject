from enum import Enum
import uuid
import cv2
import numpy as np
from mpi4py import MPI
import threading

from models.image_processing_task import ImageOperation, ImageProcessingTask
from processing import apply, divide_image_into_arrays

class WorkerThread(threading.Thread):
    def __init__(self, task: ImageProcessingTask):
        super().__init__()
        self.task = task

    def run(self):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()

        # Load image data on rank 0
        if rank == 0:
            image_data = divide_image_into_arrays(self.task.image_path, size)
        else:
            image_data = None

        # Scatter image data to all processes
        local_chunk = comm.scatter(image_data, root=0)

        # Apply Gaussian filter to local chunk of image data
        filtered_chunk = apply(self.task.operation_type, local_chunk)

        # Gather filtered chunks from all processes on rank 0
        all_filtered_chunks = comm.gather(filtered_chunk, root=0)

        # On rank 0, combine filtered chunks and save the filtered image
        if rank == 0:
            filtered_image = np.concatenate(all_filtered_chunks, axis=1)
            cv2.imwrite(self.task.get_save_path(), filtered_image) 
