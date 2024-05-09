import signal
import threading
import time
import zmq

from models.zeromq_events import ZeroMQEvent

signal.signal(signal.SIGINT, signal.SIG_DFL)

class ZMQEventSender():

    def __init__(self, addr: str = 'tcp://*:5555'):
        super().__init__()
        
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(addr)

    def send(self, event: ZeroMQEvent, data: str):
        self.socket.send(bytes(event + " " + data))