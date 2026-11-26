import unittest

from counting_line import crosses_counting_line


class TestCrossesCountingLine(unittest.TestCase):
    def test_counts_vertical_crossing_inside_line(self):
        self.assertTrue(crosses_counting_line((700, 480), (700, 520)))

    def test_counts_diagonal_crossing_inside_line(self):
        self.assertTrue(crosses_counting_line((590, 480), (630, 520)))

    def test_accepts_left_endpoint(self):
        self.assertTrue(crosses_counting_line((600, 480), (600, 520)))

    def test_accepts_right_endpoint(self):
        self.assertTrue(crosses_counting_line((1000, 480), (1000, 520)))

    def test_ignores_crossing_left_of_line(self):
        self.assertFalse(crosses_counting_line((540, 480), (560, 520)))

    def test_ignores_crossing_right_of_line(self):
        self.assertFalse(crosses_counting_line((1020, 480), (1040, 520)))

    def test_ignores_upward_crossing(self):
        self.assertFalse(crosses_counting_line((700, 520), (700, 480)))

    def test_ignores_motion_without_crossing(self):
        self.assertFalse(crosses_counting_line((700, 420), (700, 480)))


if __name__ == "__main__":
    unittest.main()
