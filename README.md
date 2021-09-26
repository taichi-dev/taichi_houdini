# Houdini To Taichi(htoti) Element

This repository is for embedding the existing [taichi-element](https://github.com/taichi-dev/taichi_elements), a High-Performance Multi-Material Continuum Physics Engine, as a Houdini extension. So that you can benefit from the both flexibility for preprocessing via Houdini and the high performance via the ti engine.

## Installing this plug-in
This plug-in only supports **the Python3 versioned Houdini >=17.5**

### Houdini "plug-in" method

Houdini will automatically create a preference folder upon your 1st luanch. On Linux, this folder is `$Home/houdini_version_number`. On windows, this folder is `$USER/Documents/houdini_version_number`. We will dive into this folder and install a json configure file to let Houdini where to search the plug-in.

- Create a folder named `packages` (if not existed) in your Houdini preferences folder.
- Copy the htoti.json file in this directory into the packages folder.
- Edit the variable $htotiLib to the `Libs` folder of this repo.

### Installing packages  under the Houdini directory
If you would like to manage the packages in the Python shipped with Houdini, follow the steps below.

- Linux
```shell
cd path_install_houdini/python/bin
python3 -m pip install --upgrade taichi
```
On Linux, you may encounter problem when importing packages in Houdini's Python because your the system Python's version is different, consider [creating a virtual environment](Misc/virtual_python_environment_linux.md).

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
from fractal import fractalClass
f = fractalClass(512)
f.draw()
```

If you open the `fractal.py`, you will find that the only thing we did is to pack an existing taichi demo solver into a ti_data_oriented class, but leaving an parameter for the front-end, in this case the Houdini, to set. You will find that the whole project is behind the idea that we combine the flexibility of Houdini and the performance of Taichi, merely with more parameters to set, and optimizations for the sake of performance.

You can see how to replicate this in Houdini by `Examples/fractal.hipnc`, although it's super slow and you might have noticed that taichi inits every frame. This is because Houdini losses the handler of the `fractalClass` every frame it re-executes the solver SOP, and we have to re-import or init() the taichi to avoid stack overflow. We discuss the solution in the later section.

<a href="https://github.com/taichi-dev/taichi/blob/master/examples/simulation/mpm128.py"><img src="https://github.com/yuanming-hu/taichi_houdini/blob/DOC/Misc/fractal.gif" height="320px"></a>

## Introduction to the MPM plug-in

### MPM 88 and the ideas behind the plug-in

The fractal solver doesn't need the previous frames information to push forward the simulation, meaning its a perfect demo for SOP cooking only. But to let the solver remember the previous frame information (and all finished frames), we also need help from the Built-in SOP Solver of Houdini TODO_ref.

Navigate to the  `Examples/mpm88.hipnc`, click running you will see below.

TODO gif of mpm88

Magic, the previous frames are remembered and used to push the simulation correctly. Don't panic, we will breakdown gradually. The overall network is below,  assuming the solver node just emits the correct position of particles at different frames, it basically says we are showing a constant colored background, and many small spheres to visualize the particles, easy.

TODO mpm88_net fig

Click into the solver, you find out that we basically create some physical properties, then merge the incoming, newly emitted particles into the existing particles, and somehow re-obtain the handler and let the ti-end knows the current state and advance. The emitors are merely points on 2 rotating ellipse which we believe you have 1,000 ways to create. The physical properties, for the mpm88 sovler, are just 2 point attributes Jp and C.

TODO mpm88_solver fig

All combined, it's working. Nonetheless, it worthy of mentioning that this implementation is neither efficient, nor compatible. In order to let the ti-solver knows the current state, we actually ti.init(), create a new solver class, the re-fill all the data from numpy array, which is super slow. The emitor and the material-maker are inside the solver and can't be edited easily. We solve these in our HToTi-MPM solver.

Overall, the above procedure defines the simplest form of any htoti solvers: 1. a solver written in taichi, packed as a ti.data_oriented class with proper parameter settings and apis; 2. a SOP Solver node containing the proper python scripts to use the ti solver, re-obtain the data, and advance the simulation 3. the input of emitors or other geometry SOP nodes to define what happens in the scence prior to the solving, and 4. the material-maker out of the sovler to create necessary attributes for the simulation.

### HToTi-MPM asset

### Making the materials, selecting parameters in the solver

Material-Maker is an independent, packed SOP node, whose solely purpose is to create point attributes for all the points of the incoming node's geometry. We have made 4 selectable materials, notably, not all of the creating point attributes will be used in the ti-element side, i.e. per particle density and Young's module is not yet supported. We keep the api here in the front-end to make things a bit easier ASA the back-end supports them.

TODO gif demo_3d

### Editing the emitors in Houdini, FREELY

The eimitors is going to the 0th input of the solver. The initial state of the geometry can be selected from the solver's menu directly. You can enjoy the 100% flexibility brought by Houdini and just merge the particles before feeding into the solver's 0th input.

TODO gif demo_2d, demo_crashing_snow_ball_at_sand_castle

### Adding analytical collisions

The analytical collision goes to the 1st input of the solver. We have made the analytical planes(walls) and the analytical spheres. We are looking forward to contribution concerning box, tets, moving analytical collisions, and generalized SDF based collisions.

TODO gif demo_wall

### Saving the cooked results via the ROP_geometry node

A quick tip from the Houdini side is to save your cooked results and do the post-processing later. We show below an example of asteroid of acid solutions crashing at our planet. Do protect the environment!

TODO gif demo_earth

## Known issues

- **Editing a connected MPMSolver node will not update the hda.** If you would like to contribute to **this hda,** always remember to sync your update to an unlocked, isolated htotiMPMSolver node after testing well, then lock and save it.
- **Reseting the simulation, or modifying the SOP network prior to the MPM solver.** This operation will dramatically slow down the following solving, try to save all the modifications then, restart Houdini.
