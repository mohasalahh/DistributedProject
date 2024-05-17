from enum import IntEnum
import json
import time
import redis

from constants import REDIS_ADDR, REDIS_PORT
from models.image_processing_task import ImageOperation

# Create a Redis connection
r = redis.Redis(host=REDIS_ADDR, port=REDIS_PORT, decode_responses=True)

class ProcessState(IntEnum):
    STARTED = 1
    FAILED = 2
    PROGRESS = 3
    DONE = 4

def set_to_redis(key: str, 
                 state: ProcessState | None = None, 
                 num_of_nodes: int | None = None, 
                 operation: ImageOperation | None = None, 
                 progress: float | None = None, 
                 uploaded_file_name: str | None = None, 
                 num_of_succeeded_nodes: int | None = None):
    """
    Set or update various properties related to an image processing task in Redis.

    Parameters:
    key (str): The Redis key under which to store the task data.
    state (ProcessState): The current state of the task.
    num_of_nodes (int): The number of nodes involved in the task.
    operation (ImageOperation): The operation being performed on the image.
    progress (float): The progress of the image processing task.
    uploaded_file_name (str): The name of the uploaded file.
    num_of_succeeded_nodes (int): The number of nodes that have successfully completed their part of the task.
    """
    # Safe concurrent update
    with r.pipeline() as pipe:
        while True:
            try:
                # Watch the key to detect changes
                pipe.watch(key)
                current_record = json.loads(pipe.get(key) or "{}")
                pipe.multi()

                if num_of_succeeded_nodes and state != ProcessState.DONE:
                    current_record["num_of_succeeded_nodes"] = current_record.get("num_of_succeeded_nodes", 0) + num_of_succeeded_nodes
                elif state == ProcessState.DONE:
                    current_record["num_of_succeeded_nodes"] = current_record["num_of_nodes"]

                if uploaded_file_name:
                    current_record["uploaded_file_name"] = uploaded_file_name
                if state:
                    current_record["state"] = state.value
                if num_of_nodes:
                    current_record["num_of_nodes"] = num_of_nodes
                if operation:
                    current_record["operation"] = operation.value
                if progress:
                    current_record["progress"] = progress

                pipe.set(key, json.dumps(current_record))
                pipe.execute()
                break
            except redis.WatchError:
                continue

def get_from_redis(key: str):
    """
    Retrieve the value stored under a specific Redis key.

    Parameters:
    key (str): The key for which to retrieve the value.

    Returns:
    dict: The value stored in Redis, parsed as a dictionary, or None if the key does not exist.
    """
    val = r.get(key)
    if val:
        return json.loads(val)
    
    return None
