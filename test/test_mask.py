import unittest
import nmiq.mask



class TestSpheresInCylinder3D(unittest.TestCase):

    def test_mask_size(self):
        img = nmiq.mask.spheres_in_cylinder_3d(
            image_size = (3, 3, 3),
            image_spacing = (1, 1, 1),
            image_origin = (0, 0, 0),
            cylinder_start_z = 1.0,
            cylinder_end_z = 2.5,
            cylinder_center_x = 1.5,
            cylinder_center_y = 1.5,
            cylinder_radius = 1,
            roi_radius = 0.6
        )
        self.assertEqual(3, img.GetDimension())
        self.assertEqual((1, 1, 1), img.GetSpacing())
        self.assertEqual((0, 0, 0), img.GetOrigin())
        self.assertEqual((3, 3, 3), img.GetSize())


    def test_mask_origin(self):
        img = nmiq.mask.spheres_in_cylinder_3d(
            image_size = (3, 3, 3),
            image_spacing = (1, 1, 1),
            image_origin = (1, 1, 1),
            cylinder_start_z = 2.0,
            cylinder_end_z = 3.5,
            cylinder_center_x = 2.5,
            cylinder_center_y = 2.5,
            cylinder_radius = 1.0,
            roi_radius = 0.6
        )
        self.assertEqual(3, img.GetDimension())
        self.assertEqual((1, 1, 1), img.GetSpacing())
        self.assertEqual((1, 1, 1), img.GetOrigin())
        self.assertEqual((3, 3, 3), img.GetSize())


    def test_mask_spacing(self):
        img = nmiq.mask.spheres_in_cylinder_3d(
            image_size = (3, 3, 3),
            image_spacing = (2, 2, 2),
            image_origin = (0, 0, 0),
            cylinder_start_z = 2.0,
            cylinder_end_z = 5.0,
            cylinder_center_x = 3.0,
            cylinder_center_y = 3.0,
            cylinder_radius = 2.0,
            roi_radius = 1.2
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
                          20, # Start z
                          60, # End z
                          100, # Center x
                          100, # Center y
                          30.0, # Cyl radius
                          20.1, # Roi radius
                          )

    def test_roi_fits_cylinder_radius(self):
        self.assertRaises(ValueError,
                          nmiq.mask.spheres_in_cylinder_3d,
                          (256, 256, 128),
                          (1.0, 1.0, 1.0),
                          (0, 0, 0),
                          20, # Start z
                          80, # End z
                          100, # Center x
                          100, # Center y
                          20.0, # Cyl radius
                          20.1, # Roi radius
                          )

    def test_cylinder_fits_image_x_left(self):
        self.assertRaises(ValueError,
                          nmiq.mask.spheres_in_cylinder_3d,
                          (256, 256, 128),
                          (1.0, 1.0, 1.0),
                          (0, 0, 0),
                          20, # Start z
                          80, # End z
                          9.4, # Center x
                          100, # Center y
                          10.0, # Cyl radius
                          1.0, # Roi radius
                          )

    def test_cylinder_fits_image_x_left(self):
        self.assertRaises(ValueError,
                          nmiq.mask.spheres_in_cylinder_3d,
                          (100, 100, 100),
                          (1.0, 1.0, 1.0),
                          (0, 0, 0),
                          20,  # Start z
                          80,  # End z
                          9.4,  # Center x
                          100,  # Center y
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

        self.assertEqual(img.GetPixel(5, 4, 3), 1) # Center pixel
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

