# Taichi MPM Solver to Houdini

A High-Performance Multi-Material Continuum Physics Engine as a Houdini extension.

## Use system's or self-created Python
it's safer to use the system's own version of python, or a seperate virtual python environment you created. On Windows, this can be achieved by PC Settings->Advanced system settings->System Properties->Environment Variables. On Linux, you can simply append or create PYTHONPATH in the bash config files. Make sure the python version you redirect to is consistent with Houdini's.
## Instaling Taichi for Houdini
- Linux
```shell
cd path_install_houdini/python/bin
./python -m pip install --upgrade taichi
```

While calling pip module, if it appears "libffi.so.6: cannot open shared object file: No such file or directory". Check out this [solution](https://stackoverflow.com/questions/61875869/ubuntu-20-04-upgrade-python-missing-libffi-so-6/63329830#63329830):

```shell
# Download 19.10 version of the package from here: 
weget http://mirrors.kernel.org/ubuntu/pool/main/libf/libffi/libffi6_3.2.1-8_amd64.deb
# then install manually:
sudo apt install ./libffi6_3.2.1-8_amd64.deb
```

- Windows
Navigate to the installation directory of Houdini, and dive into python37. You need to download pip first. Download the [get-pip script](https://bootstrap.pypa.io/get-pip.py) if it doesn't exist in the folder, then

```shell
python3.7.exe get-pip.py
python3.7.exe -m pip install --upgrade taichi
```

## Instaling this plugin
### Adding it to the Houdini environment
Houdini 17.5 or higher ("plugin" method)
Create a folder (if not existed in your Houdini preferences folder) named packages.
Copy the htoti.json file into the packages folder.
Edit the path for the environment variable $htotiLib to point to the Lib folder.

Editing Houdini env file directly
Note: currently we need to import solvers as modules in the python SOP of houdini, so python needs to be able to read the current package locations.
Append this The Libs directory to PYTHONPATH in the evironment variable in the houdini.env in your Houdini preference folder.

## Examples
### Call Taichi in the Houdini Python shell
Try the following line in your houdini python shell.
```python
from htoti.fractal import *
fractal.draw()
```
### Use Taichi in the Houdini Process
Navigte to the  examples folder, and open the mpm88.hip file. TODO add a simple tutorial for self-created geometries as emittor.
