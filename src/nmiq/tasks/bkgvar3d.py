from typing import Any
import SimpleITK as sitk
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

    mask_write_path = os.path.join(task_dict['output_path'], 'bkgvar3d_mask.nii.gz')
    sitk.WriteImage(mask, mask_write_path)

    res_file = os.path.join(task_dict['output_path'], 'bkgvar3d_res.txt')
    with open(res_file, 'w') as f:
        f.write("Result:\tN/A\n")
        f.write("S.E.:\tN/A\n")
        f.write("K:\t1\n")