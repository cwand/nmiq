import unittest

import numpy as np
import SimpleITK as sitk

import nmiq.mask


class TestSpheresInCylinder3D(unittest.TestCase):

    def test_mask_size(self):
        img = nmiq.mask.spheres_in_cylinder_3d(
            image_size=(3, 3, 3),
            image_spacing=(1, 1, 1),
            image_origin=(0, 0, 0),
            cylinder_start_z=1.0,
            cylinder_end_z=2.49,
            cylinder_center_x=1.,
            cylinder_center_y=1.,
            cylinder_radius=1,
            roi_radius=0.6
        )
        self.assertEqual(3, img.GetDimension())
        self.assertEqual((1, 1, 1), img.GetSpacing())
        self.assertEqual((0, 0, 0), img.GetOrigin())
        self.assertEqual((3, 3, 3), img.GetSize())

    def test_mask_origin(self):
        img = nmiq.mask.spheres_in_cylinder_3d(
            image_size=(3, 3, 3),
            image_spacing=(1, 1, 1),
            image_origin=(1, 1, 1),
            cylinder_start_z=2.0,
            cylinder_end_z=3.49,
            cylinder_center_x=2.,
            cylinder_center_y=2.,
            cylinder_radius=1.0,
            roi_radius=0.6
        )
        self.assertEqual(3, img.GetDimension())
        self.assertEqual((1, 1, 1), img.GetSpacing())
        self.assertEqual((1, 1, 1), img.GetOrigin())
        self.assertEqual((3, 3, 3), img.GetSize())

    def test_mask_spacing(self):
        img = nmiq.mask.spheres_in_cylinder_3d(
            image_size=(3, 3, 3),
            image_spacing=(2, 2, 2),
            image_origin=(0, 0, 0),
            cylinder_start_z=2.0,
            cylinder_end_z=4.99,
            cylinder_center_x=2.99,
            cylinder_center_y=2.99,
            cylinder_radius=2.0,
            roi_radius=1.2
        )
        self.assertEqual(3, img.GetDimension())
        self.assertEqual((2, 2, 2), img.GetSpacing())
        self.assertEqual((0, 0, 0), img.GetOrigin())
        self.assertEqual((3, 3, 3), img.GetSize())

    def test_roi_fits_cylinder_length(self):
        self.assertRaises(ValueError,
                          nmiq.mask.spheres_in_cylinder_3d,
                          (256, 256, 128),
                          (1.0, 1.0, 1.0),
                          (0, 0, 0),
                          20,  # Start z
                          60,  # End z
                          100,  # Center x
                          100,  # Center y
                          30.0,  # Cyl radius
                          20.1,  # Roi radius
                          )

    def test_roi_fits_cylinder_radius(self):
        self.assertRaises(ValueError,
                          nmiq.mask.spheres_in_cylinder_3d,
                          (256, 256, 128),
                          (1.0, 1.0, 1.0),
                          (0, 0, 0),
                          20,  # Start z
                          80,  # End z
                          100,  # Center x
                          100,  # Center y
                          20.0,  # Cyl radius
                          20.1,  # Roi radius
                          )

    def test_cylinder_fits_image_x_left(self):
        self.assertRaises(ValueError,
                          nmiq.mask.spheres_in_cylinder_3d,
                          (256, 256, 128),
                          (1.0, 1.0, 1.0),
                          (0, 0, 0),
                          20,  # Start z
                          80,  # End z
                          9.4,  # Center x
                          100,  # Center y
                          10.0,  # Cyl radius
                          1.0,  # Roi radius
                          )

    def test_cylinder_fits_image_x_right(self):
        self.assertRaises(ValueError,
                          nmiq.mask.spheres_in_cylinder_3d,
                          (100, 100, 100),
                          (1.0, 1.0, 1.0),
                          (0, 0, 0),
                          20,  # Start z
                          80,  # End z
                          89.6,  # Center x
                          50,  # Center y
                          10.0,  # Cyl radius
                          1.0,  # Roi radius
                          )

    def test_cylinder_fits_image_y_top(self):
        self.assertRaises(ValueError,
                          nmiq.mask.spheres_in_cylinder_3d,
                          (100, 100, 100),
                          (1.0, 1.0, 1.0),
                          (0, 0, 0),
                          20,  # Start z
                          80,  # End z
                          50,  # Center x
                          9.4,  # Center y
                          10.0,  # Cyl radius
                          1.0,  # Roi radius
                          )

    def test_cylinder_fits_image_y_bottom(self):
        self.assertRaises(ValueError,
                          nmiq.mask.spheres_in_cylinder_3d,
                          (100, 100, 100),
                          (1.0, 1.0, 1.0),
                          (0, 0, 0),
                          20,  # Start z
                          80,  # End z
                          50,  # Center x
                          89.6,  # Center y
                          10.0,  # Cyl radius
                          1.0,  # Roi radius
                          )

    def test_cylinder_fits_image_z_start(self):
        self.assertRaises(ValueError,
                          nmiq.mask.spheres_in_cylinder_3d,
                          (100, 100, 100),
                          (1.0, 1.0, 1.0),
                          (0, 0, 40),
                          39,  # Start z
                          100,  # End z
                          50,  # Center x
                          50,  # Center y
                          10.0,  # Cyl radius
                          1.0,  # Roi radius
                          )

    def test_cylinder_fits_image_z_end(self):
        self.assertRaises(ValueError,
                          nmiq.mask.spheres_in_cylinder_3d,
                          (100, 100, 100),
                          (1.0, 1.0, 1.0),
                          (0, 0, 40),
                          50,  # Start z
                          139.6,  # End z
                          50,  # Center x
                          50,  # Center y
                          10.0,  # Cyl radius
                          1.0,  # Roi radius
                          )

    def test_single_sphere(self):
        img = nmiq.mask.spheres_in_cylinder_3d(
            image_size=(9, 9, 7),
            image_spacing=(1, 1, 1),
            image_origin=(0, 0, 0),
            cylinder_start_z=1.0,
            cylinder_end_z=5.5,
            cylinder_center_x=5.0,
            cylinder_center_y=4.0,
            cylinder_radius=3.0,
            roi_radius=2.0
        )

        self.assertEqual(3, img.GetDimension())
        self.assertEqual((1, 1, 1), img.GetSpacing())
        self.assertEqual((0, 0, 0), img.GetOrigin())
        self.assertEqual((9, 9, 7), img.GetSize())

        self.assertEqual(img.GetPixel(5, 4, 3), 1)  # Center pixel
        self.assertEqual(img.GetPixel(6, 4, 3), 1)
        self.assertEqual(img.GetPixel(7, 4, 3), 1)
        self.assertEqual(img.GetPixel(8, 4, 3), 0)

        self.assertEqual(img.GetPixel(6, 3, 3), 1)
        self.assertEqual(img.GetPixel(6, 2, 3), 0)
        self.assertEqual(img.GetPixel(7, 4, 3), 1)
        self.assertEqual(img.GetPixel(7, 5, 3), 0)

        self.assertEqual(img.GetPixel(6, 3, 2), 1)
        self.assertEqual(img.GetPixel(7, 3, 2), 0)
        self.assertEqual(img.GetPixel(4, 3, 4), 1)
        self.assertEqual(img.GetPixel(4, 4, 4), 1)
        self.assertEqual(img.GetPixel(5, 5, 5), 0)
        self.assertEqual(img.GetPixel(5, 4, 1), 1)
        self.assertEqual(img.GetPixel(5, 4, 0), 0)

    def test_four_spheres(self):
        img = nmiq.mask.spheres_in_cylinder_3d(
            image_size=(19, 19, 19),
            image_spacing=(1, 1, 1),
            image_origin=(0, 0, 0),
            cylinder_start_z=1.0,
            cylinder_end_z=8.0,
            cylinder_center_x=9.0,
            cylinder_center_y=9.0,
            cylinder_radius=8.0,
            roi_radius=3.0
        )

        self.assertEqual(3, img.GetDimension())
        self.assertEqual((1, 1, 1), img.GetSpacing())
        self.assertEqual((0, 0, 0), img.GetOrigin())
        self.assertEqual((19, 19, 19), img.GetSize())

        self.assertEqual(4, np.max(sitk.GetArrayFromImage(img)))

        # Sphere 1
        self.assertEqual(img.GetPixel(9, 4, 4), 1)  # Center voxel
        self.assertEqual(img.GetPixel(12, 3, 4), 0)
        self.assertEqual(img.GetPixel(11, 3, 3), 1)
        self.assertEqual(img.GetPixel(10, 6, 3), 1)
        self.assertEqual(img.GetPixel(7, 5, 2), 1)
        self.assertEqual(img.GetPixel(7, 6, 2), 0)

        # Sphere 2
        self.assertEqual(img.GetPixel(4, 9, 4), 2)  # Center voxel
        self.assertEqual(img.GetPixel(5, 8, 3), 2)
        self.assertEqual(img.GetPixel(2, 11, 6), 0)
        self.assertEqual(img.GetPixel(5, 8, 7), 0)
        self.assertEqual(img.GetPixel(6, 11, 5), 2)

        # Sphere 3
        self.assertEqual(img.GetPixel(9, 14, 4), 3)  # Center voxel
        self.assertEqual(img.GetPixel(8, 13, 3), 3)
        self.assertEqual(img.GetPixel(10, 16, 3), 3)
        self.assertEqual(img.GetPixel(6, 16, 5), 0)
        self.assertEqual(img.GetPixel(10, 13, 7), 0)

        # Sphere 4
        self.assertEqual(img.GetPixel(14, 9, 4), 4)  # Center voxel
        self.assertEqual(img.GetPixel(13, 10, 3), 4)
        self.assertEqual(img.GetPixel(12, 11, 6), 0)
        self.assertEqual(img.GetPixel(12, 10, 3), 4)
        self.assertEqual(img.GetPixel(11, 9, 4), 4)
        self.assertEqual(img.GetPixel(11, 9, 5), 0)

    def test_four_spheres_in_row(self):
        img = nmiq.mask.spheres_in_cylinder_3d(
            image_size=(6, 6, 16),
            image_spacing=(1, 1, 1),
            image_origin=(0, 0, 0),
            cylinder_start_z=1.0,
            cylinder_end_z=13.0,
            cylinder_center_x=3.0,
            cylinder_center_y=3.0,
            cylinder_radius=1.5,
            roi_radius=0.9
        )

        self.assertEqual(3, img.GetDimension())
        self.assertEqual((1, 1, 1), img.GetSpacing())
        self.assertEqual((0, 0, 0), img.GetOrigin())
        self.assertEqual((6, 6, 16), img.GetSize())

        self.assertEqual(4, np.max(sitk.GetArrayFromImage(img)))

        self.assertEqual(img.GetPixel(3, 3, 0), 0)
        self.assertEqual(img.GetPixel(3, 3, 1), 1)
        self.assertEqual(img.GetPixel(3, 3, 2), 1)
        self.assertEqual(img.GetPixel(3, 3, 3), 0)
        self.assertEqual(img.GetPixel(3, 3, 4), 2)
        self.assertEqual(img.GetPixel(3, 3, 5), 2)
        self.assertEqual(img.GetPixel(3, 3, 6), 0)
        self.assertEqual(img.GetPixel(3, 3, 7), 3)
        self.assertEqual(img.GetPixel(3, 3, 8), 3)
        self.assertEqual(img.GetPixel(3, 3, 9), 0)
        self.assertEqual(img.GetPixel(3, 3, 10), 4)
        self.assertEqual(img.GetPixel(3, 3, 11), 4)
        self.assertEqual(img.GetPixel(3, 3, 12), 0)
        self.assertEqual(img.GetPixel(3, 3, 13), 0)
        self.assertEqual(img.GetPixel(3, 3, 14), 0)
        self.assertEqual(img.GetPixel(3, 3, 15), 0)

    def test_concentric_cylinders(self):
        img = nmiq.mask.spheres_in_cylinder_3d(
            image_size=(17, 17, 17),
            image_spacing=(1, 1, 1),
            image_origin=(0, 0, 0),
            cylinder_start_z=1.0,
            cylinder_end_z=7.0,
            cylinder_center_x=8.0,
            cylinder_center_y=8.0,
            cylinder_radius=7.0,
            roi_radius=1.0
        )

        self.assertEqual(3, img.GetDimension())
        self.assertEqual((1, 1, 1), img.GetSpacing())
        self.assertEqual((0, 0, 0), img.GetOrigin())
        self.assertEqual((17, 17, 17), img.GetSize())

        self.assertEqual(56, np.max(sitk.GetArrayFromImage(img)))


