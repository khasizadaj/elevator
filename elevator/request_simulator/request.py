from dataclasses import dataclass

from config import ONE_LEVEL_DURATION


@dataclass()
class Request:
    start_level: int
    end_level: int
    requested_time: int
    _finish_time: int = -1  # time that request will be done
    _is_finished: bool = False

    # TODO update aaccording to the assigned time logic
    def finish_time(self, future_start_time: int = None) -> int:
        if future_start_time is not None:
            return future_start_time + self.length_of_travel

        return self.requested_time + self.length_of_travel

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
    def finish_time(self) -> int:
        return self._finish_time

    @finish_time.setter
    def finish_time(self, time: int) -> int:
        self._finish_time = time

    @property
    def length_of_travel(self):
        return (self.end_level - self.start_level) * ONE_LEVEL_DURATION
