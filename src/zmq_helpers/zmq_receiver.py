import threading
from typing import List
import zmq

from models.zeromq_events import ZeroMQEvent


class ZMQEventReceiver(threading.Thread):

    def __init__(self, events: List[ZeroMQEvent], did_receive_callback, addr: str = 'tcp://localhost:5555'):
        super().__init__()
        
        context = zmq.Context()

        self.events = events
        self.did_receive_function = did_receive_callback
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(addr)

        for event in events:
            self.socket.setsockopt(zmq.SUBSCRIBE, bytes(event.name, "UTF-8"))

    def run(self):
        while True:
            message = self.socket.recv_string()
            self.handleMessage(message)

    def handleMessage(self, data: str):
        print("received message: ", data)
        splitMessage = data.split(" ")
        messageName = splitMessage[0]
        if messageName in ZeroMQEvent.__members__:
            message_enum = ZeroMQEvent[messageName]
            self.did_receive_function(message_enum, " ".join(splitMessage[1:]))
        else:
            print("Message not found")



