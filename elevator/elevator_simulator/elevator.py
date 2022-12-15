from dataclasses import dataclass, field

from config import ONE_LEVEL_DURATION
from elevator_simulator.helper import Direction, Status
from request_simulator.request import Request


def get_direction(start_level: int, end_level: int):
    return Direction.UP if start_level < end_level else Direction.DOWN


@dataclass()
class Elevator:
    name: str
    current_level: int = 1
    status: Status = Status.IDLE
    requests_pool: list[Request] = field(default_factory=lambda: [])
    _curr_request_pointer: int = 0
    _direction: Direction = Direction.UP
    passenger_count: int = 0

    # TODO Know current destinition of elevator

    def update(self, time: int) -> None:
        if self.has_ongoing_requests is False:
            if self.is_busy() or self.is_empty():
                self.set_idle()
            return

        self.update_current_level(time)

        if self.current_request.finish_time <= time:
            self.current_request.is_finished = True
            print(
                f"= Elevator update - {self.name}: Finalized request from level {self.current_request.start_level} to {self.current_request.end_level}."
            )
            self.remove_passenger(1)
            self.set_empty()
            self.curr_request_pointer += 1

            if self.has_ongoing_requests is False:
                if self.is_busy() or self.is_empty():
                    self.set_idle()
                return

        if (
            self.current_request.travel_start_time == time
            and self.current_request.is_started is False
        ):
            print(
                f"= Elevator update - {self.name}: Started request from level {self.current_request.start_level} to level {self.current_request.end_level}). {self.current_request.passenger_count} passenger(s) is(are) on board."
            )
            self.current_request.is_started = True
            self.add_passenger(1)
            self.set_busy()

    def update_current_level(self, time: int):

        if self.is_empty():
            self.direction = get_direction(
                self.current_level, self.current_request.start_level
            )
            previous_request = self.requests_pool[self.curr_request_pointer - 1]
            progress_of_current_request = self.calculate_progress_of_current_request(
                time,
                previous_request.finish_time,
            )
        else:
            self.direction = self.current_request.direction
            progress_of_current_request = self.calculate_progress_of_current_request(
                time, self.current_request.travel_start_time
            )

        if progress_of_current_request == 0:
            return

        if progress_of_current_request == self.current_request.progress:
            return

        self.current_request.progress = progress_of_current_request

        self.current_level += self.direction.value

        print(
            f"= Elevator update - {self.name}: Elevator arrived at level {self.current_level}."
        )

    def set_idle(self):
        self.status = Status.IDLE

    def set_busy(self):
        self.status = Status.BUSY

    def set_empty(self):
        self.status = Status.EMPTY

    def is_busy(self):
        return self.status == Status.BUSY

    def is_idle(self):
        return self.status == Status.IDLE

    def is_empty(self):
        return self.status == Status.EMPTY

    def count_ongoing_requests(self):
        return len(self.get_ongoing_requests())

    def get_ongoing_requests(self):
        return [
            request for request in self.requests_pool if request.is_finished is False
        ]

    @property
    def current_request(self):
        return self.requests_pool[self.curr_request_pointer]

    @property
    def curr_request_pointer(self) -> int:
        return self._curr_request_pointer

    @curr_request_pointer.setter
    def curr_request_pointer(self, new_pointer: int):
        self._curr_request_pointer = new_pointer

    @property
    def has_ongoing_requests(self):
        return self.count_ongoing_requests() != 0

    def calculate_progress_of_current_request(
        self, time: int, travel_start_time: int
    ) -> int:
        """
        Function calculates how many levels has been passed so far for the
        current request.
        """
        progress_of_request = abs(time - travel_start_time) // ONE_LEVEL_DURATION

        return progress_of_request

    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, direction: Direction) -> None:
        self._direction = direction

    def add_passenger(self, count):
        self.passenger_count += count

    def remove_passenger(self, count):
        self.passenger_count -= count
