from typing import Any
import SimpleITK as sitk
import numpy as np
import nmiq
import os

def bkgvar3d(task_dict: dict[str, Any]):
    img = task_dict['image']
    mask = nmiq.spheres_in_cylinder_3d(
        image_size=img.GetSize(),
        image_spacing=img.GetSpacing(),
        image_origin=img.GetOrigin(),
        cylinder_start_z=task_dict['cylinder_start_z'],
        cylinder_end_z=task_dict['cylinder_end_z'],
        cylinder_center_x=task_dict['cylinder_center_x'],
        cylinder_center_y=task_dict['cylinder_center_y'],
        cylinder_radius=task_dict['cylinder_radius'],
        roi_radius=task_dict['roi_radius']
    )

    max_label = np.max(sitk.GetArrayFromImage(mask))

    label_stats_filter = sitk.LabelStatisticsImageFilter()
    label_stats_filter.Execute(img, mask)
    means = np.zeros(max_label)
    for label in range(max_label):
        means[label] = label_stats_filter.GetMean(label + 1)

    bkg_var_func = lambda x: np.std(x, ddof=1) / np.mean(x)
    bkg_var, se = nmiq.jackknife(bkg_var_func, means)

    mask_write_path = os.path.join(task_dict['output_path'], 'bkgvar3d_mask.nii.gz')
    sitk.WriteImage(mask, mask_write_path)

    res_file = os.path.join(task_dict['output_path'], 'bkgvar3d_res.txt')
    with open(res_file, 'w') as f:
        f.write(f"Result:\t{float(bkg_var)}\n")
        f.write(f"S.E.:\t{float(se)}\n")
        f.write(f"K:\t{int(max_label)}\n")