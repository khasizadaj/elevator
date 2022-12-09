import unittest

from request_simulator.request import Request

from elevator.elevator_simulator.elevator import Elevator
from elevator.elevator_simulator.elevator_sim import ElevatorSimulator
from elevator.request_simulator.requests_sim import RequestSimulator


class TestElevatorSimulator(unittest.TestCase):
    def setUp(self) -> None:
        love = Elevator(name="love")
        relief = Elevator(name="relief")
        elevators = [love, relief]

        self.elevator_simulator = ElevatorSimulator(elevators=elevators)
        request_1 = RequestSimulator.process("1 >> 4 @ 0")
        request_1 = self.elevator_simulator.extend_request(
            request=request_1, arrival_time=0
        )
        self.elevator_simulator.assign(elevator=love, request=request_1)

        self.elevator_simulator.time = 2
        request_2 = RequestSimulator.process("1 >> 4 @ 2")
        request_2 = self.elevator_simulator.extend_request(
            request=request_2, arrival_time=0
        )
        self.elevator_simulator.assign(elevator=relief, request=request_2)

        return super().setUp()

    def test_get_arrival_times(self):
        self.elevator_simulator.time = 4
        request_2 = RequestSimulator.process("2 >> 3 @ 4")

        arrival_times = self.elevator_simulator.get_arrival_times(request_2.start_level)
        arrival_times.sort(key=lambda x: x[1])

        first_best: tuple(Elevator, int) = arrival_times[0]
        second_best: tuple(Elevator, int) = arrival_times[1]
        self.assertEqual(first_best[0].name, "love")
        self.assertEqual(first_best[1], 16)
        self.assertEqual(second_best[0].name, "relief")
        self.assertEqual(second_best[1], 18)

    def test_find_available_elevator(self):
        self.elevator_simulator.time = 8
        request = RequestSimulator.process("3 >> 4 @ 8")

        elevator, arrival_time = self.elevator_simulator.find_available_elevator(
            request
        )
        self.assertEqual(elevator.name, "love")
        self.assertEqual(arrival_time, 8)

    def test_extend_request(self):
        self.elevator_simulator.time = 8
        request = RequestSimulator.process("3 >> 4 @ 8")
        extended_request = self.elevator_simulator.extend_request(
            request=request, arrival_time=8
        )
        self.assertEqual(extended_request.travel_start_time, 16)
        self.assertEqual(extended_request.finish_time, 20)


if __name__ == "__main__":
    unittest.main()
