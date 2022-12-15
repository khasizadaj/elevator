import sys
from time import sleep

from elevator_simulator.elevator import Elevator
from elevator_simulator.elevator_sim import ElevatorSimulator
from request_simulator.requests_sim import RequestSimulator


def main(requests_str: str):
    def print_dots():
        if elevator_simulator.time == 0:
            return

        print(
            (elevator_simulator.time % 4 if elevator_simulator.time % 4 != 0 else 4)
            * "."
        )

    # love = Elevator(name="love")
    # relief = Elevator(name="relief")
    # elevators = [love, relief]
    relief = Elevator(name="relief")
    elevators = [relief]

    request_simulator = RequestSimulator(requests=requests_str)
    request_simulator.generate()

    elevator_simulator = ElevatorSimulator(elevators=elevators)

    while True:
        print_dots()
        new_requests = request_simulator.next(elevator_simulator.time)

        if elevator_simulator.has_ongoing_requests() is False and new_requests is None:
            print("\n\n= Simulator update: All requests are finished.")
            break

        if new_requests is not None:
            for new_request in new_requests:
                print(
                    f"= Simulator update: New request is received from level {new_request.start_level} to level {new_request.end_level}."
                )
                elevator, arrival_time = elevator_simulator.find_available_elevator(
                    new_request
                )
                extended_request = elevator_simulator.extend_request(
                    new_request, arrival_time
                )
                elevator_simulator.assign(elevator, extended_request)
                print(
                    f'= Simulator update: Elevator "{elevator.name.title()}" will arrive in {arrival_time} second(s).'
                )

        elevator_simulator.update()
        elevator_simulator.adjust_time()

        if elevator_simulator.has_ongoing_requests() is False and new_requests is None:
            print("\n\n= Simulator update: All requests are finished.")
            break

        sleep(0.2)


if __name__ == "__main__":
    # args = sys.argv
    # main(args[1])
    args = "1 >> 4 @ 0, 2 >> 3 @ 12, 1 >> 4 @ 20, 4 >> 1 @ 32"
    main(args)
