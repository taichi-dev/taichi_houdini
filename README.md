# Taichi MPM Solver to Houdini

A High-Performance Multi-Material Continuum Physics Engine as a Houdini extension.

## Instaling this plugin
### Using the Houdini "plugin" method (only for 17.5 and higher version)
Create a folder named packages (if not existed) in your Houdini preferences folder.
Copy the htoti.json file in this directory into the packages folder.
Edit the path for the environment variable $htotiLib to the Lib folder in this repo.

### Editing Houdini.env file directly (TODO)

### Share the system or a self-created Python's site packages
Houdini ships with its own copy of Python, it's safer to use this copy, nonetheless, tedious to re-install every site packages. It's convenient to control the packages in the system Python's or a specific virtural environment and share it with Houdini's Python.
You can achieve this by simply editing the $PYTHONPACKSPATH in the htoti.json file.

### Instaling Taichi for Houdini
If you insist to manage the packages in the Python shipped with Houdini manually, follow the steps below.

- Linux
```shell
cd path_install_houdini/python/bin
./python -m pip install --upgrade taichi
```

- Windows
Navigate to the installation directory of Houdini, and dive into the Python folder (i.e. python37). In the case pip.py doesn't exist, you need to [download pip](https://bootstrap.pypa.io/get-pip.py) first, then open the windows terminal in this folder and type

```shell
python3.7.exe get-pip.py
python3.7.exe -m pip install --upgrade taichi
```

## Examples
### Call Taichi in the Houdini Python shell
Try the following line in your houdini python shell.
```python
from htoti.fractal import *
fractal.draw()
```
### Use Taichi in the Houdini Process
Navigte to the  examples folder, and open the mpm88.hip file. TODO add a simple tutorial for self-created geometries as emittor.
