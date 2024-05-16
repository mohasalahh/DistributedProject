import time
import zmq

from models.zeromq_events import ZeroMQEvent

class ZMQEventSender():

    def __init__(self, addr: str = 'tcp://*:5555'):
        super().__init__()
        
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(addr)
        time.sleep(1)

    def send(self, event: ZeroMQEvent, data: str):
        print("PUBLSIHING: " + str(event.name) + " " + data)
        self.socket.send(bytes(str(event.name) + " " + data, "UTF-8"))