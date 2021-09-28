### Share the site packages of the system's Python or a self-created virtual environment
Houdini ships with its own copy of Python, it's safer to use this copy, nonetheless, tedious to re-install every site packages. It's convenient to control the packages in the system Python's or a specific virtural environment and share it with Houdini's Python. You can achieve this by simply editing the $PYTHONPACKSPATH in the htoti.json file. The current version of Python with Houdini 18.5 is 3.7.4, hence we recommend installing a Python 3.7.4 and create a virtual environment, i.e.

- Linux and Python3.7.4
```shell
curl https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tar.xz --output Python-3.7.4.tar.xz
tar -xf Python-3.7.4.tar.xz
cd Python-3.7.4
# if you encountered the openssl problem while installing packages via pip
# then, you need to modify the setup dist file and re-compile from source
# please refer to: https://stackoverflow.com/a/5939170
make distclean
# then repeat below
./configure --enable-optimizations
make -j
# if you see ssl fatal error while make, refer to https://stackoverflow.com/questions/43131708/fatal-error-openssl-rsa-h-no-such-file-or-directory/43132137 for the solution
# install this python alongside the system default
sudo make altinstall
# assume PATH_TO_VENV to put the virtual environment and you are naming it as htoti_env
cd PATH_TO_VENV
python3.7 -m venv htoti_env
source htoti_env/bin/activate
# now you have activated this env
python3.7 -m pip install --upgrade taichi
# the site package will be installed in the folder "htoti_env/lib/python3.7/site-packages"
# Now set PYTHONPATH variable in the installation json file that you copied earlier to houdini_preference_folder/packages/, and good to go.
```

