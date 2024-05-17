import threading
import subprocess
from models.rmq_events import RMQEvent
from rmq_helpers.rmq_receiver import RMQEventReceiver
from rmq_helpers.rmq_sender import send_to_rmq

class MPITask(threading.Thread):
    """
    This class represents an MPI task which is run as a thread. It is responsible for 
    executing an MPI-based worker script using subprocess to handle image processing.

    Attributes:
        num_of_nodes (int): The number of MPI nodes (processes) to run.
        process_id (str): The unique identifier for the process.
        img_path (str): The path to the image file to be processed.
        op_id (str): The identifier for the operation to be performed.
    """
    def __init__(self, num_of_nodes, process_id, img_path, op_id):
        super().__init__()
        self.num_of_nodes = num_of_nodes
        self.process_id = process_id
        self.img_path = img_path
        self.op_id = op_id

    def run(self):
        """
        Executes the MPI worker script using the provided attributes. 
        This function is automatically called when the thread is started.
        """
        result = subprocess.run(['mpiexec', '-n', str(self.num_of_nodes), 'python3', "-m", "mpi.worker", self.process_id, self.img_path, self.op_id])
        print(result)
        del self  # Delete this thread object after execution is completed

class TaskManager():
    """
    This class handles the management of image processing tasks. It listens for
    RabbitMQ events to start processing and creates threads for MPI tasks.

    Attributes:
        zmqReceiver (RMQEventReceiver): Receiver for RMQ events related to starting processing.
        num_of_nodes (int): Default number of MPI nodes (processes) used for tasks.
    """
    def __init__(self):
        super().__init__()
        self.zmqReceiver = RMQEventReceiver([RMQEvent.START_PROCESSING], self.didRecieveMessage)
        self.num_of_nodes = 4

    def didRecieveMessage(self, event: RMQEvent, data: str):
        """
        Handles incoming messages from RabbitMQ. Starts a new MPI task when a START_PROCESSING
        event is received.

        Args:
            event (RMQEvent): The type of event that triggered the message.
            data (str): The data received with the event, expected to contain process_id, img_path, and op_id.
        """
        if event != RMQEvent.START_PROCESSING:
            return
        
        dataSplit = data.split(" ")
        process_id = dataSplit[0]
        img_path = dataSplit[1]
        op_id = dataSplit[2]

        data = " ".join([process_id, str(self.num_of_nodes), op_id, img_path])
        send_to_rmq(RMQEvent.PROCESSING_STARTED, data)

        newThread = MPITask(self.num_of_nodes, process_id, img_path, op_id)
        newThread.start()

    def startListening(self):
        """
        Starts the RMQ event receiver which listens for messages to start image processing tasks.
        """
        self.zmqReceiver.start()

task_manager = TaskManager()

if __name__ == '__main__':
    task_manager.startListening()
