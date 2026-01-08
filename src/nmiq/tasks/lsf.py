from typing import Any
import SimpleITK as sitk
import nmiq
import os
import numpy as np
import matplotlib.pyplot as plt


def lsf(task_dict: dict[str, Any]):
    """
    Line Spread Function (LSF) Full width half maximum (FWHM) calculation.
    This function computes the FWHM of an image slice of one or more
    line sources. The sources should be aligned with the z-axis.
    The input to the task is a dictionary object, where the following keys
    should be defined:
        image               --  The image to analyse (SimpleITK Image)
        start_z             --  The start position of the line sources
        end_z               --  The end position of the line sources
        delta_z             --  Distance between successive slices to analyse
        center_x            --  List of x-coordinates of the line sources
        center_y            --  List of y-coordinates of the line sources
        radius              --  The distances from the center positions the
                                line profiles should extend
        direction           --  The directions of the line profiles (x or y)
        output_path         --  The path where output should be stored
    Given this input the function does the following:
    The function will start at the start_z location. Here it will go through
    the list of line source positions (center_x, center_y). At each position
    it will find the maximum voxel in the box where
    x = [center_x - radius, center_x + radius] and
    y = [center_y - radius, center_y + radius]. When the maximum voxel is
    determined a line profile with the given direction (x or y) will be made
    to go through that maximum voxel. If e.g. the direction is x and the
    maximum voxel is at position (x_m, y_m), then the line profile will go from
    (center_x - radius, y_m) to (center_x + radius, y_m).
    From the line profile the FWHM is determined from to algorithms: the NEMA
    algorithm and by fitting a gaussian function to the line profile.
    For both estimates the procedure is repeated for all line source positions.
    The function then moves on to the next z-position (increasing the z-value
    by delta_z), until z_end has been reached. The final FWHM-values will be
    the average of all the estimates for each separate algorithm. The standard
    error on the mean is also computed and reported. Finally, an image file is
    generated where the fits to the line profiles can be inspected.
    """

    # Get image and numpy voxel array
    img = task_dict['image']
    img_data = sitk.GetArrayFromImage(img)

    # Storage for fwhms
    nema_fwhms = []
    gauss_fwhms = []

    # Get number of line sources, and check that all agree
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

    # Get number of z-slices
    zs = int(np.ceil((task_dict['end_z'] - task_dict['start_z'])
                     / task_dict['delta_z']))

    # Create matplotlib figure handles
    fig, axs = plt.subplots(zs, n, figsize=(n*4, zs*3))

    # Iterate through z-slices
    for iz in range(zs):

        # Calculate current z
        z = task_dict['start_z'] + iz * task_dict['delta_z']

        # Iterate through line sources
        for i in range(n):
            # Identify source position and direction
            center_x = task_dict['center_x'][i]
            center_y = task_dict['center_y'][i]
            radius = task_dict['radius'][i]
            direction = task_dict['direction'][i]

            # Find position of maximum voxel
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

            # Create line profile through maximum voxel
            if direction == 'x':
                profile = img_data[z_idx, peak_idx[1], min_idx[0]:max_idx[0]+1]
                x_data = np.arange(min_idx[0], max_idx[0] + 1)
                spacing = float(img.GetSpacing()[0])
            elif direction == 'y':
                profile = img_data[z_idx, min_idx[1]:max_idx[1]+1, peak_idx[0]]
                x_data = np.arange(min_idx[1], max_idx[1] + 1)
                spacing = float(img.GetSpacing()[1])
            else:
                raise ValueError(f"Unknown direction: {direction}")

            # Calculate FWHM (multiplied by spacing to get physical value)
            nema_fwhm = nmiq.nema_fwhm_from_line_profile(profile)
            nema_fwhms.append(spacing * nema_fwhm[0])
            gauss_fwhm = nmiq.gaussfit_fwhm_from_line_profile(profile)
            gauss_fwhms.append(spacing * gauss_fwhm[2])

            # Plot line profile and fits
            x_plot_gauss = np.linspace(np.min(x_data), np.max(x_data), 1000)
            axs[iz, i].plot(x_data, profile,
                            'k.', markersize=15, label='Profile')
            axs[iz, i].plot(x_plot_gauss,
                            gauss_fwhm[0] * np.exp(
                                -4 * np.log(2.0) *
                                (x_plot_gauss - x_data[0] - gauss_fwhm[1])**2 /
                                (gauss_fwhm[2] ** 2)),
                            '-', linewidth=2, color='darkorange',
                            label='Gauss fit')
            axs[iz, i].plot([x_data[0] + gauss_fwhm[1] - 0.5 * gauss_fwhm[2],
                             x_data[0] + gauss_fwhm[1] + 0.5 * gauss_fwhm[2]],
                            [0.5 * gauss_fwhm[0], 0.5 * gauss_fwhm[0]],
                            '--', color='darkorange', linewidth=2)
            x_plot_nema = np.linspace(
                nema_fwhm[1]['x1'], nema_fwhm[1]['x1'] + 2, 1000)
            axs[iz, i].plot(x_plot_nema + x_data[0],
                            nema_fwhm[1]['poly'](x_plot_nema),
                            '-', color='royalblue', linewidth=2,
                            label='Nema fit')
            axs[iz, i].plot(
                [nema_fwhm[1]['left'] + x_data[0],
                 nema_fwhm[1]['left'] + x_data[0] + 1],
                [profile[nema_fwhm[1]['left']],
                 profile[nema_fwhm[1]['left'] + 1]],
                '--', color='royalblue', linewidth=1)
            axs[iz, i].plot(
                [nema_fwhm[1]['right'] + x_data[0],
                 nema_fwhm[1]['right'] + x_data[0] + 1],
                [profile[nema_fwhm[1]['right']],
                 profile[nema_fwhm[1]['right'] + 1]],
                '--', color='royalblue', linewidth=1)
            axs[iz, i].plot(
                [nema_fwhm[1]['left_int'] + x_data[0],
                 nema_fwhm[1]['right_int'] + x_data[0]],
                [nema_fwhm[1]['hm'], nema_fwhm[1]['hm']],
                '--', color='royalblue', linewidth=2)
            axs[iz, i].set_title(f'x = {center_x}, '
                                 f'y = {center_y}, '
                                 f'z = {z}')
            axs[iz, i].grid()

    axs[0, 0].legend()
    fig.supxlabel('Voxel index')
    fig.supylabel('Voxel intensity')
    plt.tight_layout()
    plt.savefig(os.path.join(task_dict['output_path'], 'fwhm.png'))

    # Calculate mean and standard error on fwhm estimates
    nema_fwhm_mean = np.mean(nema_fwhms)
    nema_se = np.std(nema_fwhms, ddof=1)/np.sqrt(len(nema_fwhms))

    gauss_fwhm_mean = np.mean(gauss_fwhms)
    gauss_se = np.std(gauss_fwhms, ddof=1) / np.sqrt(len(gauss_fwhms))

    # Print results
    res_file = os.path.join(task_dict['output_path'], 'lsf_res.txt')
    with open(res_file, 'w') as f:
        f.write(f"NEMA:\t{float(nema_fwhm_mean)}\n")
        f.write(f"S.E.:\t{float(nema_se)}\n")
        f.write(f"Gauss:\t{float(gauss_fwhm_mean)}\n")
        f.write(f"S.E.:\t{float(gauss_se)}\n")
