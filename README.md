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
