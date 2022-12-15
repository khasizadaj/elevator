from enum import Enum


class Status(Enum):
    IDLE = 1  # no request, no passenger
    ASSIGNED = 2
    BUSY = 3  # has request, has passenger
    EMPTY = 4  # has request, no passenger


class Direction(Enum):
    UP = 1
    DOWN = -1
