import SimpleITK as sitk
import numpy as np
import numpy.typing as npt
from collections.abc import Callable
from typing import Any

from nmiq import tasks

def load_images(image_path: str) -> sitk.Image: ...

def resample_image(image: sitk.Image,
                   new_spacing: tuple[float, ...]) -> sitk.Image: ...

def jackknife(func: Callable[[npt.NDArray[np.float64]], float],
              data: npt.NDArray[np.float64]) -> tuple[float, float]: ...

def spheres_in_cylinder_3d(
        image_size: tuple[int, int, int],
        image_spacing: tuple[int, int, int],
        image_origin: tuple[int, int, int],
        cylinder_start_z: float,
        cylinder_end_z: float,
        cylinder_center_x: float,
        cylinder_center_y: float,
        cylinder_radius: float,
        roi_radius: float) -> sitk.Image: ...

def nema_fwhm_from_line_profile(
        line_profile: npt.NDArray[np.float64]) \
        -> tuple[float, dict[str, Any]]: ...

def gaussfit_fwhm_from_line_profile(
        line_profile: npt.NDArray[np.float64]) -> list[float]: ...
