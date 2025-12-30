import numpy as np
import numpy.typing as npt

def nema_fwhm_from_line_profile(
        y: npt.NDArray[np.float64]) -> float:

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
    b = ((x1 * x1) * (y2 - y3) + (x3 * x3) * (y1 - y2) + (x2 * x2) * (y3 - y1)) / d
    c = ((x2 * x2) * (x3 * y1 - x1 * y3) + x2 * (x1 * x1 * y3 - x3 * x3 * y1) + x1 * x3 * (x3 - x1) * y2) / d

    # Calculate half max value
    yhm = (4 * a * c - b * b) / (8 * a)

    # Search for half max values
    i = 0
    while y[i+1] < yhm:
        i += 1
    # At this point: y[i] < yhm < y[i+1]
    # Find left value by interpolation:
    xl = (yhm - y[i+1] + (y[i+1] - y[i]) * (i + 1)) / (y[i+1] - y[i])

    i = i + 1
    while y[i+1] > yhm:
        i += 1
    # At this point: y[i] > yhm > y[i+1]
    # Find right value by interpolation:
    xr = (yhm - y[i + 1] + (y[i + 1] - y[i]) * (i + 1)) / (y[i + 1] - y[i])

    return xr - xl


