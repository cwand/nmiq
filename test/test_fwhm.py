import unittest
import nmiq.fwhm
import numpy as np


class TestNemaFWHMFromLineProfile(unittest.TestCase):

    def test_perfect_res(self):
        line = np.array([0.0, 0.0, 1.0, 0.0, 0.0])
        self.assertEqual(nmiq.fwhm.nema_fwhm_from_line_profile(line)[0], 1.0)

    def test_example_fwhm(self):
        line = np.array([1.0, 2.0, 4.0, 6.0, 7.75, 9.75, 9.75, 6.0, 4.0])
        self.assertEqual(nmiq.fwhm.nema_fwhm_from_line_profile(line)[0], 5.0)


class TestGaussfitFWHMFromLineProfile(unittest.TestCase):

    def test_example_fwhm(self):
        line = np.array([0.1, 0.3, 1.2, 1.1, 0.4])
        self.assertAlmostEqual(
            nmiq.fwhm.gaussfit_fwhm_from_line_profile(line, [1, 1, 1])[2],
            2.18388492, places=8)
