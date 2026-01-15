import argparse
import nmiq
import sys
import importlib.metadata
import time
from typing import Any


def main(sys_args: list[str]):

    # Get version number from pyproject.toml
    __version__ = importlib.metadata.version("nmiq")
    start_time = time.time_ns()

    print("Starting NMIQ", __version__)
    print()

    parser = argparse.ArgumentParser()

    parser.add_argument('task',
                        choices=['summary', 'bkgvar3d', 'lsf',
                                 'contrast_cyl3d'],
                        help="The task to run")

    parser.add_argument('-i',
                        help='Path to image files')
    parser.add_argument('-o',
                        help='Output path')
    parser.add_argument('--resample',
                        help='Resample the input image with a given spacing '
                             'in each image dimension. '
                             'The new spacings should be given as a '
                             'comma-separated list, like "1.2,1.2,0", '
                             'where a 0 means the original spacing should '
                             'be kept for that dimension.')
    parser.add_argument('--start_z',
                        help='Start z-coordinate '
                             '[usage: bkgvar3d, lsf, contrast_cyl3d]')
    parser.add_argument('--end_z',
                        help='End z-coordinate '
                             '[usage: bkgvar3d, lsf, contrast_cyl3d]')
    parser.add_argument('--delta_z',
                        help='Spacing between slices in z-direction '
                             '[usage: lsf]')
    parser.add_argument('--center_x', nargs='*',
                        help='Center x-coordinate [usage: bkgvar3d, lsf]')
    parser.add_argument('--center_y', nargs='*',
                        help='Start y-coordinate [usage: bkgvar3d, lsf]')
    parser.add_argument('--cyl_center_x',
                        help='Cylinder center x-coordinate '
                             '[usage: contrast_cyl3d]')
    parser.add_argument('--cyl_center_y',
                        help='Cylinder center y-coordinate '
                             '[usage: contrast_cyl3d]')
    parser.add_argument('--bkg_center_x',
                        help='Background center x-coordinate '
                             '[usage: contrast_cyl3d]')
    parser.add_argument('--bkg_center_y',
                        help='Background center y-coordinate '
                             '[usage: contrast_cyl3d]')
    parser.add_argument('--direction', nargs='*', choices=['x', 'y'],
                        help='Line profile direction [usage: lsf]')
    parser.add_argument('--radius', nargs='*',
                        help='Radius '
                             '[usage: lsf, contrast_cyl3d]')
    parser.add_argument('--cyl_radius',
                        help='Cylinder radius '
                             '[usage: bkgvar3d, contrast_cyl3d]')
    parser.add_argument('--roi_radius',
                        help='ROI radius [usage: bkgvar3d]')

    args = parser.parse_args(sys_args)

    task_dict: dict[str, Any] = {}

    # Load images
    print("Loading images...")
    img = nmiq.load_images(args.i)
    task_dict['image'] = img
    print("... done!")
    print()

    # Resample input image if needed
    if args.resample:

        old_spacing = img.GetSpacing()
        new_spacing: list[float] = []
        spacings = args.resample.split(',')
        if len(old_spacing) != len(spacings):
            raise ValueError(f"Dimension mismatch when resampling. "
                             f"Original image spacing: {old_spacing}. "
                             f"Spacing requested: {args.resample}.")
        for i in range(len(old_spacing)):
            if spacings[i] == '0':
                new_spacing.append(old_spacing[i])
            else:
                new_spacing.append(float(spacings[i]))
        img2 = nmiq.resample_image(img, tuple(new_spacing))
        task_dict['image'] = img2

    if args.task == 'summary':
        nmiq.tasks.summary(task_dict)
        print()
    if args.task == 'bkgvar3d':
        task_dict['start_z'] = float(args.start_z)
        task_dict['end_z'] = float(args.end_z)
        task_dict['cylinder_center_x'] = float(args.center_x[0])
        task_dict['cylinder_center_y'] = float(args.center_y[0])
        task_dict['cylinder_radius'] = float(args.cyl_radius)
        task_dict['roi_radius'] = float(args.roi_radius)
        task_dict['output_path'] = args.o
        nmiq.tasks.bkgvar3d(task_dict)
        print()
    if args.task == 'lsf':
        task_dict['start_z'] = float(args.start_z)
        task_dict['end_z'] = float(args.end_z)
        task_dict['delta_z'] = float(args.delta_z)
        task_dict['center_x'] = [float(x) for x in args.center_x]
        task_dict['center_y'] = [float(x) for x in args.center_y]
        task_dict['direction'] = args.direction
        task_dict['radius'] = [float(x) for x in args.radius]
        task_dict['output_path'] = args.o
        nmiq.tasks.lsf(task_dict)
        print()
    if args.task == 'contrast_cyl3d':
        task_dict['start_z'] = float(args.start_z)
        task_dict['end_z'] = float(args.end_z)
        task_dict['cylinder_center_x'] = float(args.cyl_center_x)
        task_dict['cylinder_center_y'] = float(args.cyl_center_y)
        task_dict['background_center_x'] = float(args.bkg_center_x)
        task_dict['background_center_y'] = float(args.bkg_center_y)
        task_dict['cylinder_radius'] = float(args.cyl_radius)
        task_dict['radius'] = float(args.radius[0])
        task_dict['output_path'] = args.o
        nmiq.tasks.contrast_cyl3d(task_dict)
        print()

    # Report successful end of program
    run_time = (time.time_ns() - start_time) * 1e-9
    print(f'NMIQ finished successfully in {run_time:.1f} seconds.')
    print()


if __name__ == "__main__":
    main(sys.argv[1:])
