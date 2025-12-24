import SimpleITK as sitk

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

    # Place a single sphere one radius inside cylinder at the cylinder centre
    sphere_center_point = (cylinder_center_x, cylinder_center_y, cylinder_start_z + roi_radius)
    for ix in range(img.GetSize()[0]):
        for iy in range(img.GetSize()[1]):
            for iz in range(img.GetSize()[2]):
                voxel_center_point = img.TransformIndexToPhysicalPoint((ix, iy, iz))
                d2 = ((voxel_center_point[0] - sphere_center_point[0])**2 +
                      (voxel_center_point[1] - sphere_center_point[1])**2 +
                      (voxel_center_point[2] - sphere_center_point[2])**2)
                if d2 <= roi_radius**2:
                    img.SetPixel(ix, iy, iz, 1)


    return img

