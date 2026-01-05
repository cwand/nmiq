from typing import Any
import SimpleITK as sitk
import nmiq
import os
import numpy as np


def lsf(task_dict: dict[str, Any]):

    img = task_dict['image']
    img_data = sitk.GetArrayFromImage(img)

    z = task_dict['start_z']
    fwhms = []

    n = len(task_dict['center_x'])
    if len(task_dict['center_y']) != n:
        raise ValueError(f"Unequal number of FWHM points provided: "
                         f"len(center_x) = {n}, "
                         f"len(center_y) = {len(task_dict['center_y'])}")
    if len(task_dict['radius']) != n:
        raise ValueError(f"Unequal number of FWHM points provided: "
                         f"len(center_x) = {n}, "
                         f"len(radius) = {len(task_dict['radius'])}")
    if len(task_dict['direction']) != n:
        raise ValueError(f"Unequal number of FWHM points provided: "
                         f"len(center_x) = {n}, "
                         f"len(direction) = {len(task_dict['direction'])}")

    while z < task_dict['end_z']:

        for i in range(n):
            center_x = task_dict['center_x'][i]
            center_y = task_dict['center_y'][i]
            radius = task_dict['radius'][i]
            direction = task_dict['direction'][i]

            min_idx = img.TransformPhysicalPointToIndex(
                (center_x - radius, center_y - radius, z))
            max_idx = img.TransformPhysicalPointToIndex(
                (center_x + radius, center_y + radius, z))
            z_idx = min_idx[2]

            peak_idx = min_idx
            peak_val = img[peak_idx]
            for x in range(min_idx[0], max_idx[0] + 1):
                for y in range(min_idx[1], max_idx[1] + 1):
                    if img[x, y, z_idx] > peak_val:
                        peak_idx = (x, y, z_idx)
                        peak_val = img[peak_idx]

            if direction == 'x':
                profile = img_data[z_idx, peak_idx[1], min_idx[0]:max_idx[0]]
                fwhm = nmiq.nema_fwhm_from_line_profile(profile)
                fwhms.append(float(img.GetSpacing()[0]) * fwhm)
            if direction == 'y':
                profile = img_data[z_idx, min_idx[1]:max_idx[1], peak_idx[0]]
                fwhm = nmiq.nema_fwhm_from_line_profile(profile)
                fwhms.append(float(img.GetSpacing()[1]) * fwhm)

        z += task_dict['delta_z']

    fwhm = np.mean(fwhms)
    se = np.std(fwhms, ddof=1)/np.sqrt(len(fwhms))

    res_file = os.path.join(task_dict['output_path'], 'lsf_res.txt')
    with open(res_file, 'w') as f:
        f.write(f"FWHM:\t{float(fwhm)}\n")
        f.write(f"S.E.:\t{float(se)}\n")
