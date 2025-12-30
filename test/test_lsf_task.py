import unittest
import nmiq.tasks.bkgvar3d
import SimpleITK as sitk
import os


class TestLSF_task(unittest.TestCase):

    def test_fwhm_file(self):

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

        self.assertTrue(False)