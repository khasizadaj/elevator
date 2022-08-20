from time import sleep

from elevator_simulator.elevator import Elevator
from elevator_simulator.elevator_sim import ElevatorSimulator
from request_simulator.requests_sim import RequestSimulator


def main():
    love = Elevator(name="love")
    relief = Elevator(name="relief")
    elevators = [love, relief]

    raw_requests = "1 >> 2 @ 0, 1 >> 2 @ 0, 0 >> 2 @ 2, 3 >> 4 @ 3"
    request_simulator = RequestSimulator(requests=raw_requests)
    request_simulator.generate()

    elevator_simulator = ElevatorSimulator(elevators=elevators)

    while True:
        new_requests = request_simulator.next(elevator_simulator.time)

        if elevator_simulator.has_ongoing_requests() is False and new_requests is None:
            print("work done, lads!")
            break

        if new_requests is not None:
            for new_request in new_requests:
                print(
                    f"New request is recieved from level {new_request.start_level} to level {new_request.end_level}."
                )
                elevator, arrival_time = elevator_simulator.call(new_request)
                print(
                    f"\nGo to elevator: {elevator.name.title()}. It will arrive in {arrival_time} second(s)."
                )

        elevator_simulator.update()
        print(f"\n\n==\nTime: {elevator_simulator.time}\n")

        # added for debugging purposes
        for elevator in elevator_simulator.elevators:
            print(
                f"There are {elevator.count_ongoing_requests()} ongoing requests for {elevator.name}."
            )
            for index, new_request in enumerate(elevator.get_ongoing_requests()):
                print(f"{index + 1}. {new_request}")
                print(f"  {new_request.__repr__()}")
        # simulate waiting
        sleep(0.2)


if __name__ == "__main__":
    main()
