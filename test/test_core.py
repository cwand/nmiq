import unittest
import nmiq.core
import os
import numpy as np
import SimpleITK as sitk
import numpy.typing as npt


class TestResampleImage(unittest.TestCase):

    def test_resample_3d_image(self):
        dcm_path = os.path.join(
            'test', 'data', '300',
            'Patient_unif290725_Study_1_Scan_5_Bed_1_Dyn_1.dcm')
        img = sitk.ReadImage(dcm_path)
        img2 = nmiq.resample_image(img, (1.0, 1.0, 1.0))
        self.assertEqual(img2.GetDimension(), 3)
        self.assertEqual(img2.GetSize()[0], 630)
        self.assertEqual(img2.GetSize()[1], 630)
        self.assertEqual(img2.GetSize()[2], 315)
        self.assertEqual(img2.GetOrigin()[0], -309.28)
        self.assertEqual(img2.GetOrigin()[1], -294.22)
        self.assertEqual(img2.GetOrigin()[2], 1017.57)
        self.assertEqual(img2.GetSpacing()[0], 1.0)
        self.assertEqual(img2.GetSpacing()[1], 1.0)
        self.assertEqual(img2.GetSpacing()[2], 1.0)

        self.assertAlmostEqual(
            img2.GetPixel(278, 287, 157), 56729.673, places=3)
        self.assertAlmostEqual(
            img2.GetPixel(340, 333, 140), 55230.714, places=3)


class TestJackknife(unittest.TestCase):

    def test_bkg_var(self):
        data = np.array([1.0, 2.0, 3.0])

        def func(x: npt.NDArray[np.float64]) -> float:
            return float(np.std(x, ddof=1)/np.mean(x))

        m, se = nmiq.jackknife(func, data)
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
        dcm_path = os.path.join(
            'test', 'data', '300',
            'Patient_unif290725_Study_1_Scan_5_Bed_1_Dyn_1.dcm')
        img = nmiq.load_images(dcm_path)
        self.assertEqual(3, img.GetDimension())
        self.assertEqual(128, img.GetSize()[0])
        self.assertEqual(128, img.GetSize()[1])
        self.assertEqual(64, img.GetSize()[2])
