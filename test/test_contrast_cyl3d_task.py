import unittest
import nmiq.tasks.contrast_cyl3d
import SimpleITK as sitk
import os


class TestContrastCyl3D_task(unittest.TestCase):

    def test_contrast_mask(self):
        src = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        src.SetSpacing((1, 1, 1))
        src.SetOrigin((0, 0, 0))

        src[2, 3, 2] = 1.0
        src[7, 7, 2] = 0.1
        src[2, 3, 3] = 1.1
        src[7, 7, 3] = 0.1
        src[2, 3, 4] = 0.9
        src[7, 7, 4] = 0.1
        src[2, 3, 5] = 1.0
        src[7, 7, 5] = 0.1

        task_dict = {
            'image': src,
            'start_z': 2.0,
            'end_z': 5.0,
            'cylinder_center_x': 3.0,
            'cylinder_center_y': 3.0,
            'background_center_x': 7.0,
            'background_center_y': 7.0,
            'cylinder_radius': 0.5,
            'radius': 2.0,
            'actual_ratio': 100.0,
            'output_path': os.path.join('test')
        }

        nmiq.tasks.contrast_cyl3d(task_dict)
        hot_mask = sitk.ReadImage(
            os.path.join('test', 'contrast_cyl3d_hot.nii.gz'))

        self.assertEqual(3, hot_mask.GetDimension())
        self.assertEqual((10, 10, 10), hot_mask.GetSize())
        self.assertEqual((1, 1, 1), hot_mask.GetSpacing())
        self.assertEqual((0, 0, 0), hot_mask.GetOrigin())

        self.assertEqual(0, hot_mask[2, 2, 1])
        self.assertEqual(0, hot_mask[2, 3, 1])
        self.assertEqual(0, hot_mask[3, 2, 1])
        self.assertEqual(0, hot_mask[3, 3, 1])

        self.assertEqual(0, hot_mask[2, 2, 2])
        self.assertEqual(1, hot_mask[2, 3, 2])
        self.assertEqual(0, hot_mask[3, 2, 2])
        self.assertEqual(0, hot_mask[3, 3, 2])

        self.assertEqual(0, hot_mask[2, 2, 3])
        self.assertEqual(1, hot_mask[2, 3, 3])
        self.assertEqual(0, hot_mask[3, 2, 3])
        self.assertEqual(0, hot_mask[3, 3, 3])

        self.assertEqual(0, hot_mask[2, 2, 4])
        self.assertEqual(1, hot_mask[2, 3, 4])
        self.assertEqual(0, hot_mask[3, 2, 4])
        self.assertEqual(0, hot_mask[3, 3, 4])

        self.assertEqual(0, hot_mask[2, 2, 5])
        self.assertEqual(1, hot_mask[2, 3, 5])
        self.assertEqual(0, hot_mask[3, 2, 5])
        self.assertEqual(0, hot_mask[3, 3, 5])

        self.assertEqual(0, hot_mask[2, 2, 6])
        self.assertEqual(0, hot_mask[2, 3, 6])
        self.assertEqual(0, hot_mask[3, 2, 6])
        self.assertEqual(0, hot_mask[3, 3, 6])

        bkg_mask = sitk.ReadImage(
            os.path.join('test', 'contrast_cyl3d_bkg.nii.gz'))

        self.assertEqual(3, bkg_mask.GetDimension())
        self.assertEqual((10, 10, 10), bkg_mask.GetSize())
        self.assertEqual((1, 1, 1), bkg_mask.GetSpacing())
        self.assertEqual((0, 0, 0), bkg_mask.GetOrigin())

        self.assertEqual(0, bkg_mask[6, 6, 1])
        self.assertEqual(0, bkg_mask[6, 7, 1])
        self.assertEqual(0, bkg_mask[7, 6, 1])
        self.assertEqual(0, bkg_mask[7, 7, 1])

        self.assertEqual(0, bkg_mask[6, 6, 2])
        self.assertEqual(0, bkg_mask[6, 7, 2])
        self.assertEqual(0, bkg_mask[7, 6, 2])
        self.assertEqual(1, bkg_mask[7, 7, 2])

        self.assertEqual(0, bkg_mask[6, 6, 3])
        self.assertEqual(0, bkg_mask[6, 7, 3])
        self.assertEqual(0, bkg_mask[7, 6, 3])
        self.assertEqual(1, bkg_mask[7, 7, 3])

        self.assertEqual(0, bkg_mask[6, 6, 4])
        self.assertEqual(0, bkg_mask[6, 7, 4])
        self.assertEqual(0, bkg_mask[7, 6, 4])
        self.assertEqual(1, bkg_mask[7, 7, 4])

        self.assertEqual(0, bkg_mask[6, 6, 5])
        self.assertEqual(0, bkg_mask[6, 7, 5])
        self.assertEqual(0, bkg_mask[7, 6, 5])
        self.assertEqual(1, bkg_mask[7, 7, 5])

        self.assertEqual(0, bkg_mask[6, 6, 6])
        self.assertEqual(0, bkg_mask[6, 7, 6])
        self.assertEqual(0, bkg_mask[7, 6, 6])
        self.assertEqual(0, bkg_mask[7, 7, 6])

    def test_contrast_result(self):
        src = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        src.SetSpacing((1, 1, 1))
        src.SetOrigin((0, 0, 0))

        src[2, 3, 2] = 1.0
        src[7, 7, 2] = 0.1
        src[2, 3, 3] = 1.1
        src[7, 7, 3] = 0.1
        src[2, 3, 4] = 0.9
        src[7, 7, 4] = 0.1
        src[2, 3, 5] = 1.0
        src[7, 7, 5] = 0.1

        task_dict = {
            'image': src,
            'start_z': 2.0,
            'end_z': 5.0,
            'cylinder_center_x': 3.0,
            'cylinder_center_y': 3.0,
            'background_center_x': 7.0,
            'background_center_y': 7.0,
            'cylinder_radius': 0.5,
            'radius': 2.0,
            'output_path': os.path.join('test')
        }

        nmiq.tasks.contrast_cyl3d(task_dict)
        with open(os.path.join('test', 'contrast_cyl3d_res.txt'), 'r') as f:
            lines = f.readlines()
            self.assertEqual(1, len(lines))
            line0 = lines[0].strip().split()
            self.assertEqual("Contrast:", line0[0])
            self.assertAlmostEqual(9.0, float(line0[1]), places=6)


    def tearDown(self):
        if os.path.exists(os.path.join('test', 'contrast_cyl3d_hot.nii.gz')):
            os.remove(os.path.join('test', 'contrast_cyl3d_hot.nii.gz'))
        if os.path.exists(os.path.join('test', 'contrast_cyl3d_bkg.nii.gz')):
            os.remove(os.path.join('test', 'contrast_cyl3d_bkg.nii.gz'))
        if os.path.exists(os.path.join('test', 'contrast_cyl3d_res.txt')):
            os.remove(os.path.join('test', 'contrast_cyl3d_res.txt'))