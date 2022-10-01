import copy
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

    def assign(self, elevator: Elevator, request: Request) -> None:
        if elevator.status != Status.BUSY:
            elevator.set_busy()

        elevator.requests_pool.append(request)

    def extend_request(self, elevator: Elevator, request: Request) -> Request:
        """
        Extend request with finish time and start time.
        """

        if len(elevator.requests_pool) > 0:
            latest_request = elevator.requests_pool[-1]
            start_time, finish_time = request.calculate_times(
                elevator_processing_start_time=latest_request.finish_time,
                curr_elevator_level=elevator.current_level,
            )
        else:
            start_time, finish_time = request.calculate_times(
                elevator_processing_start_time=self.time,
                curr_elevator_level=elevator.current_level,
            )

        request.finish_time = finish_time
        request.travel_start_time = start_time

        return request

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
