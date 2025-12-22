import os.path

import SimpleITK as sitk

def load_images(image_path: str) -> sitk.Image:

    if os.path.isfile(image_path):
        return sitk.ReadImage(image_path)

    series_reader = sitk.ImageSeriesReader()
    dcm_names = series_reader.GetGDCMSeriesFileNames(image_path)
    series_reader.SetFileNames(dcm_names)
    return series_reader.Execute()
