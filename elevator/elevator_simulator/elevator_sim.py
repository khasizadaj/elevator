from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from request_simulator.request import Request

from elevator_simulator.elevator import Elevator


class Status(Enum):
    IDLE = 1
    ASSIGNED = 2
    BUSY = 3


class ElevatorSimulator:
    def __init__(self, elevators: list[Elevator]) -> None:
        self.elevators = elevators
        self._time = 0

    def call(self, request: Request) -> Tuple[Elevator, int]:
        elevator, arrival_time = self.find_available_elevator()

        if elevator.status != Status.BUSY:
            elevator.set_busy()

        # calculate finish_time of request
        if len(elevator.requests_pool) > 0:
            request.finish_time = (
                elevator.requests_pool[-1].finish_time + request.length_of_travel
            )
        else:
            request.finish_time = self.time + request.length_of_travel

        elevator.requests_pool.append(request)
        return elevator, arrival_time

    def update(self) -> None:
        self.adjust_time()
        for elevator in self.elevators:
            elevator.update(self.time)

    def find_available_elevator(self) -> Tuple[Elevator, int]:
        """
        Function returns available elevator by assuming that elevator arriving
        faster than others are the better one.
        """
        arrival_times = self.get_arrival_times()
        arrival_times.sort(key=lambda x: x[1])

        return arrival_times[0]

    def get_arrival_times(self) -> Tuple[Elevator, int]:
        result = []
        for elevator in self.elevators:
            try:
                latest_request = elevator.requests_pool[-1]
                arrival_time = latest_request.finish_time - self.time
            except IndexError:
                arrival_time = 0

            result.append((elevator, arrival_time))

        return result

    def has_ongoing_requests(self) -> bool:
        return any([elevator.is_busy() for elevator in self.elevators])

    def adjust_time(self) -> int:
        self.time += 1
        return self.time

    @property
    def time(self) -> int:
        return self._time

    @time.setter
    def time(self, new_time: int):
        self._time = new_time
