# Taichi MPM Solver to Houdini

This repository is for embedding the existing [taichi-element](https://github.com/taichi-dev/taichi_elements), a High-Performance Multi-Material Continuum Physics Engine, as a Houdini extension. So that you can benefit from the both flexibility for preprocessing via Houdini and the high performance via the ti engine.

## Installing this plug-in
This plug-in only supports **the Python3 Houdini with version >=17.5**

### Houdini "plug-in" method

- Create a folder named packages (if not existed) in your Houdini preferences folder.
- Copy the htoti.json file in this directory into the packages folder.
- Edit the variable $htotiLib to the `Libs` folder of this repo.

### Share the site packages of the system's Python or a self-created virtual environment
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
# Now set PYTHONPATH the directory containing this virtual environment's site packages, and you are good to go.
```

### Installing under the Houdini directory
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

### Use Taichi in the Houdini Python shell
You can use Taichi in Houdini just like in any other normal Python shells. Try the following in any Python shell in your Houdini.
```python
import taichi as ti
ti.init()
from htoti.fractal import *
fractal.draw()
```

## Introduction to the MPM plug-in
Navigte to the  `Examples` folder, we will start with the simplest `mpm88.hip` demo.

### MPM 88 and the ideas behind the plug-in

### HToTi-MPM asset

### Editing the emitors in Houdini, FREELY

### Making the materials

### Adding analytical collisions

### Saving the cooked results via the ROP_geometry node



## Known issues and TODO list

Known issues:

- **Editing a connected MPMSolver node will not update the hda.** If you would like to contribute to **this hda,** always remember to sync your update to an unlocked, isolated htotiMPMSolver node after testing well, then lock and save it.
- **Reseting the simulation, or modifying the SOP network prior to the MPM solver.** This operation will dramatically slow down the following solving, try to save all the modifications then, restart Houdini.



ti-element-back-end:

- CUDA has bug in Houdini
- Support modifying the parameters: 1. 2. 3. after having created the MPM solver
- SDF/volume based collision
- Slippery spherical collision
- Analytical box collision
- Moving collision
- Per-particle physical properties: 1. 2. 3.



Houdini-front-end:

- SDF/volume based collision
- Slippery spherical collision
- Analytical box collision
- Moving collision
- Visualization flag for collision objects
- Sub-frame update for the emitor and/or collision object
- Results Dumper





