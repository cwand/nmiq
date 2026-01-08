import os.path
from math import ceil
import SimpleITK as sitk
import numpy as np
import numpy.typing as npt
from collections.abc import Callable


def resample_image(image: sitk.Image,
                   new_spacing: tuple[float, ...]) -> sitk.Image:
    """
    Resample an image to a new spacing using nearest neighbour interpolation
    Parameters:
         image          --  The image to be resampled (SimpleITK.Image).
         new_spacing    --  The new spacing. Use zeros to indicate that the
                            original spacing should be kept.
    Returns:
        A SimpleITK.Image object with the image resampled to the new spacing.
    """

    # Calculate grid size for the resampled image
    original_size = image.GetSize()
    original_spacing = image.GetSpacing()
    new_size = [
        int(ceil(original_size[i] * original_spacing[i] / new_spacing[i]))
        for i in range(image.GetDimension())
    ]

    # Setup resampler and return image
    resampler = sitk.ResampleImageFilter()
    resampler.SetInterpolator(
        sitk.sitkNearestNeighbor)
    resampler.SetOutputSpacing(new_spacing)
    resampler.SetSize(new_size)
    resampler.SetOutputDirection(image.GetDirection())
    resampler.SetOutputOrigin(image.GetOrigin())
    return resampler.Execute(image)  # type: ignore


def load_images(image_path: str) -> sitk.Image:
    """
    Load image from a file. This wrapper around SimpleITK.ReadImage is made
    to ensure that image series in a directory as well as an image file can
    be loaded from the same function call.
    Parameters:
        image_path   --  The path to the image or series to be loaded.
    Returns:
        A SimpleITK.Image object with the image or image series.
    """

    # In case of a single image file: load the image directly.
    if os.path.isfile(image_path):
        return sitk.ReadImage(image_path)

    # If a directory is given, read as a series.
    series_reader = sitk.ImageSeriesReader()
    dcm_names = series_reader.GetGDCMSeriesFileNames(image_path)
    series_reader.SetFileNames(dcm_names)
    return series_reader.Execute()  # type: ignore


def jackknife(func: Callable[[npt.NDArray[np.float64]], float],
              data: npt.NDArray[np.float64]) -> tuple[float, float]:
    """
    Jackknife resampling to estimate the standard error of a distribution
    property.
    Parameters:
         func: the function describing the distribution property of interest.
         data: a sample of the distribution.
    Returns:
        A tuple with two floats: the first is the estimate of the mean (simply
        the function evaluated on the entire data sample), the second is the
        jackknife estimate of the standard error on the mean.
    """

    # Number of jackknife samples to generate
    n = len(data)

    # Placeholder for function evaluations on the jackknife samples
    jks = np.zeros_like(data)

    # Evaluate function on all jackknife samples
    for i in range(n):
        jks[i] = func(np.delete(data, i))

    # Evaluate jackknife mean and compute standard error
    jkm = np.mean(jks)
    se = np.sqrt(((n-1)/n)*np.sum(np.pow(jks-jkm, 2)))

    return func(data), se
