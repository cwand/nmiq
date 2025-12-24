import SimpleITK as sitk
import numpy as np


def _check_bounds(image: sitk.Image, physical_point: tuple[float, float, float]):

    index = image.TransformPhysicalPointToIndex(physical_point)

    # Get the image size
    size = image.GetSize()

    # Check if the continuous index is within the image bounds
    for i in range(len(index)):
        if index[i] < 0 or index[i] >= size[i]:
            return False
    return True

def spheres_in_cylinder_3d(
        image_size: tuple[int, int, int],
        image_spacing: tuple[int, int, int],
        image_origin: tuple[int, int, int],
        cylinder_start_z: float,
        cylinder_end_z: float,
        cylinder_center_x: float,
        cylinder_center_y: float,
        cylinder_radius: float,
        roi_radius: float) -> sitk.Image:
    img = sitk.Image(image_size, sitk.sitkUInt8)
    img.SetOrigin(image_origin)
    img.SetSpacing(image_spacing)

    # Sanity checks:

    # Check ROI radius fits inside cylinder length at least once
    if roi_radius > 0.5 * (cylinder_end_z - cylinder_start_z):
        raise ValueError(f"ROI radius does not fit into cylinder length: "
                         f"{roi_radius} > {(cylinder_end_z - cylinder_start_z)}"
                         f".")

    # Check ROI radius fits inside cylinder radius at least once
    if roi_radius > cylinder_radius:
        raise ValueError(f"ROI radius does not fit into cylinder radius: "
                         f"{roi_radius} > {cylinder_radius}.")

    # Check cylinder fits inside image space
    cyl_min_x = cylinder_center_x - cylinder_radius
    cyl_max_x = cylinder_center_x + cylinder_radius
    cyl_min_y = cylinder_center_y - cylinder_radius
    cyl_max_y = cylinder_center_y + cylinder_radius
    check_points = [
        (cyl_min_x, cyl_min_y, cylinder_start_z),
        (cyl_max_x, cyl_max_y, cylinder_end_z),
    ]
    for point in check_points:
        if not _check_bounds(img, point):
            raise ValueError(f"Cylinder exceeds image space: ({point[0]}, {point[1]}, {point[2]}) outside image.")

    # Sanity checks OK - start masking

    roi_center_z = cylinder_start_z + roi_radius
    z_idx = 0
    while roi_center_z + roi_radius < cylinder_end_z:
        if roi_radius > cylinder_radius / 2.0:
            # Only room for one sphere. Place it in the center of the cylinder
            placement_radius = 0.0
            n = 1
        else:
            # Spheres will be by the perimeter of the cylinder (kissing the edge)
            placement_radius = cylinder_radius - roi_radius
            # Calculate number of spheres:
            n = np.floor( np.pi / np.arcsin(roi_radius / (cylinder_radius - roi_radius)) )
        for s in range(int(n)):
            # Determine center point of ROI.
            roi_center_x = cylinder_center_x - placement_radius * np.sin(2 * s * np.pi / n)
            roi_center_y = cylinder_center_y - placement_radius * np.cos(2 * s * np.pi / n)
            # Find a bounding box around center voxel, that will contain all relevant voxels
            lower_index = img.TransformPhysicalPointToIndex(
                (roi_center_x - roi_radius,
                 roi_center_y - roi_radius,
                 roi_center_z - roi_radius))
            upper_index = img.TransformPhysicalPointToIndex(
                (roi_center_x + roi_radius,
                 roi_center_y + roi_radius,
                 roi_center_z + roi_radius)
            )
            # Iterate through bounding box
            for ix in range(lower_index[0], upper_index[0] + 1):
                for iy in range(lower_index[1], upper_index[1] + 1):
                    for iz in range(lower_index[2], upper_index[2] + 1):
                        voxel_center_point = img.TransformIndexToPhysicalPoint((ix, iy, iz))
                        d2 = ((voxel_center_point[0] - roi_center_x) ** 2 +
                              (voxel_center_point[1] - roi_center_y) ** 2 +
                              (voxel_center_point[2] - roi_center_z) ** 2)
                        if d2 <= roi_radius ** 2:
                            img.SetPixel(ix, iy, iz, int(n) * z_idx + s + 1)

        roi_center_z = roi_center_z + 2 * roi_radius + img.GetSpacing()[2]
        z_idx = z_idx + 1



    return img

