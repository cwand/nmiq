import numpy as np
import numpy.typing as npt
import scipy.optimize as so
from typing import Any


def nema_fwhm_from_line_profile(
        y: npt.NDArray[np.float64]) -> tuple[float, dict[str, Any]]:
    """
    Compute FWHM from a line profile according to the NEMA algorithm:
        1)  A second-degree polynomial is "fitted" to the maximum value along
            the profile along with its two neighbours.
        2)  The "peak value" yp is computed as the maximum of the polynomial.
        3)  The positions xl and xr, where the line profile goes through the
            value yp/2 are determined by linear interpolation along the line
            profile.
        4)  The FWHM equals xr - xl
    The function returns the computed FWHM along with a dict object that can
    be used to draw a depiction of the algorithm. The dict object contains the
    keys:
        poly        --  The 2nd deg. polynomial fitted to the three points as a
                        callable (assuming the line profile starts at x=0).
        x1          --  The index of the first of the three points included in
                        the polynomial fit.
        hm          --  The half-maximum value of the polynomial.
        left        --  The index of the point just before the line profile
                        goes above the half maximum value.
        left_int    --  The interpolated x-value (assuming the line profile
                        starts at x=0), where the line profile goes above the
                        half maximum value.
        right       --  The index of the point just before the line profile
                        goes below the half maximum value.
        right_int   --  The interpolated x-value (assuming the line profile
                        starts at x=0), where the line profile goes below the
                        half maximum value.

    Arguments:
        y   --  The line profile of the source
    Returns:
        A tuple with the following values:
            --  The computed FWHM.
            --  A tuple for visual documentation of the calculation
                (see above).
    """

    # The dictionary containing fitting info
    img_dict: dict[str, Any] = {}

    # Find maximum point and neighbours
    x2 = np.argmax(y)
    x1 = x2 - 1
    x3 = x2 + 1
    img_dict['x1'] = x1

    # Corresponding y-values.
    y1 = y[x1]
    y2 = y[x2]
    y3 = y[x3]

    # Solve second degree polynomial
    # (You improve it if you're so clever!)
    d = (x1 - x2) * (x1 - x3) * (x2 - x3)
    a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / d
    b = ((x1 * x1) * (y2 - y3) +
         (x3 * x3) * (y1 - y2) +
         (x2 * x2) * (y3 - y1)) / d
    c = ((x2 * x2) * (x3 * y1 - x1 * y3) +
         x2 * (x1 * x1 * y3 - x3 * x3 * y1) +
         x1 * x3 * (x3 - x1) * y2) / d
    img_dict['poly'] = lambda x: a * x**2 + b * x + c

    # Calculate half max value
    yhm = (4 * a * c - b * b) / (8 * a)
    img_dict['hm'] = yhm

    # Search for half max values
    i = 0
    while y[i+1] < yhm:
        i += 1
    # At this point: y[i] < yhm < y[i+1]
    # Find left value by interpolation:
    xl = i + (yhm - y[i])/(y[i+1] - y[i])
    img_dict['left'] = i
    img_dict['left_int'] = xl

    i = i + 1
    while y[i+1] > yhm:
        i += 1
    # At this point: y[i] > yhm > y[i+1]
    # Find right value by interpolation:
    xr = i + (yhm - y[i])/(y[i+1] - y[i])
    img_dict['right'] = i
    img_dict['right_int'] = xr

    return float(xr - xl), img_dict


def _gauss(x: npt.NDArray[np.float64],
           a: float, b: float, w: float) -> npt.NDArray[np.float64]:
    """
    A gaussian bell curve function parametrised by FWHM (w)
    """
    return np.array(a * np.exp(-4 * np.log(2.0) * (x - b)**2 / (w ** 2)))


def gaussfit_fwhm_from_line_profile(
        line_profile: npt.NDArray[np.float64]) \
        -> list[float]:
    """
    Compute FWHM of a line profile by fitting a gaussian. The gaussian is
    parametrised as
    y = a * exp(-4 * np.log(2.0) * (x - b)**2 / (w ** 2)).
    It is assumed that the line profile starts at x=0 and that the distance
    between the points is 1. The FWHM is w.
    Arguments:
        line_profile  --  The line profile of the source
    Returns:
        The optimal parameters of the gauss function: a, b, w
    """

    # Construct artificial x-axis
    x = np.arange(len(line_profile))

    # Guess starting values
    p0 = [np.max(line_profile), len(line_profile)/2, 1.0]

    # Fit and return optimal values
    p = so.curve_fit(_gauss, x, line_profile, p0)
    return list(p[0])
