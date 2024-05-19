
from enum import Enum


class RMQEvent(Enum):
    NODE_FAILED = 1
    PROCESSING_FAILED = 2
    PROCESSING_DONE = 3
    '''
    Fired when progress is updated.
    '''
    PROGRESS_UPDATE = 4
    START_PROCESSING = 5
    '''
    Fired when a node finishes processing.
    '''
    NODE_DONE = 6

    '''
    Fired when processing of a specific image starts.
    '''
    PROCESSING_STARTED = 7
    ADD_NODE = 8
    REMOVE_NODE = 9