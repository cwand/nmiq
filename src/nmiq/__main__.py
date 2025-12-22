# import argparse
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

    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", metavar="IMG_PATH",
                        help="Path to dynamic image data",
                        required=True)
    parser.add_argument("-o", metavar="OUT_PATH",
                        help="Output path",
                        required=True)
    parser.add_argument("--roi", nargs=5, action="append",
                        metavar=("PATH", "VOX_VALUE", "LABEL", "OPERATION",
                                 "RESAMPLE"),
                        help="Define a ROI to extract. PATH is the path to "
                             "the ROI-file. VOX_VALUE is the value of the ROI "
                             "voxels in the file. LABEL is the name of the "
                             "ROI in the output file. RESAMPLE states whether "
                             "to resample either the ROI or the image data "
                             "before extraction (possible values are 'img', "
                             "'roi' or 'none'.")
    parser.add_argument("--scale", action='append', nargs=3,
                        metavar=("label_in", "label_out", "factor"),
                        help="Apply a scale factor to label_in and save it "
                             "as label_out")
    parser.add_argument("--pvc_vdil", action="append", nargs=4,
                        metavar=("ROI_LABEL", "DIL_LABEL", "BKG_LABEL",
                                 "LABEL_OUT"),
                        help="VDIL partial volume correction. Corrects the ROI"
                             "activity by adding the background corrected"
                             "activity in a dilated ROI.")
    parser.add_argument("--pvc_bard", action='append', nargs=5,
                        metavar=("ROI_LABEL", "BKG_LABEL",
                                 "ROI_DIAMETER", "TABLE_FILE", "LABEL_OUT"),
                        help="BARD partial volume correction. Corrects the "
                             "ROI activity based on the diameter of the ROI "
                             "and the background activity. Correction is "
                             "interpolated from a file of measured "
                             "PVC-factors.")
    parser.add_argument("--hideprogress", action='store_false',
                        help="Hide progress bar")
    args = parser.parse_args(sys_args)
    '''

    print(nmiq.add_things(3, 4))
    print()

    # Report successful end of program
    run_time = (time.time_ns() - start_time) * 1e-9
    print(f'NMIQ finished successfully in {run_time:.1f} seconds.')
    print()


if __name__ == "__main__":
    main(sys.argv[1:])
