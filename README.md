# nmiq
Python code for performing image quality analysis in nuclear medicine images

## Getting nmiq
Clone the repository to your computer using git:
```
> git clone https://github.com/cwand/nmiq
```

Enter the directory.
Make sure you are on the main branch:
```
> git checkout main
```

Create a new virtual python environment:
```
> python -m venv my_venv
```

Activate the virtual environment. Commands vary according to OS and shell (see [the venv documentation](https://docs.python.org/3/library/venv.html)), but in a Windows PowerShell:
```
> my_venv\Scripts\Activate.ps1
```

Install nmiq and required dependencies
```
> pip install .
```

If everything has gone right, you should be able to run nmiq
```
> python -m nmiq
Starting NMIQ

...
python.exe -m nmiq: error: the following arguments are required: task
```

## Using nmiq

First and foremost: a help message is displayed when running mniq with the ```-h``` flag:
```
> python -m nmiq -h
```

To use nmiq you need an image file to analyse 
(any format recognised by SimpleITK will do).
Let us say we want to measure Line Spread Function FWHM on an
image located in ```img/test_img.dcm```:

```
> python -m nmiq lsf -i img/test_img.dcm -o res/lsf --center_x 50 --center_y 70 --start_z 1000 --end_z 1010 --delta_z 7 --radius 10 --direction x
```
The meaning of the input arguments relevant for the LSF-task will be explained below.
The ```-i img/test_img.dcm``` tells nmiq where to look for the input image file,
and ```-o res/lsf``` tells nmiq that any output should be written to the directory
```res/lsf```, where all result files will be put.

### Resampling
In case resampling is required before starting the computation task, this can
be acieved by the ```--resample``` flag:
```
> python -m nmiq bkgvar3d -i img/low_res_img.dcm -o . --resample 0.5,0.5,0 ...
```
The new voxel spacing is set as a comma-separated list. To keep the native spacing
in a certain dimension use a 0. 
All resampling is done with nearest neighbour interpolation.

### Tasks

Below is a quick guide to each of the tasks implemented in nmiq.

#### bkgvar3d

This task is designed to measure uniformity in homegeneous cylindrical phantom.
Given a cylindrical region of the image and a, this task creates a series of $K$ 
spherical ROIs (with user determined radius) distributed around the cylinder and measures
the average voxel intensity in each ROI. The background variability $B$ is then calculated
as the ratio of the sample standard deviation of the $K$ ROI signals and their mean:
$$
B = \frac{\sqrt{\frac{1}{K-1} \sum_{i=1}^K \left(y_i - \bar{y}\right)^2}}{\bar{y}},
$$
where $y_i$ is the average voxel signal in ROI $i$ and 
$$
\bar{y} = \frac{1}{K} \sum_{i=i}^K y_i,
$$
is the mean ROI signal.

It is always assumed that the cylinder axis is along the z-axis. If not the image
will have to transformed first.

As output this task produces to files: The first is a mask image file (in nifti-format),
that can be used to show the positions of the spherical ROIs on the input image. The second
contains the numerical result of the computation (The result, the standard error computed
from jackknife resampling and the value of $K$).

Note that the spherical ROIs will be created on the same grid as the input image. In case
of a coarse grid it might be a good idea to resample the image so that the resolution is at least
ten times higher than the ROI radius (i.e. if the ROI radius is 5mm, an image resolution of 0.5mm
is recommended). This will help avoid the spheres becoming too jagged.

Syntax:
```
> python -m nmiq bkgvar3d -i img.dcm -o res --resample 1,1,1 --center_x 10.5 --center_y 30.4 --start_z 980.1 --end_z 1102.1 --cyl_radius 80 --roi_radius 10
```
This will run the task with the following setup:
* The image will be loaded from the image file ```img.dcm``` and resampled to a resolution of 1mm in all dimensions
* The cylinder is centered that the physical point $x=10.5, y=30.4$ (relative to the origin).
* The cylinder starts at $z=980.1$ and ends at $z=1102.1$ (relative to the origin)
* The cylinder radius is 80mm
* The spherical ROIs will have a radius of 10mm
* A mask image file and the numerical results will be written put in the ```res```-folder.

#### lsf

This task is designed to measure line spread function FWHM from a phantom
containing one or more line sources. Given the approximate position of a slice of
line source, this task will calculate the FWHM in a given direction using the NEMA-algorithm
and by fitting a gaussian function to the line profile. 
Several source positions and directions can be given
in which case an average and a standard error is computed.

For a given source, the line profile will always be made to go through the maximum
intensity voxel. The position of that voxel is found by searching all voxels in the
neighbourhood of the center position.

It is always assumed that the line sources lie along the z-axis. If this is not the case
the image will have to be transformed first.

The output of the computation will be a text file containing the measured FWHM from
both the NEMA and gauss fitting procedures, as well as an image file showing the line
profile along with a depiction of the fits.

Syntax:
```
> python -m nmiq lsf -i img.dcm -o res --start_z 980.1 --end_z 1102.1 --center_x 10.5 20.1 --center_y 30.4 15.1 --radius 30 30 --direction x y
```
This will run the task with the following setup:
* The image will be loaded from the image file ```img.dcm```.
* There are two line sources of interest: one at $x=10.5, y=30.4$ and another at $x=20.1, y=15.1$
* The first line source will be measured in the $x$-direction with the correct $y$-index being automatically found within a 30mm distance from the center voxel
* The second line source will be measured in the $y$-direction with the correct $x$-index being automatically found within a 30mm distance from the center voxel
* The line profiles will include all voxels within 30mm from the center voxels.
* The numerical results and an image file showing the fits will be put in the ```res```-folder.