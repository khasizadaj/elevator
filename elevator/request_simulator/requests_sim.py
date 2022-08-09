from dataclasses import dataclass
from re import A
from typing import Generator, Tuple

from config import ONE_LEVEL_DURATION


@dataclass()
class Request:
    start_level: int
    end_level: int
    requested_time: int
    _assigned_time: int = -1  # time that elevator will pick up person
    _finish_time: int = -1  # time that elevator will finish the task

    # TODO update aaccording to the assigned time logic
    def finish_time(self, future_start_time: int = None) -> int:
        length_of_travel = (self.end_level - self.start_level) * ONE_LEVEL_DURATION
        if future_start_time is not None:
            return future_start_time + length_of_travel

        return self.requested_time + length_of_travel

    def __repr__(self) -> str:
        return f"Request(start_level={self.start_level}, end_level={self.end_level}, requested_time={self.start_level}, assigned_time={self.assigned_time})"

    def __str__(self) -> str:
        return f"Request(start_level={self.start_level}, end_level={self.end_level}, requested_time={self.start_level}, assigned_time={self.assigned_time}, finish_time={self.finish_time()})"

    @property
    def assigned_time(self) -> int:
        return self._assigned_time

    @assigned_time.setter
    def assigned_time(self, time: int):
        self._assigned_time = time

    @property
    def finish_time(self) -> int:
        return self._finish_time

    @finish_time.setter
    def finish_time(self, time: int) -> int:
        self._finish_time = time


class RequestPool:
    _in_progress_requests = []
    _pending_requests = []

    def add(self, assigned_request: Tuple) -> None:
        self.in_progress_requests.append(assigned_request)
        self.in_progress_requests.sort(key=self.get_finish_time)

    def add_pending(self, pending_request: Tuple) -> None:
        self.pending_requests.append(pending_request)

    @property
    def in_progress_requests(self):
        return self._in_progress_requests

    @property
    def pending_requests(self):
        return self._pending_requests

    @staticmethod
    def get_finish_time(aassigned_request: Tuple) -> int:
        raw_request: Request = aassigned_request[1]
        return raw_request.finish_time()

    def update(self, time: int):
        if len(self.in_progress_requests) > 0:
            elevator, request = (
                self.in_progress_requests[0][0],
                self.in_progress_requests[0][1],
            )
            if time >= request.finish_time():
                del self.in_progress_requests[0]

        if len(self.pending_requests) > 0:
            # we use FIFO. first added will be moved to started requests
            elevator = self.pending_requests[0][0]
            request = self.pending_requests[0][1]
            if elevator.name not in [el.name for el, _ in self.in_progress_requests]:
                elevator.set_busy()
                self.add((elevator, request))
                del self.pending_requests[0]

    def find_next_elevator(self) -> "Elevator":
        return self.pending_requests[0][0]

    def has_request(self):
        return (len(self.pending_requests) + len(self.in_progress_requests)) != 0

    def all_requests(self):
        return self.in_progress_requests + self.pending_requests


class RequestSimulator:
    def __init__(self, requests: str) -> None:
        self.requests = requests

    def generate(self) -> Generator[Request, None, None]:
        all_raw_requests = self.requests.replace(" ", "").split(",")
        for curr_request in all_raw_requests:
            yield self.process(curr_request)

    def process(self, request: str) -> Request:
        # 1 >> 5 @ 0
        list_of_request_details = (
            request.replace(">>", "_").replace("@", "_").split("_")
        )
        list_of_request_details = [int(detail) for detail in list_of_request_details]

        return Request(*list_of_request_details)
