import SimpleITK as sitk
import numpy as np


def _check_bounds(image: sitk.Image,
                  physical_point: tuple[float, float, float]) -> bool:
    """
    Check whether a physical point is inside the image boundary (inside the
    Brillouin zone of a voxel).
    """

    # Transform physical point to index
    index = image.TransformPhysicalPointToIndex(physical_point)

    # Get the image size
    size = image.GetSize()

    # Check if the indices are within the image bounds
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
    """
    Given a cylinder, defined by the (x, y) coordinates of the cylinder axis
    (which points in the z-direction), the start and end positions of the
    cylinder i the z-dimension and the cylinder radius, this function places
    a set of spheres of a given radius inside the cylinder.
    The spheres will be defined in a voxelised grid with a given size and
    spacing. Therefore the quality of the spheres depend on the resolution
    given. In broad terms, the algorithm works as follows:
    The cylinder is sliced into pieces along the z-axis with a length equal
    to the diameter of the spheres (+ a small margin to make sure spheres do
    not overlap). Each piece of cylinder is cut into concentric shells with
    thickness equal to the sphere diameter (again + a small safety margin).
    Spheres are then distributed in each of these concentric shells in each
    of the pieces. Each sphere is defined by its central position, and a given
    voxel is deemed to belong to the sphere if its centre is at most one radius
    away from the centre point.
    All spheres will be given a separate integer label, which will be written
    to the output SimpleITK image object.
    Parameters:
        image_size          --  The voxel grid dimension
        image_spacing       --  The physical spacing between voxels
        image_origin        --  The physical position of the (0,0,0)-voxel
        cylinder_start_z    --  The start position of the cylinder
        cylinder_end_z      --  The end position of the cylinder
        cylinder_center_x   --  The x-coordinate of the cylinder centre
        cylinder_center_y   --  The y-coordinate of the cylinder centre
        cylinder_radius     --  The radius of the cylinder
        roi_radius          --  The radius of the spheres
    """

    # Create the output image
    img = sitk.Image(image_size, sitk.sitkUInt8)
    img.SetOrigin(image_origin)
    img.SetSpacing(image_spacing)

    # Sanity checks:

    # Check ROI radius fits inside cylinder length at least once
    if roi_radius > 0.5 * (cylinder_end_z - cylinder_start_z):
        raise ValueError(
            f"ROI radius does not fit into cylinder length: "
            f"{roi_radius} > {(cylinder_end_z - cylinder_start_z)}.")

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
            raise ValueError(
                f"Cylinder exceeds image space: "
                f"({point[0]}, {point[1]}, {point[2]}) outside image.")

    # Sanity checks OK - start masking

    # Initiate sphere labels
    label = 1

    # Get the central z-cooridnate of the first cylinder piece.
    roi_center_z = cylinder_start_z + roi_radius
    # Iterate through pieces along the z-direction
    while roi_center_z + roi_radius < cylinder_end_z:

        # First concentric shell starts from the outside
        conc_cylinder_radius = cylinder_radius
        # Iterate through concentric radii
        while conc_cylinder_radius >= roi_radius:

            # Calculate the radius of the spheres and the number that can fit
            if roi_radius > conc_cylinder_radius / 2.0:
                # Only room for one sphere
                placement_radius = 0.0
                n = 1
            else:
                # Spheres will be by the perimeter of the cylinder
                placement_radius = conc_cylinder_radius - roi_radius
                # Calculate number of spheres:
                n = np.floor(np.pi / np.arcsin(
                    roi_radius / (conc_cylinder_radius - roi_radius)
                ))

            # Iterate through each ROI in the shell
            for s in range(int(n)):
                # Determine center point of ROI. (First sphere at 12 o'clock)
                roi_center_x = (cylinder_center_x -
                                placement_radius * np.sin(2 * s * np.pi / n))
                roi_center_y = (cylinder_center_y -
                                placement_radius * np.cos(2 * s * np.pi / n))
                # Find a bounding box around centre voxel
                lower_index = img.TransformPhysicalPointToIndex(
                    (roi_center_x - roi_radius,
                     roi_center_y - roi_radius,
                     roi_center_z - roi_radius))
                upper_index = img.TransformPhysicalPointToIndex(
                    (roi_center_x + roi_radius,
                     roi_center_y + roi_radius,
                     roi_center_z + roi_radius)
                )
                # Iterate through bounding box to check if voxel belongs
                for ix in range(lower_index[0], upper_index[0] + 1):
                    for iy in range(lower_index[1], upper_index[1] + 1):
                        for iz in range(lower_index[2], upper_index[2] + 1):
                            voxel_center_point = (
                                img.TransformIndexToPhysicalPoint((ix, iy, iz))
                            )
                            d2 = ((voxel_center_point[0] - roi_center_x) ** 2 +
                                  (voxel_center_point[1] - roi_center_y) ** 2 +
                                  (voxel_center_point[2] - roi_center_z) ** 2)
                            if d2 <= roi_radius ** 2:
                                # Voxel centre inside radius. Add to label.
                                img.SetPixel(ix, iy, iz, label)

                label = label + 1

            # Decrease concentric shell radius by one sphere diamater and a
            # safety margin
            conc_cylinder_radius = (conc_cylinder_radius - 2 * roi_radius -
                                    max(img.GetSpacing()[0],
                                        img.GetSpacing()[1]))

        # Advance to next cylinder piece in the z-direction.
        roi_center_z = roi_center_z + 2 * roi_radius + img.GetSpacing()[2]

    return img


