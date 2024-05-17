import argparse
from enum import Enum
import time
import uuid
import cv2
import numpy as np
from mpi4py import MPI
import threading

from models.image_processing_task import ImageOperation, ImageProcessingTask
from models.rmq_events import RMQEvent
from mpi.processing import apply, divide_image_into_arrays
from rmq_helpers.rmq_receiver import RMQEventReceiver
from rmq_helpers.rmq_sender import send_to_rmq

class WorkerThread(threading.Thread):
    """
    A subclass of threading.Thread for processing image processing tasks in parallel.

    Attributes:
        task (ImageProcessingTask): The image processing task to be performed.
    """

    def __init__(self, task: ImageProcessingTask):
        super().__init__()
        self.task = task
        # flag indicating if any of the nodes failed
        self.zmqReceiver = None
        self.didFail = False
        self.num_of_nodes_done = 0
        self.size = 1

    def run(self):
        """
        Execute the image processing task in parallel using MPI.
        """
        
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        self.size = comm.Get_size()
        
        try:
            # Load image data on rank 0
            if rank == 0:
                self.zmqReceiver = RMQEventReceiver([RMQEvent.NODE_FAILED, RMQEvent.NODE_DONE], self.didRecieveMessage)
                self.zmqReceiver.start()
                image_data = divide_image_into_arrays(self.task.img_path, self.size)
            else:
                image_data = None

            time.sleep(5)
            # Scatter image data to all processes
            local_chunk = comm.scatter(image_data, root=0)

            # Apply Gaussian filter to local chunk of image data
            filtered_chunk = apply(self.task.operation_type, local_chunk)

            # Gather filtered chunks from all processes on rank 0
            all_filtered_chunks = comm.gather(filtered_chunk, root=0)

            # On rank 0, combine filtered chunks and save the filtered image
            if rank == 0:
                if self.didFail:
                    data = " ".join([self.task.id])
                    send_to_rmq(RMQEvent.PROCESSING_FAILED, data)
                    return
                filtered_image = np.concatenate(all_filtered_chunks, axis=1)
                cv2.imwrite(self.task.get_save_path(), filtered_image) 
                data = " ".join([self.task.id, self.task.get_save_path()])
                send_to_rmq(RMQEvent.PROCESSING_DONE, data)
            else:
                data = " ".join([self.task.id, str(rank)])
                send_to_rmq(RMQEvent.NODE_DONE, data)
        except Exception as e:
            print(e)
            if rank == 0:
                data = " ".join([self.task.id])
                send_to_rmq(RMQEvent.PROCESSING_FAILED, data)
            else:
                data = " ".join([self.task.id, str(rank)])
                send_to_rmq(RMQEvent.NODE_FAILED, data)

        
        if self.zmqReceiver:
            self.zmqReceiver.stop_consuming()

    def didRecieveMessage(self, event: RMQEvent, data: str):
        dataSplit = data.split(" ")
        process_id = dataSplit[0]
        # if process_id != self.task.id: return 
        if event == RMQEvent.NODE_FAILED:
            rank = dataSplit[1] # rank of failed node

            if process_id == self.task.id:
                self.didFail = True
        elif event == RMQEvent.NODE_DONE:
            self.num_of_nodes_done += 1

            data = " ".join([self.task.id, str(self.num_of_nodes_done), str(self.size)])
            send_to_rmq(RMQEvent.PROGRESS_UPDATE, data)

        



def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('process_id', type=str, help='The process ID')
    parser.add_argument('img_path', type=str, help='The img path')
    parser.add_argument('operation_id', type=int, help='The operation ID')

    args = parser.parse_args()
    process_id: str = args.process_id
    img_path: str = args.img_path
    operation_id: int = args.operation_id

    new_task = ImageProcessingTask(process_id, img_path, ImageOperation(operation_id) )

    worker_thread = WorkerThread(new_task)
    worker_thread.start()
    worker_thread.join()


if __name__ == '__main__':
    main()