# Taichi MPM Solver to Houdini

A High-Performance Multi-Material Continuum Physics Engine as a Houdini extension.



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
### Call Taichi in the Houdini Python shell
Append this path to PYTHONPATH the evironment variable then, try the following line in your houdini python shell
```python
from htoti.fractal import *
fractal.draw()
```
