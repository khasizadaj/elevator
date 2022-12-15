from enum import Enum
from typing import Tuple

from config import ONE_LEVEL_DURATION
from elevator_simulator.elevator import Elevator
from elevator_simulator.helper import Direction, Status
from request_simulator.request import Request


class ElevatorSimulator:
    def __init__(self, elevators: list[Elevator]) -> None:
        self.elevators = elevators
        self._time = 0

    def assign(self, elevator: Elevator, request: Request) -> None:
        # if elevator.status != Status.BUSY:
        #     elevator.set_busy()
        #     elevator.add_passenger(count=1)

        elevator.requests_pool.append(request)

    def extend_request(self, request: Request, arrival_time: int = 0) -> Request:
        """
        Extend request with finish time and start time.
        """

        request.travel_start_time = arrival_time + self.time
        request.finish_time = request.travel_start_time + request.length_of_travel

        return request

    def update(self) -> None:
        # self.adjust_time()
        for elevator in self.elevators:
            elevator.update(self.time)

    def find_available_elevator(self, new_request: Request) -> Tuple[Elevator, int]:
        """
        Function returns available elevator along with relative arrival time.

        Args:
            - new_request: newly arrived request

        Note:
            - Function assumes that elevator arriving faster than others is the
            best one.
        """

        arrival_times = self.get_arrival_times(new_request.start_level)
        arrival_times.sort(key=lambda x: x[1])

        return arrival_times[0]

    def get_arrival_times(self, new_request_start_level) -> list[Elevator, int]:
        result = []
        for elevator in self.elevators:
            try:
                latest_request = elevator.requests_pool[-1]

                arrival_time = (
                    abs(latest_request.end_level - new_request_start_level)
                    * ONE_LEVEL_DURATION
                )

                if elevator.has_ongoing_requests:
                    arrival_time += latest_request.finish_time - self.time

            except IndexError:
                arrival_time = 0

            result.append((elevator, arrival_time))

        return result

    def has_ongoing_requests(self) -> bool:
        return any([elevator.is_idle() is False for elevator in self.elevators])

    def adjust_time(self) -> int:
        self.time += 1
        return self.time

    @property
    def time(self) -> int:
        return self._time

    @time.setter
    def time(self, new_time: int):
        self._time = new_time
