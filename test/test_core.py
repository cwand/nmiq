import unittest
import nmiq.core
import os
import numpy as np


class TestJackknife(unittest.TestCase):

    def test_bkg_var(self):
        data = np.array([1.0, 2.0, 3.0])
        f = lambda x: np.std(x, ddof=1)/np.mean(x)
        m, se = nmiq.jackknife(f, data)
        self.assertEqual(0.5, m)
        self.assertAlmostEqual(0.245452, se, places=6)




class TestLoadImages(unittest.TestCase):

    def test_load_dynamic_series_300(self):
        dcm_path = os.path.join('test', 'data', '300')
        img = nmiq.load_images(dcm_path)
        self.assertEqual(4, img.GetDimension())
        self.assertEqual(128, img.GetSize()[0])
        self.assertEqual(128, img.GetSize()[1])
        self.assertEqual(64, img.GetSize()[2])
        self.assertEqual(12, img.GetSize()[3])

    def test_load_dynamic_series_ct(self):
        dcm_path = os.path.join('test', 'data', 'CT')
        img = nmiq.load_images(dcm_path)
        self.assertEqual(3, img.GetDimension())
        self.assertEqual(512, img.GetSize()[0])
        self.assertEqual(512, img.GetSize()[1])
        self.assertEqual(132, img.GetSize()[2])

    def test_load_single_dcm_file(self):
        dcm_path = os.path.join('test', 'data', '300',
                                'Patient_unif290725_Study_1_Scan_5_Bed_1_Dyn_1.dcm')
        img = nmiq.load_images(dcm_path)
        self.assertEqual(3, img.GetDimension())
        self.assertEqual(128, img.GetSize()[0])
        self.assertEqual(128, img.GetSize()[1])
        self.assertEqual(64, img.GetSize()[2])

