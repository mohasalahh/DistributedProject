
from enum import IntEnum
import json
import time
import redis

from constants import REDIS_ADDR, REDIS_PORT
from models.image_processing_task import ImageOperation


r = redis.Redis(host=REDIS_ADDR, port=REDIS_PORT, decode_responses=True)

class ProcessState(IntEnum):
    STARTED = 1
    FAILED = 2
    PROGRESS = 3
    DONE = 4

def acquire_lock(lock_name, timeout=10):
    while True:
        lock = r.setnx(lock_name, "locked")
        if lock:
            r.expire(lock_name, timeout)
            return True
        else:
            time.sleep(0.1)
            
def set_to_redis(key: str, 
state: ProcessState | None = None, 
num_of_nodes: int | None = None, 
operation: ImageOperation | None = None, 
progress: float | None = None, 
uploaded_file_name: str | None = None, 
num_of_succeeded_nodes: int | None = None):
    
    # safe concurrent update
    with r.pipeline() as pipe:
        while True:
            try:
                # Watch the key to detect changes
                pipe.watch(key)
                # Get the current value of the counter
                current_record = json.loads(pipe.get(key) or "{}")
                # Increment the counter value within a transaction
                pipe.multi()

                if num_of_succeeded_nodes and state != ProcessState.DONE:
                    if "num_of_succeeded_nodes" in current_record:
                        current_record["num_of_succeeded_nodes"] = int(current_record["num_of_succeeded_nodes"])+num_of_succeeded_nodes
                    else:
                        current_record["num_of_succeeded_nodes"] = num_of_succeeded_nodes
                elif state == ProcessState.DONE:
                    current_record["num_of_succeeded_nodes"] = current_record["num_of_nodes"]

                
                if uploaded_file_name:
                    current_record["uploaded_file_name"] = uploaded_file_name

                if state:
                    current_record["state"] = state
                if num_of_nodes:
                    current_record["num_of_nodes"] = num_of_nodes
                if operation and ("operation" not in current_record or current_record["operation"] != ProcessState.DONE.value):
                    current_record["operation"] = operation
                if progress:
                    current_record["progress"] = progress

                pipe.set(key, json.dumps(current_record))
                pipe.execute()
                break
            except redis.WatchError:
                # Retry if another client modified the key
                continue

    # current_record = get_from_redis(key)
    # if not current_record:
    #     current_record = {}
        
    
    # r.set(key, json.dumps(current_record))

def get_from_redis(key: str):
    val = r.get(key)
    if val:
        return json.loads(val)
    
    return None