import unittest

1
from request_simulator.request import Request


class TestRequests(unittest.TestCase):
    # def test_calculate_finish_time(self):
    #     request = Request(start_level=1, end_level=4, requested_time=0)

    #     self.assertEqual(request.calculate_finish_time(0, 1), 12)

    def test_calculate_finish_time_different_level(self):
        request = Request(start_level=5, end_level=3, requested_time=0)
        self.assertEqual(request.calculate_finish_time(0, 2), 20)

    def test_calculate_finish_time_different_time(self):
        request = Request(start_level=5, end_level=3, requested_time=4)
        self.assertEqual(request.calculate_finish_time(6, 5), 14)

    def test_calculate_finish_time_different_time_and_level(self):
        request = Request(start_level=5, end_level=3, requested_time=6)
        self.assertEqual(request.calculate_finish_time(8, 2), 28)


if __name__ == "__main__":
    unittest.main()
