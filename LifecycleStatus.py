from enum import Enum


class Status(Enum):
    IDLE = 1
    SESSION_STARTED = 2
    WAITING_PHASE = 3
    FOCUS_PHASE = 4
    RECORDING_PHASE = 5
    SESSION_ENDED = 6