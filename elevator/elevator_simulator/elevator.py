from dataclasses import dataclass, field

from config import ONE_LEVEL_DURATION
from elevator_simulator.helper import Status
from request_simulator.request import Request


@dataclass()
class Elevator:
    name: str
    current_level: int = 1
    status: Status = Status.IDLE
    requests_pool: list[Request] = field(default_factory=lambda: [])
    _curr_request_pointer: int = 0

    # TODO Know current destinition of elevator

    def update(self, time: int) -> None:
        if self.has_ongoing_requests is False:
            if self.is_busy():
                self.set_idle()
            return

        self.update_current_level(time)

        if self.current_request.finish_time <= time:
            self.current_request.is_finished = True
            print(
                f'\n== Request for "{self.name}" from level {self.current_request.start_level} to {self.current_request.end_level} finished.\n'
            )
            self.curr_request_pointer += 1

            if self.has_ongoing_requests is False:
                if self.is_busy():
                    self.set_idle()
                return

    def update_current_level(self, time: int):
        progress_of_current_request = self.calculate_progress_of_current_request(
            time, self.current_request
        )
        if progress_of_current_request != 0:
            self.current_request.progress = progress_of_current_request

            if (
                self.current_request.start_level + progress_of_current_request
                >= self.current_level + 1
            ):
                self.current_level = (
                    self.current_request.start_level + progress_of_current_request
                )
                print(f'"{self.name}" arrived at level {self.current_level}')

    def set_idle(self):
        self.status = Status.IDLE

    def set_busy(self):
        self.status = Status.BUSY

    def is_busy(self):
        return self.status == Status.BUSY

    def is_idle(self):
        return self.status == Status.IDLE

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
        self, time: int, curr_request: Request
    ) -> int:
        """
        Function calculates how many levels has been passed so far for the
        current request.
        """
        progress_of_request = (
            time - curr_request.travel_start_time
        ) // ONE_LEVEL_DURATION

        return progress_of_request
