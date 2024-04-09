from enum import Enum


class Status(Enum):
    IDLE = 1
    SESSION_STARTED = 2
    WAITING_PHASE = 3
    FOCUS_PHASE = 4
    RECORDING_PHASE = 5
    SESSION_ENDED = 6


class StreamStatus(Enum):
    IDLE = 1
    SEARCHING = 2
    FOUND = 3
    NOT_FOUND = 4
