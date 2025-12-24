import unittest
from nmiq import __main__
import os


class TestBkgVar3D_main(unittest.TestCase):

    def test_bkg_var_files(self):

        img_path = os.path.join('test', 'data', '300', 'Patient_unif290725_Study_1_Scan_5_Bed_1_Dyn_1.dcm')
        out_path = os.path.join('test')

        __main__.main(['bkgvar3d', '-i', img_path, '-o', out_path,
                       '--start_z', '1100', '--end_z', '1150',
                       '--center_x', '0', '--center_y', '0',
                       '--cyl_radius', '30', '--roi_radius', '20',])

        self.assertTrue(os.path.isfile(os.path.join(out_path, 'bkgvar3d_mask.nii.gz')))
        self.assertTrue(os.path.isfile(os.path.join(out_path, 'bkgvar3d_res.txt')))

    def tearDown(self):
        if os.path.exists(os.path.join('test', 'bkgvar3d_mask.nii.gz')):
            os.remove(os.path.join('test', 'bkgvar3d_mask.nii.gz'))
        if os.path.exists(os.path.join('test', 'bkgvar3d_res.txt')):
            os.remove(os.path.join('test', 'bkgvar3d_res.txt'))