
from models.zeromq_events import ZeroMQEvent
from zmq_helpers.zmq_receiver import ZMQEventReceiver
import subprocess


class TaskManager():

    def __init__(self):
        super().__init__()
        self.zmqReceiver = ZMQEventReceiver([ZeroMQEvent.START_PROCESSING], self.didRecieveMessage)
        self.num_of_nodes = 4

    
    def didRecieveMessage(self, event: ZeroMQEvent, data: str):
        if event != ZeroMQEvent.START_PROCESSING: return
        dataSplit = data.split(" ")
        process_id = dataSplit[0]
        img_path = dataSplit[1]
        op_id = dataSplit[2]
        result = subprocess.run(['mpiexec', '-n', str(self.num_of_nodes), 'python3', "-m", "mpi.worker", process_id, img_path, op_id]) 
        print(result)


    def startListening(self):
        self.zmqReceiver.start()


task_manager = TaskManager()

if __name__ == '__main__':
    task_manager.startListening()