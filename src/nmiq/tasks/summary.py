from typing import Any


def summary(task_dict: dict[str, Any]):
    """
    Write a summary of an image to standard out.
    Takes a dictionary object as input. The only object required is
        image   --  The image to be summarized.
    """
    print("Image summary:")
    image = task_dict["image"]
    print(f"  Dimension: {image.GetDimension()}")
    print(f"  Size: {image.GetSize()}")
    print(f"  Spacing: {image.GetSpacing()}")
    print(f"  Origin: {image.GetOrigin()}")
