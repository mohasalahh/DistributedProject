import time
import zmq

from models.zeromq_events import ZeroMQEvent


if __name__ == "__main__":
    print("aaaaa")

context = None
socket = None

def send_to_zmq(event: ZeroMQEvent, data: str):
    global context
    global socket
    if not context and not socket: 

        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind('tcp://*:5555')
        time.sleep(1)
    print("PUBLISHING: " + str(event.name) + " " + data)
    socket.send_string(str(event.name) + " " + data)
