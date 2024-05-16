

import signal
import time
import rmq_helpers
from models.zeromq_events import ZeroMQEvent
from zmq_sender import ZMQEventSender



signal.signal(signal.SIGINT, signal.SIG_DFL)
if __name__ == "__main__":
    # src_path = "./uploaded_imgs/img.jpeg"
    # new_task = ImageProcessingTask(ImageOperation.COLOR_INVERSION, src_path)

    # worker_thread = WorkerThread(new_task)
    # worker_thread.start()

    zeroMQReceiver = ZMQEventSender()
    zeroMQReceiver.send(ZeroMQEvent.PROGRESS_UPDATE, "process_id:100")
    time.sleep(5)