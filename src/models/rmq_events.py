
from enum import Enum


class RMQEvent(Enum):
    NODE_FAILED = 1
    PROCESSING_FAILED = 2
    PROCESSING_DONE = 3
    '''
    Fired when one node is done.
    '''
    PROGRESS_UPDATE = 4
    START_PROCESSING = 5