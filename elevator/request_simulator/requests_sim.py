from typing import Generator

from request_simulator.request import Request

GeneratorOfRequests = Generator[Request, None, None]


class RequestSimulator:
    def __init__(self, requests: str) -> None:
        self.requests = requests

    def generate(self) -> GeneratorOfRequests:
        all_raw_requests = self.requests.replace(" ", "").split(",")
        for curr_request in all_raw_requests:
            yield self.process(curr_request)

    def process(self, request: str) -> Request:
        """
        Function processes the request string and return `Request` object.


        Args:
            request: string representation of request for the simulator
                example: 1 >> 5 @ 0

        """
        list_of_request_details = (
            request.replace(">>", "_").replace("@", "_").split("_")
        )
        start_level, end_level, requested_time = [
            int(detail) for detail in list_of_request_details
        ]

        return Request(start_level, end_level, requested_time)
