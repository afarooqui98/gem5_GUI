# GUI for gem5

## Dependencies
* PySide2 5.13.2
* shiboken2 5.13.2


## Installation
*Note:* This install process assumes you have already installed python**3.7.5**. Visit [here](https://www.python.org/downloads/release/python-375/) to download. Virtualenv can also be installed with ```pip install virtualenv```.
### Step 1
Clone our repository using:

    git clone https://github.com/afarooqui98/ECS193a.git

### Step 2
Make a new directory to contain the project files; create a virtual environment to manage installed packages and activate it.

    virtualenv -p python3.7 venv
    source venv/bin/activate



*troubleshooting:* Machines with multiple versions of python will have multiple names for each version. If ```-p python3.7``` doesn't work, you can replace with ```-p python3``` or even ```-p python```. Once your virtual environment is active, type ```python --version``` to ensure that you are using python 3.7.5

### Step 3
Download dependencies using:

    pip install -r requirements.txt

## Proof of Concept
In order to run the gui:

    python .\gui.py
