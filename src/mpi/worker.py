import argparse
import random
import time
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
    This class represents a worker thread in a distributed image processing system,
    capable of processing tasks in parallel using MPI and handling MPI-related errors.

    Attributes:
        task (ImageProcessingTask): The image processing task to be performed.
    """

    def __init__(self, task: ImageProcessingTask):
        """
        Initializes the WorkerThread with a specific image processing task.

        Args:
            task (ImageProcessingTask): The image processing task assigned to this worker.
        """
        super().__init__()
        self.task = task
        self.zmqReceiver = None
        self.didFail = False
        self.num_of_nodes_done = 0
        self.size = 1

    def run(self):
        """
        Runs the worker thread, executing the distributed image processing task using MPI,
        handling node failures, and sending updates via RabbitMQ.
        """
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        self.size = comm.Get_size()

        try:
            if rank == 0:
                self.zmqReceiver = RMQEventReceiver([RMQEvent.NODE_FAILED, RMQEvent.NODE_DONE], self.didRecieveMessage)
                self.zmqReceiver.start()
                image_data = divide_image_into_arrays(self.task.img_path, self.size)
            else:
                image_data = None

            local_chunk = comm.scatter(image_data, root=0)

            time.sleep(random.randint(3, 10))  # Simulate processing delay

            if rank == 1:
                raise Exception("Example Error")  # Simulate error in node

            filtered_chunk = apply(self.task.operation_type, local_chunk)

            if rank != 0:
                send_to_rmq(RMQEvent.NODE_DONE, f"{self.task.id} {rank}")

            all_filtered_chunks = comm.gather(filtered_chunk, root=0)

            if rank == 0:
                if self.didFail:
                    send_to_rmq(RMQEvent.PROCESSING_FAILED, self.task.id)
                    return
                filtered_image = np.concatenate(all_filtered_chunks, axis=1)
                cv2.imwrite(self.task.get_save_path(), filtered_image)
                send_to_rmq(RMQEvent.PROCESSING_DONE, f"{self.task.id} {self.task.get_save_path()}")

        except Exception as e:
            print(e)
            send_to_rmq(RMQEvent.NODE_FAILED if rank != 0 else RMQEvent.PROCESSING_FAILED, f"{self.task.id} {rank}")

            comm.gather([], root=0)

        try:
            if self.zmqReceiver:
                self.zmqReceiver.stop_consuming()
        except Exception as e:
            pass

    def didRecieveMessage(self, event: RMQEvent, data: str):
        """
        Handles messages received from RabbitMQ related to node failures or task completions.

        Args:
            event (RMQEvent): The type of event (NODE_FAILED or NODE_DONE).
            data (str): The message data containing process ID and potentially the rank of the node.
        """
        dataSplit = data.split(" ")
        process_id = dataSplit[0]
        if process_id != self.task.id:
            return
        
        if event == RMQEvent.NODE_FAILED:
            self.didFail = True
        elif event == RMQEvent.NODE_DONE:
            self.num_of_nodes_done += 1
            send_to_rmq(RMQEvent.PROGRESS_UPDATE, f"{self.task.id} {self.num_of_nodes_done} {self.size}")

def main():
    """
    Main function to parse arguments and initiate the image processing task.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('process_id', type=str, help='The process ID')
    parser.add_argument('img_path', type=str, help='The image path')
    parser.add_argument('operation_id', type=int, help='The operation ID')

    args = parser.parse_args()
    new_task = ImageProcessingTask(args.process_id, args.img_path, ImageOperation(args.operation_id))

    worker_thread = WorkerThread(new_task)
    worker_thread.start()
    worker_thread.join()

if __name__ == '__main__':
    main()
