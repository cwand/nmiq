import argparse
import nmiq
import sys
import importlib.metadata
import time


def main(sys_args: list[str]):

    # Get version number from pyproject.toml
    __version__ = importlib.metadata.version("nmiq")
    start_time = time.time_ns()

    print("Starting NMIQ", __version__)
    print()

    parser = argparse.ArgumentParser()

    parser.add_argument('task',
                        choices=['summary'],
                        help="The task to run")

    parser.add_argument('-i',
                        help='Path to image files')

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

    # Report successful end of program
    run_time = (time.time_ns() - start_time) * 1e-9
    print(f'NMIQ finished successfully in {run_time:.1f} seconds.')
    print()


if __name__ == "__main__":
    main(sys.argv[1:])
