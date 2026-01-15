from typing import Any
import nmiq
import SimpleITK as sitk
import os

from nmiq.tasks.bkgvar3d import bkgvar3d


def contrast_cyl3d(task_dict: dict[str, Any]):
    """
    Cylinder contrast task.
    Computes the contrast and activity ratio between a hot cylinder and
    background measured from the same geometry.
    The function takes a dictionary object as input, and the following keys
    must be present:
        image               --  The image to analyse (SimpleITK Image)
        start_z             --  The physical z-position of the start of the
                                cylinder
        end_z               --  The physical z-position of the end of the
                                cylinder
        cylinder_center_x   --  Approximate x-position of the cylinder center
        cylinder_center_y   --  Approximate y-position of the cylinder center
        background_center_x --  The x-position of the background center
        background_center_y --  The y-position of the background center
        cylinder_radius     --  The radius of the cylinder
        radius              --  The radius of the ROIs to use
        output_path         --  The path where output should be stored

    Given these inputs the function will automatically find the position of
    the cylinder (the position which gives the maximum signal for the hot
    cylinder) and compute the contrast and ratio to the background.
    The position of the cylinder is found slice by slice. On each slice a
    circle is drawn in a box in the region
        cylinder_center_x-radius <= x <= cylinder_center_x+radius
        cylinder_center_y-radius <= y <= cylinder_center_y+radius
    and this circle is placed to maximise the signal. The radius of the circle
    s always cylinder_radius.
    The position of the background cylinder is fixed to the input location.
    """

    print("Starting CONTRAST_CYL3D task.")
    print()

    # Get image
    img = task_dict['image']

    # Compute hot cylinder and background masks
    print("Placing hot cylinder.")
    hot_mask = nmiq.hottest_cylinder_3d(
        image=img,
        cylinder_start_z=task_dict['start_z'],
        cylinder_end_z=task_dict['end_z'],
        cylinder_center_x=task_dict['cylinder_center_x'],
        cylinder_center_y=task_dict['cylinder_center_y'],
        cylinder_radius=task_dict['cylinder_radius'],
        radius=task_dict['radius']
    )
    print("Placing background cylinder.")
    bkg_mask = nmiq.cylinder_3d(
        image_size=img.GetSize(),
        image_spacing=img.GetSpacing(),
        image_origin=img.GetOrigin(),
        cylinder_start_z=task_dict['start_z'],
        cylinder_end_z=task_dict['end_z'],
        cylinder_center_x=task_dict['background_center_x'],
        cylinder_center_y=task_dict['background_center_y'],
        cylinder_radius=task_dict['cylinder_radius'],
    )

    # Compute the mean voxel intensity in each cylinder
    label_stats_filter = sitk.LabelStatisticsImageFilter()
    
    label_stats_filter.Execute(img, hot_mask)
    hot_mean = label_stats_filter.GetMean(1)

    label_stats_filter.Execute(img, bkg_mask)
    bkg_mean = label_stats_filter.GetMean(1)
    
    # Compute contrast and ratio
    contrast = hot_mean / bkg_mean - 1.0

    # Write output
    print("Writing output.")
    hot_write_path = os.path.join(task_dict['output_path'],
                                   'contrast_cyl3d_hot.nii.gz')
    sitk.WriteImage(hot_mask, hot_write_path)

    bkg_write_path = os.path.join(task_dict['output_path'],
                                  'contrast_cyl3d_bkg.nii.gz')
    sitk.WriteImage(bkg_mask, bkg_write_path)


    res_file = os.path.join(task_dict['output_path'], 'contrast_cyl3d_res.txt')
    with open(res_file, 'w') as f:
        f.write(f"Contrast:\t{float(contrast)}\n")

    print("CONTRAST_CYL3D task completed.")
    print()
