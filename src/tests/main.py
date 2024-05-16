

import signal
import zmq_helpers
from models.zeromq_events import ZeroMQEvent
from zmq_receiver import ZMQEventReceiver


signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":
    # src_path = "./uploaded_imgs/img.jpeg"
    # new_task = ImageProcessingTask(ImageOperation.COLOR_INVERSION, src_path)

    # worker_thread = WorkerThread(new_task)
    # worker_thread.start()

    zmqReceiver = ZMQEventReceiver()
    zmqReceiver.start()
    zmqReceiver.join()
        
