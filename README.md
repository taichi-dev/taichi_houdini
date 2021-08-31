# Taichi MPM Solver to Houdini

A High-Performance Multi-Material Continuum Physics Engine as a Houdini extension.

## Instaling this plugin
### Using the Houdini "plugin" method (only for 17.5 and higher version)
Create a folder named packages (if not existed) in your Houdini preferences folder.
Copy the htoti.json file in this directory into the packages folder.
Edit the path for the environment variable $htotiLib to the Lib folder in this repo.

### Editing Houdini.env file directly (TODO)

### Share the system or a self-created Python's site packages
Houdini ships with its own copy of Python, it's safer to use this copy, nonetheless, tedious to re-install every site packages. It's convenient to control the packages in the system Python's or a specific virtural environment and share it with Houdini's Python. You can achieve this by simply editing the $PYTHONPACKSPATH in the htoti.json file. The current version of Python with Houdini 18.5 is 3.7.4, hence we recommend installing the same version and use that to create a virtual environment, i.e.

- Linux and Python3.7.4
```shell
curl https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz
tar -xf Python-3.7.4.tar.xz
cd Python-3.7.4
# if you encountered the openssl problem while installing packages via pip
# then, you need to modify the setup dist file and re-compile from source
# please refer to: https://stackoverflow.com/a/5939170
make distclean
# then repeat below
./configure --enable-optimization
make
# install this python alongside the system default
sudo make altinstall
# assume PATH_TO_VENV to put the virtual environment and the name is htoti_env
cd PATH_TO_VENV
python3.7 -m venv htoti_env
source htoti_env/bin/activate
# now you have activated this env
python3.7 -m pip install --upgrade taichi
# the site package will be installed in the folder "htoti_env/lib/python3.7/site-packages"
# adding it to the PYTHONPAHT in the htoti.json will let houdini use the package inside
```



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
