import threading
import zmq

from models.zeromq_events import ZeroMQEvent


class ZMQEventReceiver(threading.Thread):

    def __init__(self, addr: str = 'tcp://localhost:5555'):
        super().__init__()
        
        context = zmq.Context()

        self.socket = context.socket(zmq.SUB)
        self.socket.connect(addr)
    
        self.socket.setsockopt(zmq.SUBSCRIBE, bytes(ZeroMQEvent.NODE_FAILED.name, "UTF-8"))
        self.socket.setsockopt(zmq.SUBSCRIBE, bytes(ZeroMQEvent.PROCESSING_FAILED.name, "UTF-8"))
        self.socket.setsockopt(zmq.SUBSCRIBE, bytes(ZeroMQEvent.PROCESSING_DONE.name, "UTF-8"))
        self.socket.setsockopt(zmq.SUBSCRIBE, bytes(ZeroMQEvent.PROGRESS_UPDATE.name, "UTF-8"))

    def run(self):
        while True:
            message = self.socket.recv_multipart()
            print(f'Received: {message}')
