import SimpleITK as sitk

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
    if cylinder_center_x - cylinder_radius < image_origin[0] - 0.5 * image_spacing[0]:
        raise ValueError(f"Cylinder exceeds image space "
                         f"(x = {cylinder_center_x - cylinder_radius} < "
                         f"{image_origin[0] - 0.5 * image_spacing[0]}.")


    return img

