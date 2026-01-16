import unittest
from nmiq import __main__
import os
import SimpleITK as sitk


class TestBkgVar3D_main(unittest.TestCase):

    def test_bkg_var_files(self):

        img_path = os.path.join(
            'test', 'data', '300',
            'Patient_unif290725_Study_1_Scan_5_Bed_1_Dyn_1.dcm')
        out_path = os.path.join('test')

        __main__.main(['bkgvar3d', '-i', img_path, '-o', out_path,
                       '--start_z', '1100', '--end_z', '1150',
                       '--center_x', '0', '--center_y', '0',
                       '--cyl_radius', '30', '--roi_radius', '20',])

        self.assertTrue(os.path.isfile(os.path.join(out_path,
                                                    'bkgvar3d_mask.nii.gz')))
        self.assertTrue(os.path.isfile(os.path.join(out_path,
                                                    'bkgvar3d_res.txt')))

    def test_resample(self):

        img_path = os.path.join(
            'test', 'data', '300',
            'Patient_unif290725_Study_1_Scan_5_Bed_1_Dyn_1.dcm')
        out_path = os.path.join('test')

        __main__.main(['bkgvar3d', '-i', img_path, '-o', out_path,
                       '--resample', '1,1,0',
                       '--start_z', '1100', '--end_z', '1150',
                       '--center_x', '0', '--center_y', '0',
                       '--cyl_radius', '30', '--roi_radius', '20'])

        img = sitk.ReadImage(os.path.join(out_path, 'bkgvar3d_mask.nii.gz'))
        self.assertEqual(1.0, img.GetSpacing()[0])
        self.assertEqual(1.0, img.GetSpacing()[1])
        self.assertAlmostEqual(4.92, img.GetSpacing()[2], places=6)

    def test_resample_correct_dimension(self):

        img_path = os.path.join(
            'test', 'data', '300',
            'Patient_unif290725_Study_1_Scan_5_Bed_1_Dyn_1.dcm')
        out_path = os.path.join('test')

        self.assertRaises(ValueError,
                          __main__.main,
                          ['bkgvar3d', '-i', img_path, '-o', out_path,
                           '--resample', '1,1,1,0',
                           '--start_z', '1100', '--end_z', '1150',
                           '--center_x', '0', '--center_y', '0',
                           '--cyl_radius', '30', '--roi_radius', '20'])

    def tearDown(self):
        if os.path.exists(os.path.join('test', 'bkgvar3d_mask.nii.gz')):
            os.remove(os.path.join('test', 'bkgvar3d_mask.nii.gz'))
        if os.path.exists(os.path.join('test', 'bkgvar3d_res.txt')):
            os.remove(os.path.join('test', 'bkgvar3d_res.txt'))


class TestLSF_main(unittest.TestCase):

    def test_fwhm_files(self):

        img_path = os.path.join(
            'test', 'data', 'res',
            'Patient_test20250806_Study_1_Scan_6_Bed_1_Dyn_20.dcm')
        out_path = os.path.join('test')

        __main__.main(['lsf', '-i', img_path, '-o', out_path,
                       '--start_z', '950', '--end_z', '1100',
                       '--delta_z', '30',
                       '--center_x', '10.9', '67.9',
                       '--center_y', '88.3', '14.5',
                       '--direction', 'x', 'y',
                       '--radius', '25', '25'])

        self.assertTrue(os.path.isfile(os.path.join(out_path,
                                                    'lsf_res.txt')))
        self.assertTrue(os.path.isfile(os.path.join(out_path,
                                                    'fwhm.png')))

    def tearDown(self):
        if os.path.exists(os.path.join('test', 'lsf_res.txt')):
            os.remove(os.path.join('test', 'lsf_res.txt'))
        if os.path.exists(os.path.join('test', 'fwhm.png')):
            os.remove(os.path.join('test', 'fwhm.png'))


class TestContrastCyl3D_main(unittest.TestCase):

    def test_contrast_files(self):

        img_path = os.path.join(
            'test', 'data', 'cyl',
            'Patient_phantomg9_220925_Study_6_Scan_5_Bed_1_Dyn_20.dcm')
        out_path = os.path.join('test')

        __main__.main(['contrast_cyl3d', '-i', img_path, '-o', out_path,
                       '--start_z', '1146', '--end_z', '1275',
                       '--cyl_center_x', '2.0',
                       '--cyl_center_y', '63.3',
                       '--bkg_center_x', '3.1',
                       '--bkg_center_y', '24.3',
                       '--cyl_radius', '12.0'])

        self.assertTrue(
            os.path.isfile(os.path.join(
                out_path, 'contrast_cyl3d_hot.nii.gz')))
        self.assertTrue(
            os.path.isfile(os.path.join(
                out_path, 'contrast_cyl3d_bkg.nii.gz')))
        self.assertTrue(
            os.path.isfile(os.path.join(out_path, 'contrast_cyl3d_res.txt')))

    def test_use_unresampled_for_search(self):

        img_path = os.path.join(
            'test', 'data', 'cyl',
            'Patient_phantomg9_220925_Study_6_Scan_5_Bed_1_Dyn_20.dcm')
        out_path = os.path.join('test')

        __main__.main(['contrast_cyl3d', '-i', img_path, '-o', out_path,
                       '--resample', '1,1,0',
                       '--start_z', '1156.2', '--end_z', '1190.7',
                       '--cyl_center_x', '6.3',
                       '--cyl_center_y', '57.3',
                       '--bkg_center_x', '5.4',
                       '--bkg_center_y', '-43.0',
                       '--cyl_radius', '12.0'])

        mask_hot = sitk.ReadImage(
            os.path.join(out_path, 'contrast_cyl3d_hot.nii.gz'))

        self.assertEqual(0, mask_hot[327, 350, 27])

    def tearDown(self):
        if os.path.exists(os.path.join('test', 'contrast_cyl3d_hot.nii.gz')):
            os.remove(os.path.join('test', 'contrast_cyl3d_hot.nii.gz'))
        if os.path.exists(os.path.join('test', 'contrast_cyl3d_bkg.nii.gz')):
            os.remove(os.path.join('test', 'contrast_cyl3d_bkg.nii.gz'))
        if os.path.exists(os.path.join('test', 'contrast_cyl3d_res.txt')):
            os.remove(os.path.join('test', 'contrast_cyl3d_res.txt'))
