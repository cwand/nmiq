from typing import Any

def summary(task_dict: dict[str, Any]):
    print("Image summary:")
    image = task_dict["image"]
    print(f"  Dimension: {image.GetDimension()}")
    print(f"  Size: {image.GetSize()}")
    print(f"  Spacing: {image.GetSpacing()}")