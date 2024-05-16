
from enum import Enum


class ZeroMQEvent(Enum):
    NODE_FAILED = 1
    PROCESSING_FAILED = 2
    PROCESSING_DONE = 3
    PROGRESS_UPDATE = 4
    START_PROCESSING = 5