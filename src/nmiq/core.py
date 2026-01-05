import os.path
from math import ceil
import SimpleITK as sitk
import numpy as np
import numpy.typing as npt
from collections.abc import Callable


def resample_image(image: sitk.Image,
                   new_spacing: tuple[float, ...]) -> sitk.Image:
    original_size = image.GetSize()
    original_spacing = image.GetSpacing()
    new_size = [
        int(ceil(original_size[i] * original_spacing[i] / new_spacing[i]))
        for i in range(image.GetDimension())
    ]

    resampler = sitk.ResampleImageFilter()
    resampler.SetInterpolator(
        sitk.sitkNearestNeighbor)
    resampler.SetOutputSpacing(new_spacing)
    resampler.SetSize(new_size)
    resampler.SetOutputDirection(image.GetDirection())
    resampler.SetOutputOrigin(image.GetOrigin())

    return resampler.Execute(image)  # type: ignore


def load_images(image_path: str) -> sitk.Image:

    if os.path.isfile(image_path):
        return sitk.ReadImage(image_path)

    series_reader = sitk.ImageSeriesReader()
    dcm_names = series_reader.GetGDCMSeriesFileNames(image_path)
    series_reader.SetFileNames(dcm_names)

    return series_reader.Execute()  # type: ignore


def jackknife(func: Callable[[npt.NDArray[np.float64]], float],
              data: npt.NDArray[np.float64]) -> tuple[float, float]:

    n = len(data)
    jks = np.zeros_like(data)
    for i in range(n):
        jks[i] = func(np.delete(data, i))
    jkm = np.mean(jks)
    se = np.sqrt(((n-1)/n)*np.sum(np.pow(jks-jkm, 2)))

    return func(data), se
