from dataclasses import dataclass, field
from enum import Enum

from request_simulator.request import Request

from elevator_simulator.helper import Status


@dataclass()
class Elevator:
    name: str
    current_level: int = 1
    status: Status = Status.IDLE
    requests_pool: list[Request] = field(default_factory=lambda: [])
    _curr_request_pointer: int = 0

    def update(self, time: int) -> None:
        if self.has_ongoing_requests is False:
            if self.is_busy():
                self.set_idle()
            return

        curr_request = self.requests_pool[self.curr_request_pointer]
        if curr_request.finish_time <= time:
            curr_request.is_finished = True
            self.curr_request_pointer += 1

        if self.has_ongoing_requests is False:
            if self.is_busy():
                self.set_idle()
            return

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
    def curr_request_pointer(self) -> int:
        return self._curr_request_pointer

    @curr_request_pointer.setter
    def curr_request_pointer(self, new_pointer: int):
        self._curr_request_pointer = new_pointer

    @property
    def has_ongoing_requests(self):
        return self.count_ongoing_requests() != 0
