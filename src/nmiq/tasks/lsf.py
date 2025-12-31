from typing import Any

def lsf(task_dict: dict[str, Any]):

    z = task_dict['start_z']
    fwhms = []
    while z < task_dict['end_z']:

        n = len(task_dict['center_x'])




        z += task_dict['delta_z']
