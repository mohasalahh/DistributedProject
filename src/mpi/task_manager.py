
from models.zeromq_events import ZeroMQEvent
from zmq_helpers.zmq_receiver import ZMQEventReceiver

class TaskManager():

    def __init__(self):
        super().__init__()
        self.zmqReceiver = ZMQEventReceiver([ZeroMQEvent.START_PROCESSING], self.didRecieveMessage)

    
    def didRecieveMessage(self, event: ZeroMQEvent, data: str):
        print(event, data)

    def startListening(self):
        self.zmqReceiver.start()


task_manager = TaskManager()

if __name__ == '__main__':
    task_manager.startListening()