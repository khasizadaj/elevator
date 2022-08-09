from copy import deepcopy
from dataclasses import dataclass
from enum import Enum

from request_simulator.requests_sim import Request, RequestPool


class Status(Enum):
    IDLE = 1
    ASSIGNED = 2
    BUSY = 3


@dataclass()
class Elevator:
    name: str
    current_level: int = 1
    status: Status = Status.IDLE

    def update_state(self):
        if self.status.name == Status.IDLE:
            self.status = Status.BUSY

        self.status = Status.IDLE

    def set_idle(self):
        self.status = Status.IDLE

    def set_assigned(self):
        self.status = Status.ASSIGNED

    def set_busy(self):
        self.status = Status.BUSY


@dataclass()
class ElevatorSimulator:
    elevators: list[Elevator]
    requests_pool: RequestPool
    _time = 0

    def call(self, request: Request) -> str:
        elevator = self.find_available_elevator(request)
        elevator.set_assigned()
        print(f"status: {elevator.status}")
        print(f"status: {elevator.status == Status.IDLE}")

        # TODO find when is the starting time
        request.assigned_time = self.time

        self.requests_pool.add_pending((elevator, request))
        return elevator.name

    def update(self) -> None:
        self.adjust_time()
        self.requests_pool.update(self.time)

    def find_available_elevator(self, request: Request) -> Elevator:
        # TODO implement case that available elevator is further than not
        #      available one (will be in future)
        result = None
        for elevator in self.elevators:
            if elevator.status == Status.IDLE:
                result = elevator

        if result is None:
            result = self.find_next_elevator()

        return deepcopy(result)

    def find_next_elevator(self) -> Elevator:
        # TODO look for first elevator in request pool that will be available and return it
        return self.requests_pool.find_next_elevator()

    def adjust_time(self) -> int:
        self._time += 1
        return self.time

    @property
    def time(self):
        return self._time