def cylinder_3d(
        image_size: tuple[int, int, int],
        image_spacing: tuple[int, int, int],
        image_origin: tuple[int, int, int],
        cylinder_start_z: float,
        cylinder_end_z: float,
        cylinder_center_x: float,
        cylinder_center_y: float,
        cylinder_radius: float) -> sitk.Image:

    mask = sitk.Image(image_size, sitk.sitkUInt16)
    mask.SetSpacing(image_spacing)
    mask.SetOrigin(image_origin)

    # Sanity checks:

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
        if not _check_bounds(mask, point):
            raise ValueError(
                f"Cylinder exceeds image space: "
                f"({point[0]}, {point[1]}, {point[2]}) outside image.")

    # Convert extreme points to indices
    min_search_point = (cylinder_center_x - cylinder_radius,
                        cylinder_center_y - cylinder_radius,
                        cylinder_start_z)
    min_index = mask.TransformPhysicalPointToIndex(min_search_point)
    max_search_point = (cylinder_center_x + cylinder_radius,
                        cylinder_center_y + cylinder_radius,
                        cylinder_end_z)
    max_index = mask.TransformPhysicalPointToIndex(max_search_point)

    # Iterate through z-slices from start to end
    iz = min_index[2]
    while iz <= max_index[2]:

        # Check all voxels in search box for distance to center and include
        for ix in range(min_index[0], max_index[0] + 1):
            for iy in range(min_index[1], max_index[1] + 1):
                vox_point = mask.TransformIndexToPhysicalPoint((ix, iy, iz))
                if ((cylinder_center_x - vox_point[0]) ** 2 + (cylinder_center_y - vox_point[1]) ** 2
                        <= cylinder_radius ** 2):
                    mask[ix, iy, iz] = 1

        # Move on to next z
        iz += 1

    return mask


