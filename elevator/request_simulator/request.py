from dataclasses import dataclass
from urllib import request

from config import ONE_LEVEL_DURATION


@dataclass()
class Request:
    start_level: int
    end_level: int
    requested_time: int
    progress = 0
    _travel_start_time = -1  # will be set when request is assigned
    _finish_time: int = -1  # time that request will be done
    _is_finished: bool = False

    def __repr__(self) -> str:
        return f"Request(start_level={self.start_level}, end_level={self.end_level}, requested_time={self.requested_time})"

    def __str__(self) -> str:
        return f"Request from level {self.start_level} to {self.end_level}. It is requested at second {self.requested_time} and will last for {self.finish_time - self.requested_time} second(s).)"

    @property
    def is_finished(self) -> bool:
        return self._is_finished

    @is_finished.setter
    def is_finished(self, status: bool):
        self._is_finished = status

    @property
    def travel_start_time(self):
        return self._travel_start_time

    @travel_start_time.setter
    def travel_start_time(self, start_time: int) -> None:
        self._travel_start_time = start_time

    @property
    def finish_time(self) -> int:
        return self._finish_time

    @finish_time.setter
    def finish_time(self, time: int) -> int:
        self._finish_time = time

    @property
    def length_of_travel(self):
        return abs(self.end_level - self.start_level) * ONE_LEVEL_DURATION

    def calculate_times(
        self, elevator_processing_start_time: int = 0, curr_elevator_level: int = 1
    ):
        """
        Function calculates finish time of the request based on the starting
        time of the request and current level of the elevator.

        TODO Consider door opening and closing.
        """
        elevator_reach_time = (
            abs(self.start_level - curr_elevator_level) * ONE_LEVEL_DURATION
        )
        request_finish_time = (
            elevator_processing_start_time + self.length_of_travel + elevator_reach_time
        )
        request_start_time = request_finish_time - self.length_of_travel
        return request_start_time, request_finish_time
