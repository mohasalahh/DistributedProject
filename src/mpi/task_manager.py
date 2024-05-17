
import threading
from models.rmq_events import RMQEvent
from rmq_helpers.rmq_receiver import RMQEventReceiver
import subprocess

class MPITask(threading.Thread):
    def __init__(self, num_of_nodes, process_id, img_path, op_id):
        super().__init__()

        self.num_of_nodes = num_of_nodes
        self.process_id = process_id
        self.img_path = img_path
        self.op_id = op_id

    def run(self):
        result = subprocess.run(['mpiexec', '-n', str(self.num_of_nodes), 'python3', "-m", "mpi.worker", self.process_id, self.img_path, self.op_id]) 
        print(result)



class TaskManager():

    def __init__(self):
        super().__init__()
        self.zmqReceiver = RMQEventReceiver([RMQEvent.START_PROCESSING], self.didRecieveMessage)
        self.num_of_nodes = 4

    
    def didRecieveMessage(self, event: RMQEvent, data: str):
        if event != RMQEvent.START_PROCESSING: return
        dataSplit = data.split(" ")
        print(dataSplit)
        process_id = dataSplit[0]
        img_path = dataSplit[1]
        op_id = dataSplit[2]

        newThread = MPITask(self.num_of_nodes, process_id, img_path, op_id)
        newThread.start()


    def startListening(self):
        self.zmqReceiver.start()


task_manager = TaskManager()

if __name__ == '__main__':
    task_manager.startListening()