def hottest_cylinder_3d(
        image: sitk.Image,
        cylinder_start_z: float,
        cylinder_end_z: float,
        cylinder_center_x: float,
        cylinder_center_y: float,
        cylinder_radius: float,
        mask_size: tuple[int, int, int] = None,
        mask_spacing: tuple[int, int, int] = None,
        mask_origin: tuple[int, int, int] = None) -> sitk.Image:

    if mask_size is None:
        mask = sitk.Image(image.GetSize(), sitk.sitkUInt16)
    else:
        mask = sitk.Image(mask_size, sitk.sitkUInt16)

    if mask_spacing is None:
        mask.SetSpacing(image.GetSpacing())
    else:
        mask.SetSpacing(mask_spacing)

    if image_origin is None:
        mask.SetOrigin(image.GetOrigin())
    else:
        mask.SetOrigin(image_origin)

    # Sanity checks:

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
        if not _check_bounds(mask, point):
            raise ValueError(
                f"Cylinder exceeds image space: "
                f"({point[0]}, {point[1]}, {point[2]}) outside image.")

    # Sanity checks OK, start masking

    # Convert centre point to index
    start_point = (cylinder_center_x, cylinder_center_y, cylinder_start_z)
    start_index = mask.TransformPhysicalPointToIndex(start_point)
    end_point = (cylinder_center_x, cylinder_center_y, cylinder_end_z)
    end_index = mask.TransformPhysicalPointToIndex(end_point)

    # Convert radius to index in x- and y-direction
    x_idx_radius = int(np.ceil(cylinder_radius / image.GetSpacing()[0]))
    y_idx_radius = int(np.ceil(cylinder_radius / image.GetSpacing()[1]))

    # Prepare stats filter for testing mask
    label_stats_filter = sitk.LabelStatisticsImageFilter()

    # Iterate through z-slices from start to end
    iz = start_index[2]
    while iz <= end_index[2]:

        search_dict = {}
        max_val = -1.0
        max_index = (0, 0, 0)

        # Start search at centre point
        index_list = [(start_index[0], start_index[1], iz)]
        while index_list:
            index = index_list.pop()
            print(f'Testing index {index}:')
            if index not in search_dict:

                point = image.TransformIndexToPhysicalPoint(index)

                for ix in range(index[0] - x_idx_radius,
                                index[0] + x_idx_radius + 1):
                    for iy in range(index[1] - y_idx_radius,
                                    index[1] + y_idx_radius + 1):
                        # Calculate distance between voxel and centre
                        vox_point = image.TransformIndexToPhysicalPoint(
                            (ix, iy, iz))
                        r2 = ((point[0] - vox_point[0]) ** 2 +
                              (point[1] - vox_point[1]) ** 2)
                        # Mask if within radius
                        if r2 <= cylinder_radius ** 2:
                            mask[ix, iy, iz] = 2
                label_stats_filter.Execute(image, mask)
                cur_val = label_stats_filter.GetSum(2)
                # Reset mask
                for ix in range(index[0] - x_idx_radius,
                                index[0] + x_idx_radius + 1):
                    for iy in range(index[1] - y_idx_radius,
                                    index[1] + y_idx_radius + 1):
                        mask[ix, iy, iz] = 0

                search_dict[index] = cur_val
                if cur_val > max_val:
                    max_val = cur_val
                    max_index = index
                    index_list.append((index[0] - 1, index[1], index[2]))
                    index_list.append((index[0] + 1, index[1], index[2]))
                    index_list.append((index[0], index[1] - 1, index[2]))
                    index_list.append((index[0], index[1] + 1, index[2]))

        # Draw final mask
        point = image.TransformIndexToPhysicalPoint(max_index)
        for ix in range(max_index[0] - x_idx_radius,
                        max_index[0] + x_idx_radius + 1):
            for iy in range(max_index[1] - y_idx_radius,
                            max_index[1] + y_idx_radius + 1):
                # Calculate distance between voxel and centre
                vox_point = image.TransformIndexToPhysicalPoint(
                    (ix, iy, iz))
                r2 = ((point[0] - vox_point[0]) ** 2 +
                      (point[1] - vox_point[1]) ** 2)
                # Mask if within radius
                if r2 <= cylinder_radius ** 2:
                    mask[ix, iy, iz] = 1

        # Move on to next z
        iz += 1

    return mask
