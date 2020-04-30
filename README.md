# GUI for gem5

## Dependencies
* PySide2 5.13.2
* shiboken2 5.13.2


## Installation
*Note:* This install process assumes you have already installed python**3.6** or later. Visit [here](https://www.python.org/downloads/release/python-375/) to download. Virtualenv can also be installed with ```pip3 install virtualenv``` (see step 2).

### Step 1
Clone our repository into the gem5 repository using:

    git clone https://github.com/afarooqui98/ECS193a.git

### Step 2 (Optional)
Create a virtual environment to manage installed packages and activate it.

    virtualenv -p python venv
    source venv/bin/activate



*troubleshooting:* Machines with multiple versions of python will have multiple names for each version. If ```-p python``` doesn't work, you can replace with ```-p python[version]```. Once your virtual environment is active, type ```python --version``` to ensure that you are using python 3.6.+

### Step 3
Download dependencies using:

    pip3 install -r requirements.txt


## Proof of Concept
In order to run the gui:

    <gem5.opt path> gui.py

You may need to specify the gem5 root directory if the above yields import errors. On the command line:

    GEM5_HOME=<path to gem5>
    
## Importing objects from config scripts
You can import custom made simobjects from python scripts into the gui. However before doing so you need to include the following code snippet in your script. 

    import sys, os
    sys.path.append(os.getenv('gem5_path'))
