import unittest
import nmiq.tasks.lsf
import SimpleITK as sitk
import os


class TestLSF_task(unittest.TestCase):

    def test_fwhm_resfile(self):

        img = sitk.Image((100, 100, 100), sitk.sitkFloat32)
        img.SetSpacing((1, 1, 1))
        img.SetOrigin((0, 0, 0))

        task_dict = {
            'image': img,
            'start_z': 1.0,
            'end_z': 9.0,
            'delta_z': 6.0,
            'center_x': [20, 60],
            'center_y': [50, 30],
            'radius': [5, 5],
            'direction': ['x', 'y'],
            'output_path': os.path.join('test')
        }

        img.SetPixel(15, 51, 1, 1.0)
        img.SetPixel(16, 51, 1, 2.0)
        img.SetPixel(17, 51, 1, 4.0)
        img.SetPixel(18, 51, 1, 5.0)
        img.SetPixel(19, 51, 1, 7.0)  # FWHM (nema) = 3.09375
        img.SetPixel(20, 51, 1, 3.0)  # FWHM (gauss) = 3.97583030....
        img.SetPixel(21, 51, 1, 2.0)
        img.SetPixel(22, 51, 1, 1.0)
        img.SetPixel(23, 51, 1, 1.0)
        img.SetPixel(24, 51, 1, 0.0)
        img.SetPixel(25, 51, 1, 0.0)

        img.SetPixel(15, 48, 7, 0.0)
        img.SetPixel(16, 48, 7, 0.0)
        img.SetPixel(17, 48, 7, 1.0)
        img.SetPixel(18, 48, 7, 3.0)
        img.SetPixel(19, 48, 7, 8.0)
        img.SetPixel(20, 48, 7, 9.0)  # FWHM (nema) = 4.125
        img.SetPixel(21, 48, 7, 6.0)  # FWHM (gauss) = 4.36307488....
        img.SetPixel(22, 48, 7, 5.0)
        img.SetPixel(23, 48, 7, 4.0)
        img.SetPixel(24, 48, 7, 2.0)
        img.SetPixel(25, 48, 7, 0.0)

        img.SetPixel(60, 25, 1, 0.0)
        img.SetPixel(60, 26, 1, 1.0)
        img.SetPixel(60, 27, 1, 2.0)
        img.SetPixel(60, 28, 1, 3.0)
        img.SetPixel(60, 29, 1, 5.0)
        img.SetPixel(60, 30, 1, 6.0)
        img.SetPixel(60, 31, 1, 9.0)
        img.SetPixel(60, 32, 1, 10.0)  # FWHM (nema) = 4.9722222222....
        img.SetPixel(60, 33, 1, 8.0)   # FWHM (gauss) = 5.00906792....
        img.SetPixel(60, 34, 1, 5.0)
        img.SetPixel(60, 35, 1, 1.0)

        img.SetPixel(61, 25, 7, 0.0)
        img.SetPixel(61, 26, 7, 2.0)
        img.SetPixel(61, 27, 7, 5.0)
        img.SetPixel(61, 28, 7, 6.0)
        img.SetPixel(61, 29, 7, 12.0)  # FWHM (nema) = 1.85565476190...
        img.SetPixel(61, 30, 7, 5.0)   # FWHM (gauss) = 3.01677026....
        img.SetPixel(61, 31, 7, 2.0)
        img.SetPixel(61, 32, 7, 1.0)
        img.SetPixel(61, 33, 7, 0.0)
        img.SetPixel(61, 34, 7, 0.0)
        img.SetPixel(61, 35, 7, 0.0)

        nmiq.tasks.lsf(task_dict)

        with open(os.path.join('test', 'lsf_res.txt'), 'r') as f:
            lines = f.readlines()
            self.assertEqual(4, len(lines))
            line0 = lines[0].strip().split()
            self.assertEqual("NEMA:", line0[0])
            self.assertAlmostEqual(3.51165675, float(line0[1]), places=8)

            line1 = lines[1].strip().split()
            self.assertEqual("S.E.:", line1[0])
            self.assertAlmostEqual(0.67246, float(line1[1]), places=5)

            line2 = lines[2].strip().split()
            self.assertEqual("Gauss:", line2[0])
            self.assertAlmostEqual(4.09120, float(line2[1]), places=5)

            line3 = lines[3].strip().split()
            self.assertEqual("S.E.:", line3[0])
            self.assertAlmostEqual(0.41674, float(line3[1]), places=5)


    def test_fwhm_with_spacing_resfile(self):

        img = sitk.Image((100, 100, 100), sitk.sitkFloat32)
        img.SetSpacing((2, 5, 1))
        img.SetOrigin((0, 0, 0))

        task_dict = {
            'image': img,
            'start_z': 1.0,
            'end_z': 9.0,
            'delta_z': 6.0,
            'center_x': [40, 60],
            'center_y': [200, 400],
            'radius': [10, 25],
            'direction': ['x', 'y'],
            'output_path': os.path.join('test')
        }

        img.SetPixel(15, 41, 1, 1.0)
        img.SetPixel(16, 41, 1, 2.0)
        img.SetPixel(17, 41, 1, 4.0)
        img.SetPixel(18, 41, 1, 5.0)
        img.SetPixel(19, 41, 1, 7.0)  # FWHM = 3.09375 x 2
        img.SetPixel(20, 41, 1, 3.0)
        img.SetPixel(21, 41, 1, 2.0)
        img.SetPixel(22, 41, 1, 1.0)
        img.SetPixel(23, 41, 1, 1.0)
        img.SetPixel(24, 41, 1, 0.0)
        img.SetPixel(25, 41, 1, 0.0)

        img.SetPixel(15, 39, 7, 0.0)
        img.SetPixel(16, 39, 7, 0.0)
        img.SetPixel(17, 39, 7, 1.0)
        img.SetPixel(18, 39, 7, 3.0)
        img.SetPixel(19, 39, 7, 8.0)
        img.SetPixel(20, 39, 7, 9.0)  # FWHM = 4.125 x 2
        img.SetPixel(21, 39, 7, 6.0)
        img.SetPixel(22, 39, 7, 5.0)
        img.SetPixel(23, 39, 7, 4.0)
        img.SetPixel(24, 39, 7, 2.0)
        img.SetPixel(35, 39, 7, 0.0)

        img.SetPixel(30, 75, 1, 0.0)
        img.SetPixel(30, 76, 1, 1.0)
        img.SetPixel(30, 77, 1, 2.0)
        img.SetPixel(30, 78, 1, 3.0)
        img.SetPixel(30, 79, 1, 5.0)
        img.SetPixel(30, 80, 1, 6.0)
        img.SetPixel(30, 81, 1, 9.0)
        img.SetPixel(30, 82, 1, 10.0)  # FWHM = 4.9722222222.... x 5
        img.SetPixel(30, 83, 1, 8.0)
        img.SetPixel(30, 84, 1, 5.0)
        img.SetPixel(30, 85, 1, 1.0)

        img.SetPixel(31, 75, 7, 0.0)
        img.SetPixel(31, 76, 7, 2.0)
        img.SetPixel(31, 77, 7, 5.0)
        img.SetPixel(31, 78, 7, 6.0)
        img.SetPixel(31, 79, 7, 12.0)  # FWHM = 1.85565476190... x 5
        img.SetPixel(31, 80, 7, 5.0)
        img.SetPixel(31, 81, 7, 2.0)
        img.SetPixel(31, 82, 7, 1.0)
        img.SetPixel(31, 83, 7, 0.0)
        img.SetPixel(31, 84, 7, 0.0)
        img.SetPixel(31, 85, 7, 0.0)

        nmiq.tasks.lsf(task_dict)

        with open(os.path.join('test', 'lsf_res.txt'), 'r') as f:
            lines = f.readlines()
            self.assertEqual(4, len(lines))
            line0 = lines[0].strip().split()
            self.assertEqual("NEMA:", line0[0])
            self.assertAlmostEqual(12.14422123, float(line0[1]), places=8)

            line1 = lines[1].strip().split()
            self.assertEqual("S.E.:", line1[0])
            self.assertAlmostEqual(4.28739, float(line1[1]), places=5)

            line2 = lines[2].strip().split()
            self.assertEqual("Gauss:", line2[0])
            self.assertAlmostEqual(14.2018, float(line2[1]), places=4)

            line3 = lines[3].strip().split()
            self.assertEqual("S.E.:", line3[0])
            self.assertAlmostEqual(3.95191, float(line3[1]), places=5)

    def test_fwhm_image_file(self):
        img = sitk.Image((100, 100, 100), sitk.sitkFloat32)
        img.SetSpacing((1, 1, 1))
        img.SetOrigin((0, 0, 0))

        task_dict = {
            'image': img,
            'start_z': 1.0,
            'end_z': 9.0,
            'delta_z': 6.0,
            'center_x': [20, 60],
            'center_y': [50, 30],
            'radius': [5, 5],
            'direction': ['x', 'y'],
            'output_path': os.path.join('test')
        }

        img.SetPixel(15, 51, 1, 1.0)
        img.SetPixel(16, 51, 1, 2.0)
        img.SetPixel(17, 51, 1, 4.0)
        img.SetPixel(18, 51, 1, 5.0)
        img.SetPixel(19, 51, 1, 7.0)
        img.SetPixel(20, 51, 1, 3.0)
        img.SetPixel(21, 51, 1, 2.0)
        img.SetPixel(22, 51, 1, 1.0)
        img.SetPixel(23, 51, 1, 1.0)
        img.SetPixel(24, 51, 1, 0.0)
        img.SetPixel(25, 51, 1, 0.0)

        img.SetPixel(15, 48, 7, 0.0)
        img.SetPixel(16, 48, 7, 0.0)
        img.SetPixel(17, 48, 7, 1.0)
        img.SetPixel(18, 48, 7, 3.0)
        img.SetPixel(19, 48, 7, 8.0)
        img.SetPixel(20, 48, 7, 9.0)
        img.SetPixel(21, 48, 7, 6.0)
        img.SetPixel(22, 48, 7, 5.0)
        img.SetPixel(23, 48, 7, 4.0)
        img.SetPixel(24, 48, 7, 2.0)
        img.SetPixel(25, 48, 7, 0.0)

        img.SetPixel(60, 25, 1, 0.0)
        img.SetPixel(60, 26, 1, 1.0)
        img.SetPixel(60, 27, 1, 2.0)
        img.SetPixel(60, 28, 1, 3.0)
        img.SetPixel(60, 29, 1, 5.0)
        img.SetPixel(60, 30, 1, 6.0)
        img.SetPixel(60, 31, 1, 9.0)
        img.SetPixel(60, 32, 1, 10.0)
        img.SetPixel(60, 33, 1, 8.0)
        img.SetPixel(60, 34, 1, 5.0)
        img.SetPixel(60, 35, 1, 1.0)

        img.SetPixel(61, 25, 7, 0.0)
        img.SetPixel(61, 26, 7, 2.0)
        img.SetPixel(61, 27, 7, 5.0)
        img.SetPixel(61, 28, 7, 6.0)
        img.SetPixel(61, 29, 7, 12.0)
        img.SetPixel(61, 30, 7, 5.0)
        img.SetPixel(61, 31, 7, 2.0)
        img.SetPixel(61, 32, 7, 1.0)
        img.SetPixel(61, 33, 7, 0.0)
        img.SetPixel(61, 34, 7, 0.0)
        img.SetPixel(61, 35, 7, 0.0)

        nmiq.tasks.lsf(task_dict)

        self.assertTrue(os.path.isfile(os.path.join('test', 'fwhm.png')))


    def test_fwhm_errors_unequal_group_lengths(self):

        img = sitk.Image((100, 100, 100), sitk.sitkFloat32)
        img.SetSpacing((1, 1, 1))
        img.SetOrigin((0, 0, 0))

        task_dict = {
            'image': img,
            'start_z': 1.0,
            'end_z': 9.0,
            'delta_z': 6.0,
            'center_x': [20],
            'center_y': [50, 30],
            'radius': [5, 5],
            'direction': ['x', 'y'],
            'output_path': os.path.join('test')
        }

        self.assertRaises(ValueError, nmiq.tasks.lsf, task_dict)

        task_dict = {
            'image': img,
            'start_z': 1.0,
            'end_z': 9.0,
            'delta_z': 6.0,
            'center_x': [20, 60],
            'center_y': [50],
            'radius': [5, 5],
            'direction': ['x', 'y'],
            'output_path': os.path.join('test')
        }

        self.assertRaises(ValueError, nmiq.tasks.lsf, task_dict)

        task_dict = {
            'image': img,
            'start_z': 1.0,
            'end_z': 9.0,
            'delta_z': 6.0,
            'center_x': [20, 60],
            'center_y': [50, 30],
            'radius': [5],
            'direction': ['x', 'y'],
            'output_path': os.path.join('test')
        }

        self.assertRaises(ValueError, nmiq.tasks.lsf, task_dict)

        task_dict = {
            'image': img,
            'start_z': 1.0,
            'end_z': 9.0,
            'delta_z': 6.0,
            'center_x': [20, 60],
            'center_y': [50, 30],
            'radius': [5, 5],
            'direction': ['x'],
            'output_path': os.path.join('test')
        }

        self.assertRaises(ValueError, nmiq.tasks.lsf, task_dict)

    def test_unknown_direction(self):
        img = sitk.Image((100, 100, 100), sitk.sitkFloat32)
        img.SetSpacing((1, 1, 1))
        img.SetOrigin((0, 0, 0))

        task_dict = {
            'image': img,
            'start_z': 1.0,
            'end_z': 9.0,
            'delta_z': 6.0,
            'center_x': [20, 60],
            'center_y': [50, 30],
            'radius': [5, 5],
            'direction': ['z', 'y'],
            'output_path': os.path.join('test')
        }

        self.assertRaises(ValueError, nmiq.tasks.lsf, task_dict)

    def tearDown(self):
        if os.path.exists(os.path.join('test', 'lsf_res.txt')):
            os.remove(os.path.join('test', 'lsf_res.txt'))
        if os.path.exists(os.path.join('test', 'fwhm.png')):
            os.remove(os.path.join('test', 'fwhm.png'))
