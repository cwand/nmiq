from typing import Any
import SimpleITK as sitk
import numpy as np
import numpy.typing as npt
import nmiq
import os


def _bkg_var_func(x: npt.NDArray[np.float64]) -> float:
    """
    Function that calculates background variability from a set of measured
    ROI values.
    The background varaibility is defined as the sample standard deviation
    divided by the mean of the samples.
    """
    return float(np.std(x, ddof=1) / np.mean(x))


def bkgvar3d(task_dict: dict[str, Any]):
    """
    Background variability task.
    Calculates background variability in a cylindrical region of an image.
    The function takes a dictionary object as input, and the following keys
    must be present:
        image               --  The image to analyse (SimpleITK Image)
        start_z             --  The physical z-position of the start of the
                                cylinder
        end_z               --  The physical z-position of the end of the
                                cylinder
        cylinder_center_x   --  The x-position of the cylinder center
        cylinder_center_y   --  The y-position of the cylinder center
        cylinder_radius     --  The radius of the cylinder
        roi_radius          --  The radius of the ROIs to use
        output_path         --  The path where output should be stored

    Given these inputs, a number of spherical ROIs with the given radius will
    be placed inside the cylinder, and the background variability measured
    from the mean values inside each ROI. The standard error of the background
    variability will be estimated by jackknife resampling.
    Two files will be created as output: A text file containing the numerical
    results of the computation and an image file containing the spherical ROIs.
    """

    print("Starting BKGVAR3D task.")
    print()

    # Get image
    img = task_dict['image']

    # Compute masks given cylinder and ROI geometry
    print("Placing spheres in cylinder.")
    mask = nmiq.spheres_in_cylinder_3d(
        image_size=img.GetSize(),
        image_spacing=img.GetSpacing(),
        image_origin=img.GetOrigin(),
        cylinder_start_z=task_dict['start_z'],
        cylinder_end_z=task_dict['end_z'],
        cylinder_center_x=task_dict['cylinder_center_x'],
        cylinder_center_y=task_dict['cylinder_center_y'],
        cylinder_radius=task_dict['cylinder_radius'],
        roi_radius=task_dict['roi_radius']
    )

    # Find the number of spheres placed in the cylinder
    max_label = np.max(sitk.GetArrayFromImage(mask))
    print(f'{max_label} spheres placed in cylinder.')

    # Compute the mean voxel intensity in each spehere
    label_stats_filter = sitk.LabelStatisticsImageFilter()
    label_stats_filter.Execute(img, mask)
    means = np.zeros(max_label)
    for label in range(max_label):
        m = label_stats_filter.GetMean(label + 1)
        print(f'Sphere {label} mean = {m:.2f}')
        means[label] = m

    # Compute background variability and standard error
    bkg_var, se = nmiq.jackknife(_bkg_var_func, means)
    print(f"Result: N = {bkg_var:.4f} +/- {se:.4f}")

    # Write output
    print("Writing output.")
    mask_write_path = os.path.join(task_dict['output_path'],
                                   'bkgvar3d_mask.nii.gz')
    sitk.WriteImage(mask, mask_write_path)

    res_file = os.path.join(task_dict['output_path'], 'bkgvar3d_res.txt')
    with open(res_file, 'w') as f:
        f.write(f"Result:\t{float(bkg_var)}\n")
        f.write(f"S.E.:\t{float(se)}\n")
        f.write(f"K:\t{int(max_label)}\n")
    print("BKGVAR3D task completed.")
    print()
