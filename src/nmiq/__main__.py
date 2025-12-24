import argparse
import nmiq
import sys
import importlib.metadata
import time

from nmiq.tasks import bkgvar3d


def main(sys_args: list[str]):

    # Get version number from pyproject.toml
    __version__ = importlib.metadata.version("nmiq")
    start_time = time.time_ns()

    print("Starting NMIQ", __version__)
    print()

    parser = argparse.ArgumentParser()

    parser.add_argument('task',
                        choices=['summary', 'bkgvar3d'],
                        help="The task to run")

    parser.add_argument('-i',
                        help='Path to image files')
    parser.add_argument('-o',
                        help='Output path')
    parser.add_argument('--start_z',
                        help='Start z-coordinate [usage: bkgvar3d]')
    parser.add_argument('--end_z',
                        help='End z-coordinate [usage: bkgvar3d]')
    parser.add_argument('--center_x',
                        help='Center x-coordinate [usage: bkgvar3d]')
    parser.add_argument('--center_y',
                        help='Start y-coordinate [usage: bkgvar3d]')
    parser.add_argument('--cyl_radius',
                        help='Cylinder radius [usage: bkgvar3d]')
    parser.add_argument('--roi_radius',
                        help='ROI radius [usage: bkgvar3d]')

    args = parser.parse_args(sys_args)

    task_dict = {}

    # Load images
    print("Loading images...")
    img = nmiq.load_images(args.i)
    task_dict['image'] = img
    print(f"... done!")
    print()

    if args.task == 'summary':
        nmiq.tasks.summary(task_dict)
        print()
    if args.task == 'bkgvar3d':
        task_dict['cylinder_start_z'] = float(args.start_z)
        task_dict['cylinder_end_z'] = float(args.end_z)
        task_dict['cylinder_center_x'] = float(args.center_x)
        task_dict['cylinder_center_y'] = float(args.center_y)
        task_dict['cylinder_radius'] = float(args.cyl_radius)
        task_dict['roi_radius'] = float(args.roi_radius)
        task_dict['output_path'] = args.o
        nmiq.tasks.bkgvar3d(task_dict)
        print()

    # Report successful end of program
    run_time = (time.time_ns() - start_time) * 1e-9
    print(f'NMIQ finished successfully in {run_time:.1f} seconds.')
    print()


if __name__ == "__main__":
    main(sys.argv[1:])