class TestHottestCylinder3D(unittest.TestCase):

    def test_mask_size(self):
        src = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        src.SetSpacing((1, 1, 1))
        src.SetOrigin((0, 0, 0))
        src[2, 3, 2] = 1.0
        src[2, 3, 3] = 1.1
        src[2, 3, 4] = 1.2
        src[2, 3, 5] = 1.1
        mask = nmiq.mask.hottest_cylinder_3d(
            image=src,
            cylinder_start_z=2.0,
            cylinder_end_z=5.0,
            cylinder_center_x=2.0,
            cylinder_center_y=3.0,
            cylinder_radius=1.0,
            radius=1.0
        )
        self.assertEqual(3, mask.GetDimension())
        self.assertEqual((1, 1, 1), mask.GetSpacing())
        self.assertEqual((0, 0, 0), mask.GetOrigin())
        self.assertEqual((10, 10, 10), mask.GetSize())

    def test_cylinder_fits_inside_image_x_left(self):
        src = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        src.SetSpacing((1, 1, 1))
        src.SetOrigin((0, 0, 0))
        src[2, 3, 2] = 1.0
        src[2, 3, 3] = 1.1
        src[2, 3, 4] = 1.2
        src[2, 3, 5] = 1.1

        self.assertRaises(ValueError, nmiq.mask.hottest_cylinder_3d,
                          **{'image': src,
                             'cylinder_start_z': 2.0,
                             'cylinder_end_z': 5.0,
                             'cylinder_center_x': 2.0,
                             'cylinder_center_y': 3.0,
                             'cylinder_radius': 2.6,
                             'radius': 1.0})

    def test_cylinder_fits_inside_image_x_right(self):
        src = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        src.SetSpacing((1, 1, 1))
        src.SetOrigin((0, 0, 0))
        src[8, 3, 2] = 1.0
        src[8, 3, 3] = 1.1
        src[8, 3, 4] = 1.2
        src[8, 3, 5] = 1.1

        self.assertRaises(ValueError, nmiq.mask.hottest_cylinder_3d,
                          **{'image': src,
                             'cylinder_start_z': 2.0,
                             'cylinder_end_z': 5.0,
                             'cylinder_center_x': 8.0,
                             'cylinder_center_y': 3.0,
                             'cylinder_radius': 2.6,
                             'radius': 1.0})

    def test_cylinder_fits_inside_image_y_top(self):
        src = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        src.SetSpacing((1, 1, 1))
        src.SetOrigin((0, 0, 0))
        src[7, 2, 2] = 1.0
        src[7, 2, 3] = 1.1
        src[7, 2, 4] = 1.2
        src[7, 2, 5] = 1.1

        self.assertRaises(ValueError, nmiq.mask.hottest_cylinder_3d,
                          **{'image': src,
                             'cylinder_start_z': 2.0,
                             'cylinder_end_z': 5.0,
                             'cylinder_center_x': 7.0,
                             'cylinder_center_y': 2.0,
                             'cylinder_radius': 2.6,
                             'radius': 1.0})

    def test_cylinder_fits_inside_image_y_bottom(self):
        src = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        src.SetSpacing((1, 1, 1))
        src.SetOrigin((0, 0, 0))
        src[6, 7, 2] = 1.0
        src[6, 7, 3] = 1.1
        src[6, 7, 4] = 1.2
        src[6, 7, 5] = 1.1

        self.assertRaises(ValueError, nmiq.mask.hottest_cylinder_3d,
                          **{'image': src,
                             'cylinder_start_z': 2.0,
                             'cylinder_end_z': 5.0,
                             'cylinder_center_x': 6.0,
                             'cylinder_center_y': 7.0,
                             'cylinder_radius': 2.6,
                             'radius': 1.0})

    def test_cylinder_fits_inside_image_z_front(self):
        src = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        src.SetSpacing((1, 1, 1))
        src.SetOrigin((0, 0, 0))
        src[6, 6, 0] = 1.0
        src[6, 6, 1] = 1.1
        src[6, 6, 2] = 1.2
        src[6, 6, 3] = 1.1

        self.assertRaises(ValueError, nmiq.mask.hottest_cylinder_3d,
                          **{'image': src,
                             'cylinder_start_z': -0.6,
                             'cylinder_end_z': 3.0,
                             'cylinder_center_x': 6.0,
                             'cylinder_center_y': 6.0,
                             'cylinder_radius': 2.0,
                             'radius': 1.0})

    def test_cylinder_fits_inside_image_z_back(self):
        src = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        src.SetSpacing((1, 1, 1))
        src.SetOrigin((0, 0, 0))
        src[6, 6, 6] = 1.0
        src[6, 6, 7] = 1.1
        src[6, 6, 8] = 1.2
        src[6, 6, 9] = 1.1

        self.assertRaises(ValueError, nmiq.mask.hottest_cylinder_3d,
                          **{'image': src,
                             'cylinder_start_z': 6.0,
                             'cylinder_end_z': 9.5,
                             'cylinder_center_x': 6.0,
                             'cylinder_center_y': 6.0,
                             'cylinder_radius': 2.0,
                             'radius': 1.0})

    def test_mask_correct_values(self):
        src = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        src.SetSpacing((1, 1, 1))
        src.SetOrigin((0, 0, 0))
        src[6, 6, 2] = 1.0
        src[6, 7, 3] = 1.1
        src[7, 7, 4] = 1.2
        src[7, 6, 5] = 1.1
        mask = nmiq.mask.hottest_cylinder_3d(
            image=src,
            cylinder_start_z=2.0,
            cylinder_end_z=5.0,
            cylinder_center_x=6.0,
            cylinder_center_y=6.0,
            cylinder_radius=0.9,
            radius=2.0
        )

        self.assertEqual(np.max(mask), 1.0)
        self.assertEqual(np.max(mask[:, :, 0]), 0.0)
        self.assertEqual(np.max(mask[:, :, 1]), 0.0)

        self.assertEqual(mask[6, 6, 2], 1.0)
        self.assertEqual(mask[6, 7, 2], 0.0)
        self.assertEqual(mask[7, 6, 2], 0.0)
        self.assertEqual(mask[7, 7, 2], 0.0)

        self.assertEqual(mask[6, 6, 3], 0.0)
        self.assertEqual(mask[6, 7, 3], 1.0)
        self.assertEqual(mask[7, 6, 3], 0.0)
        self.assertEqual(mask[7, 7, 3], 0.0)

        self.assertEqual(mask[6, 6, 4], 0.0)
        self.assertEqual(mask[6, 7, 4], 0.0)
        self.assertEqual(mask[7, 6, 4], 0.0)
        self.assertEqual(mask[7, 7, 4], 1.0)

        self.assertEqual(mask[6, 6, 5], 0.0)
        self.assertEqual(mask[6, 7, 5], 0.0)
        self.assertEqual(mask[7, 6, 5], 1.0)
        self.assertEqual(mask[7, 7, 5], 0.0)

        self.assertEqual(np.max(mask[:, :, 6]), 0.0)
        self.assertEqual(np.max(mask[:, :, 7]), 0.0)
        self.assertEqual(np.max(mask[:, :, 8]), 0.0)
        self.assertEqual(np.max(mask[:, :, 9]), 0.0)

    def test_mask_correct_values_2(self):
        src = sitk.Image((10, 10, 10), sitk.sitkFloat32)
        src.SetSpacing((1, 1, 1))
        src.SetOrigin((0, 0, 0))

        src[1, 1, 2] = 1.0
        src[2, 1, 2] = 2.0
        src[3, 1, 2] = 2.0
        src[4, 1, 2] = 3.0
        src[5, 1, 2] = 2.0
        src[6, 1, 2] = 3.0
        src[7, 1, 2] = 1.0

        src[1, 2, 2] = 3.0
        src[2, 2, 2] = 5.0
        src[3, 2, 2] = 4.0
        src[4, 2, 2] = 4.0
        src[5, 2, 2] = 5.0
        src[6, 2, 2] = 2.0
        src[7, 2, 2] = 1.0
        src[8, 2, 2] = 1.0

        src[1, 3, 2] = 4.0
        src[2, 3, 2] = 9.0
        src[3, 3, 2] = 7.0
        src[4, 3, 2] = 7.0
        src[5, 3, 2] = 5.0
        src[6, 3, 2] = 2.0
        src[7, 3, 2] = 1.0
        src[8, 3, 2] = 2.0

        src[1, 4, 2] = 3.0
        src[2, 4, 2] = 5.0
        src[3, 4, 2] = 8.0
        src[4, 4, 2] = 8.0
        src[5, 4, 2] = 3.0
        src[6, 4, 2] = 4.0
        src[7, 4, 2] = 3.0
        src[8, 4, 2] = 1.0

        src[1, 5, 2] = 5.0
        src[2, 5, 2] = 6.0
        src[3, 5, 2] = 9.0
        src[4, 5, 2] = 6.0
        src[5, 5, 2] = 5.0
        src[6, 5, 2] = 5.0
        src[7, 5, 2] = 4.0
        src[8, 5, 2] = 2.0

        src[1, 6, 2] = 3.0
        src[2, 6, 2] = 4.0
        src[3, 6, 2] = 3.0
        src[4, 6, 2] = 5.0
        src[5, 6, 2] = 3.0
        src[6, 6, 2] = 2.0
        src[7, 6, 2] = 1.0

        src[1, 7, 2] = 2.0
        src[2, 7, 2] = 3.0
        src[3, 7, 2] = 1.0
        src[4, 7, 2] = 2.0
        src[5, 7, 2] = 1.0
        src[6, 7, 2] = 2.0
        src[7, 7, 2] = 2.0

        src[2, 8, 2] = 1.0
        src[3, 8, 2] = 2.0
        src[4, 8, 2] = 1.0
        src[5, 8, 2] = 1.0

        mask = nmiq.mask.hottest_cylinder_3d(
            image=src,
            cylinder_start_z=2.0,
            cylinder_end_z=5.0,
            cylinder_center_x=2.0,
            cylinder_center_y=3.0,
            cylinder_radius=1.5,
            radius=4.0
        )

        self.assertEqual(3, mask.GetDimension())
        self.assertEqual((1, 1, 1), mask.GetSpacing())
        self.assertEqual((0, 0, 0), mask.GetOrigin())
        self.assertEqual((10, 10, 10), mask.GetSize())

        data = sitk.GetArrayFromImage(mask)

        self.assertEqual(np.max(mask), 1.0)
        self.assertEqual(np.max(mask[0, :, :]), 0.0)
        self.assertEqual(np.max(mask[1, :, :]), 0.0)

        self.assertEqual(np.max(data[2, 0, :]), 0)
        self.assertEqual(np.max(data[2, 1, :]), 0)
        self.assertEqual(np.max(data[2, 2, :]), 0)
        self.assertEqual(mask[0, 3, 2], 0)
        self.assertEqual(mask[1, 3, 2], 0)
        self.assertEqual(mask[2, 3, 2], 1)
        self.assertEqual(mask[3, 3, 2], 1)
        self.assertEqual(mask[4, 3, 2], 1)
        self.assertEqual(mask[5, 3, 2], 0)
        self.assertEqual(mask[6, 3, 2], 0)
        self.assertEqual(mask[7, 3, 2], 0)
        self.assertEqual(mask[8, 3, 2], 0)
        self.assertEqual(mask[9, 3, 2], 0)
        self.assertEqual(mask[0, 4, 2], 0)
        self.assertEqual(mask[1, 4, 2], 0)
        self.assertEqual(mask[2, 4, 2], 1)
        self.assertEqual(mask[3, 4, 2], 1)
        self.assertEqual(mask[4, 4, 2], 1)
        self.assertEqual(mask[5, 4, 2], 0)
        self.assertEqual(mask[6, 4, 2], 0)
        self.assertEqual(mask[7, 4, 2], 0)
        self.assertEqual(mask[8, 4, 2], 0)
        self.assertEqual(mask[9, 4, 2], 0)
        self.assertEqual(mask[0, 5, 2], 0)
        self.assertEqual(mask[1, 5, 2], 0)
        self.assertEqual(mask[2, 5, 2], 1)
        self.assertEqual(mask[3, 5, 2], 1)
        self.assertEqual(mask[4, 5, 2], 1)
        self.assertEqual(mask[5, 5, 2], 0)
        self.assertEqual(mask[6, 5, 2], 0)
        self.assertEqual(mask[7, 5, 2], 0)
        self.assertEqual(mask[8, 5, 2], 0)
        self.assertEqual(mask[9, 5, 2], 0)
        self.assertEqual(np.max(data[2, 6, :]), 0)
        self.assertEqual(np.max(data[2, 7, :]), 0)
        self.assertEqual(np.max(data[2, 8, :]), 0)
        self.assertEqual(np.max(data[2, 9, :]), 0)

        self.assertEqual(np.max(mask[:, :, 3]), 0.0)
        self.assertEqual(np.max(mask[:, :, 4]), 0.0)
        self.assertEqual(np.max(mask[:, :, 5]), 0.0)
        self.assertEqual(np.max(mask[:, :, 6]), 0.0)
        self.assertEqual(np.max(mask[:, :, 7]), 0.0)
        self.assertEqual(np.max(mask[:, :, 8]), 0.0)
        self.assertEqual(np.max(mask[:, :, 9]), 0.0)
