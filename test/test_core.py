import unittest
import nmiq.core


class TestAddThings(unittest.TestCase):

    def test_add_things(self):
        x = 3
        y = 4
        self.assertEqual(nmiq.add_things(x, y), 7)
