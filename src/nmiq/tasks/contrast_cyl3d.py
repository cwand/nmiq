from typing import Any
import nmiq
import SimpleITK as sitk
import os

from nmiq.tasks.bkgvar3d import bkgvar3d


def contrast_cyl3d(task_dict: dict[str, Any]):


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
    ratio = hot_mean / bkg_mean

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
        f.write(f"Ratio:\t{float(ratio)}\n")

    print("CONTRAST_CYL3D task completed.")
    print()
