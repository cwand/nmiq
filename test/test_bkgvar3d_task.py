import unittest
import nmiq.tasks.bkgvar3d
import SimpleITK as sitk
import os


class TestBkgVar3D_task(unittest.TestCase):

    def test_bkg_var_mask(self):

        img = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        img.SetSpacing((1, 1, 1))
        img.SetOrigin((0, 0, 0))

        task_dict = {
            'image': img,
            'cylinder_start_z': 1.0,
            'cylinder_end_z': 5.5,
            'cylinder_center_x': 5.0,
            'cylinder_center_y': 5.0,
            'cylinder_radius': 3.0,
            'roi_radius': 2.0,
            'output_path': os.path.join('test')
        }

        nmiq.tasks.bkgvar3d(task_dict)

        res_mask = sitk.ReadImage(os.path.join('test', 'bkgvar3d_mask.nii.gz'))

        self.assertEqual(3, res_mask.GetDimension())
        self.assertEqual((10, 10, 10), res_mask.GetSize())
        self.assertEqual((1, 1, 1), res_mask.GetSpacing())
        self.assertEqual((0, 0, 0), res_mask.GetOrigin())

        self.assertEqual(1, res_mask.GetPixel(5, 5, 3))
        self.assertEqual(1, res_mask.GetPixel(6, 5, 3))
        self.assertEqual(1, res_mask.GetPixel(7, 5, 3))
        self.assertEqual(0, res_mask.GetPixel(8, 5, 3))

        self.assertEqual(1, res_mask.GetPixel(5, 4, 3))
        self.assertEqual(1, res_mask.GetPixel(5, 3, 3))
        self.assertEqual(0, res_mask.GetPixel(5, 2, 3))

        self.assertEqual(1, res_mask.GetPixel(4, 4, 3))
        self.assertEqual(0, res_mask.GetPixel(4, 3, 3))

        self.assertEqual(1, res_mask.GetPixel(5, 4, 2))
        self.assertEqual(0, res_mask.GetPixel(5, 4, 1))

    def test_bkg_var_resfile(self):

        img = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        img.SetSpacing((1, 1, 1))
        img.SetOrigin((0, 0, 0))

        task_dict = {
            'image': img,
            'cylinder_start_z': 1.0,
            'cylinder_end_z': 5.5,
            'cylinder_center_x': 5.0,
            'cylinder_center_y': 5.0,
            'cylinder_radius': 3.0,
            'roi_radius': 2.0,
            'output_path': os.path.join('test')
        }

        nmiq.tasks.bkgvar3d(task_dict)

        with open(os.path.join('test', 'bkgvar3d_res.txt'), 'r') as f:
            lines = f.readlines()
            print(lines)
            self.assertEqual(3, len(lines))
            self.assertEqual("Result:\tN/A", lines[0].strip())
            self.assertEqual("S.E.:\tN/A", lines[1].strip())
            self.assertEqual("K:\t1", lines[2].strip())





    def tearDown(self):
        if os.path.exists(os.path.join('test', 'bkgvar3d_mask.nii.gz')):
            os.remove(os.path.join('test', 'bkgvar3d_mask.nii.gz'))
        if os.path.exists(os.path.join('test', 'bkgvar3d_res.txt')):
            os.remove(os.path.join('test', 'bkgvar3d_res.txt'))