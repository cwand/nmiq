import numpy as np
import numpy.typing as npt
import scipy.optimize as so
from typing import Any



def nema_fwhm_from_line_profile(
        y: npt.NDArray[np.float64]) \
    -> tuple[float, dict[str, Any]]:

    img_dict = {}

    # Find maximum point and neighbours
    x2 = np.argmax(y)
    x1 = x2 - 1
    x3 = x2 + 1

    y1 = y[x1]
    y2 = y[x2]
    y3 = y[x3]

    # Solve third degree polynomial

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

    # Search for half max values
    i = 0
    while y[i+1] < yhm:
        i += 1
    # At this point: y[i] < yhm < y[i+1]
    # Find left value by interpolation:
    xl = i + (yhm - y[i])/(y[i+1] - y[i])
    img_dict['left'] = i

    i = i + 1
    while y[i+1] > yhm:
        i += 1
    # At this point: y[i] > yhm > y[i+1]
    # Find right value by interpolation:
    xr = i + (yhm - y[i])/(y[i+1] - y[i])
    img_dict['right'] = i

    return float(xr - xl), img_dict


def _gauss(x: npt.NDArray[np.float64],
           a: float, b: float, w: float) -> npt.NDArray[np.float64]:
    return a * np.exp(-4 * np.log(2.0) * (x - b)**2 / (w ** 2))

def gaussfit_fwhm_from_line_profile(
        line_profile: npt.NDArray[np.float64],
        p0: list[float]) \
        -> list[float]:
    x = np.arange(len(line_profile))
    p = so.curve_fit(_gauss, x, line_profile, p0)
    return p[0]

