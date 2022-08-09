from pprint import pprint
from time import sleep

from elevator_simulator.elevator_sim import Elevator, ElevatorSimulator
from request_simulator.requests_sim import RequestPool, RequestSimulator


def main():
    love = Elevator(name="love")
    # relief = Elevator(name="relief")
    # joy = Elevator(name="joy")
    elevators = [love]
    # pride = Elevator(name="pride")
    # excitement = Elevator(name="excitement")
    # elevators = [love, relief, joy, pride, excitement]

    # raw_requests = "1 >> 12 @ 0, 1 >> 2 @ 0, 1 >> 6 @ 2, 5 >> 6 @ 12, 6 >> 7 @ 20"
    raw_requests = "1 >> 3 @ 0, 2 >> 4 @ 0"  # 2 people goes to same place
    requests = RequestSimulator(requests=raw_requests).generate()

    requests_pool = RequestPool()
    elevator_simulator = ElevatorSimulator(
        elevators=elevators, requests_pool=requests_pool
    )

    while True:
        new_request = next(requests, None)

        if requests_pool.has_request() is False and new_request is None:
            print("work done, lads!")
            break

        if new_request is not None:
            message = elevator_simulator.call(new_request)
            print(f"Go to elevator: {message.title()}.")

        elevator_simulator.update()
        print(elevator_simulator.time)

        for (
            in_progress_request
        ) in elevator_simulator.requests_pool.in_progress_requests:
            pprint(in_progress_request[0])
            pprint(in_progress_request[1])
        for pending_request in elevator_simulator.requests_pool.pending_requests:
            pprint(pending_request[0])
            pprint(pending_request[1])
        sleep(0.5)

    # for assigned_request in elevator_simulator.requests_pool.in_progress_requests:
    #     print(assigned_request[0], assigned_request[1])


if __name__ == "__main__":
    main()
