from pprint import pprint
from time import sleep

from elevator_simulator.elevator import Elevator
from elevator_simulator.elevator_sim import ElevatorSimulator
from request_simulator.requests_sim import RequestSimulator


def main():
    love = Elevator(name="love")
    relief = Elevator(name="relief")
    elevators = [love, relief]

    raw_requests = "1 >> 12 @ 0, 1 >> 2 @ 0, 1 >> 6 @ 2, 5 >> 6 @ 12, 6 >> 7 @ 20"
    requests = RequestSimulator(requests=raw_requests).generate()

    elevator_simulator = ElevatorSimulator(elevators=elevators)

    while True:
        new_request = next(requests, None)

        if elevator_simulator.has_ongoing_requests() is False and new_request is None:
            print("work done, lads!")
            break

        if new_request is not None:
            # TODO call elevator based on request time
            elevator, arrival_time = elevator_simulator.call(new_request)
            print(
                f"Go to elevator: {elevator.name.title()}. It will arrive in {arrival_time} second(s)."
            )

        elevator_simulator.update()
        print(elevator_simulator.time)

        # added for debugging purposes
        for elevator in elevator_simulator.elevators:
            print(
                f"There are {elevator.count_ongoing_requests()} ongoing requests for {elevator.name}."
            )
            for index, request in enumerate(elevator.get_ongoing_requests()):
                print(f"{index + 1}. {request}")

        # simulate waiting
        sleep(1)


if __name__ == "__main__":
    main()
