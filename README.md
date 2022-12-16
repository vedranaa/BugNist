# Setup
*For vtk-based rendeing from python  at the g-bar server*

Start a VirtualGL node by opening a terminal `Applications -> DTU -> xterm(VirtualGL-application-node)`

Make a python environment, I slightly modified  Patrick's `init.sh`
```
#!/bin/bash
# Based on simple init script for Python on DTU HPC
# by Patrick M. Jensen, patmjen@dtu.dk, 2022

# Configuration
PYTHON_VERSION=3.9.14  # Python version
VENV_DIR=.  # Where to store your virtualenv
VENV_NAME=withVtk  # Name of your virtualenv

# Load modules
module load python3/$PYTHON_VERSION
module load $(module avail -o modulepath -t -C "python-${PYTHON_VERSION}" | grep "numpy/")

# Create virtualenv if needed and activate it
if [ ! -d "${VENV_DIR}/${VENV_NAME}" ]
then
    echo INFO: Did not find virtualenv. Creating...
    virtualenv "${VENV_DIR}/${VENV_NAME}"
fi
source "${VENV_DIR}/${VENV_NAME}/bin/activate"
```

Install vtk 
```
pip install vtk
```

Run test script with virtualGL
```
vglrun python red_cube_test.py
``` 
If a window opens with a rendering of a red cube, you're good to go! The window might open *behind* other open windows, so make sure to look for it before concluding that it did not work.

Additional installs for handling volumetric files  

```
pip install tifffile
```

# Use


Try using `showbug`, by typing one of the following
```
python showbug.py filename
python showbug.ph filename -surf
```

The code from the script `render_in_notebook` is written to be used interactively, for example in Jupyter notebook.

The script `save_screenshots.py` needs to know the source folder where to find tiff files and destination folder to store screensots.
