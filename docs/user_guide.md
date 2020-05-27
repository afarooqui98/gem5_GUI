
# **gem5 GUI: User Guide**


## **Table of Contents**

- [1. Preface](#preface)
  * [1.1 README](#readme)
  * [1.2 Audience](#audience)
  * [1.3 Contact Us](#contact-us)
- [2. Overview](#overview)
  * [2.1 Background](#background)
  * [2.2 Description](#description)
  * [2.3 Approach](#approach)
  * [2.4 Technical Specifications](#technical-specifications)
- [3. Installation and Setup](#installation-and-setup)
  * [3.1 Prerequisites](#prerequisites)
  * [3.2 Basic Setup](#basic-setup)
  * [3.3 Running the application](#running-the-application)
- [4. Features and Functionality](#features-and-functionality)
  * [4.1 GUI Overview](#gui-overview)
  * [4.2 Catalog View](#catalog-view)
  * [4.3 Attribute Table](#attribute-table)
  * [4.4 Wiring](#wiring)
  * [4.5 Context](#context)
  * [4.6 Menu Overview](#menu-overview)
  * [4.7 Run](#run)
  * [4.8 Debug](#debug)
  * [4.9 Import and Export UI Objects](#import-and-export-ui-objects)
  * [4.10 Import SimObject](#import-simobject)
- [5. Troubleshooting](#troubleshooting)
  * [5.1 Could not load Qt platform plugin even though it was found](#could-not-load-qt-platform-plugin-even-though-it-was-found)
  * [5.2 ImportError: No module named PySide2](#importerror:-no-module-named-pyside2)
- [6. Appendix](#appendix)
  * [6.1 Requirements](#requirements)
  * [6.2 Technology Survey](#technology-survey)
  * [6.3 FAQ](#faq)
  * [6.4 Github Repository](#github-repository)
  * [6.5 Glossary](#glossary)
- [7. Future](#future)


## 1. Preface

### 1.1 README

This user guide covers setup, installation, and usage of the gem5 GUI. The purpose of this guide is to provide users with a high-level understanding of the features and components of the GUI, answer any questions about its operation, and highlight differences between the configuring architectural simulations via scripts and via the gem5 GUI.

### 1.2 Audience

This user guide is meant for both existing gem5 users looking to develop simulations using the GUI [[Bobby] Do you really want to frame this as en entry point for beginners? I feel that's a bit out-of-scope. I'd make this more broad, something like "This user guide is intended for those who wish to carry out architectural simulations using gem5's GUI interface, as opposed to the use of configuration scripts"] and new users who are unfamiliar with how gem5 works]. For new users, highlighted terms and sections will indicate background information necessary for understanding the proper usage of the GUI. Experienced users can skip these sections.

### 1.3 Contact Us

[[Bobby] Very brave of you... are you sure? :)]

- Ahmed Farooqui

	- [amfarooqui@ucdavis.edu](mailto:amfarooqui@ucdavis.edu)

- Ravishdeep Singh

	- [ravishdeep10@gmail.com](mailto:ravishdeep10@gmail.com)

-  Rohit Dhamankar

	- [rohit.dhamankar@gmail.com](mailto:rohit.dhamankar@gmail.com)

- Shivam Desai

	- [shivamd50@gmail.com](mailto:shivamd50@gmail.com)


## Overview

![](https://cdn.fbsbx.com/v/t59.2708-21/100914476_177123480350163_4173079852171132928_n.gif?_nc_cat=106&_nc_sid=041f46&_nc_ohc=7tJE3wy0YPAAX-M2Pxs&_nc_ht=cdn.fbsbx.com&oh=173b2536760b7a324eb0ad9e959a22f9&oe=5ECEF05B)

### 2.1 Background

Currently, gem5 is an open source project used to simulate computer architecture. gem5 was originally developed for computer architecture research withinin academia. However, it has since been extended and found use in industry, full computer system design, and as an education tool for computer architecture students. Most gem5 development involves specifying architectural models via python scripts. Though powerful, this introduces a steep learning curve to the product. To make gem5 more accessible and user-friendly, we have created a graphical user interface for gem5; the details of which are outlined in this document.

### 2.2 Description

[[Bobby] I think we could afford to be more high-level here and save the details fo the exact layout for later in the document (the following "Approach" section and the "GUI overview" seems most appropriate for this). Very rough starting point: "We developed a user interface whichs allows users to search through a library of simobject, configure them, and place them in an architectural heirarchy to then be instantiate and simulated..."]

We developed a user interface that allows users to search for simobjects in a left hand catalog, place them in the canvas, and move them around to create an architectural hierarchy that can then be instantiated and simulated. Selecting an object allows a user to modify parameters in the attribute table on the bottom left. Placing objects inside other objects establishes a parent-child relationship. Drawing wires using the wire tool allows for port connections between objects.

### 2.3 Approach [[Bobby] Can we rename this? This seems more like "Design" than approach]

[[Bobby] Reading back over this (2nd pass), I still don't really know what this section is about. What's its purpose? What key points are we trying to communicate here? It seems redundant given the sections that follow it]

[[Bobby] I'd rephrase this below. The diagram is helpful in describing your approach. I wouldn't cast it aside by mentioning it was a first-draft or some kind of diagram you found useful early on. You also slip into past tense here a lot ("Our GUI had a distinct front-end and back-end"), does it not so much anymore? If so, explain, or make it present tense --- likewise for elsewhere in the document if applicable]

The image below was our initial diagramming of the basic structure of the GUI, as well as a very high level overview of interaction with our &quot;back-end&quot;, which in this case was the gem5 repository. Our GUI had a distinct front-end and back-end, which were linked by a State class and the SymObject class.

Front-end: The primary UI interaction and design comprise the front end. Dragging and dropping objects, selecting them, and highlighting multiple objects are all part of the front-end. The classes that encapsulate this behavior are LineDrawers, which allow the user to draw ports between objects; GraphicScene, which allows the interaction between the SymObject instance; and multiple different View classes that represent each portion of the user interface. The State class is used to maintain real-time information about the context of the GUI that is accessible across files. As most of the objects built were subclassed from PySide, most of these objects were either QWidgets or QMainWindows.

Back-end: The front and back-end are tightly coupled. Any of the objects selected and dragged to the canvas are mapped to [[Bobby] You've mentioned SimObjects at least once before this point. Could we have a definition further up when it's first declared also?] &quot;SimObjects.&quot; These &quot;SimObjects&quot; define the schema and function of a particular computer architectural entity, like a CPU, for example. We refer to this list of objects as the &quot;catalog&quot; which dynamically loads all of the SimObjects at program initialization. Users are then able to select the component they want from the catelog via a categorized and searchable menu. Each selected object os its own instance of a specific SimObject. Each of these objects contain varying parameters including some that have default values and others that need to be specified by the user. The description of the objects and their parameters are also loaded from gem5 and can be viewed via tooltips. Furthermore, users can use the gem5 guo to save their work and subsequently export to a file format suited for running in the gem5 simulation environment. [[Bobby] Can you state what those file formats are?]. 
![](https://lh3.googleusercontent.com/wjVauYFnztL0aIxrHWjf-dgybE87O4_nTb2dcB3mOpZezpZfnenHZ8csDD0EOwaGaCWd_c1Ysb6HSWvdz-mbfKwMAkVXUMrjLwsyyg4A2aR-Pl3OSn_T2r-zHbBRMiNR1s6pEdnF)

### 2.4 Technical Specifications

#### 2.4.1 PySide2

We decided to develop the GUI using Python. Therefore, the natural choice was to use the Python binding for QT, one of the most popular GUI development libraries. We chose PySide2 over PyQt5 as would require a commercial license for release.


## 3. Installation and Setup

### 3.1 Prerequisites

[[Bobby] This reads a bit 'clunky' to me. Consider rephrasing to something like "The gem5 GUI builds atop gem5. gem5 must be compiled and run within a linux operating system..."

gem5 requires the linux operating system to run, [[Bobby] Let's not undersell ourselves, this is gem5 restriction, not specifically one with the GUI] ~~so the GUI does not support cross platform developmen~~. You need to have a compiled gem5 installation on your machine as well. Visit [gem5 download](http://www.m5sim.org/Download) for instructions on how to setup gem5.

[[Bobby] Please don't reference m5sim.org. It's ancient (and should be removed). If there are anyother instances of this in the documentation please change to an equivelant page on gem5.org. In this case, gem5 building and download instructions can be found here: http://www.gem5.org/documentation/general_docs/building]

[[Bobby] What version of Python are you using? I'm assuming Python2? Or does the GUI work with Python3? Either way, it's a prerequisite for running this.]

### 3.2 Basic Setup

To begin the setup process, clone the [repository](https://github.com/afarooqui98/gem5_GUI) directly into the gem5 directory. Once complete, enter into the gem5\_GUI directory and download the dependencies using:

[[Bobby] pip3 is for Python3, no? Are we using python3?]
```pip3 install -r requirements.txt```

### 3.3 Running the application

Once the dependencies are installed, users can run the GUI with the command:

```<gem5.opt path> gui.py```

[[Bobby] It might be nice to have that "help with setup and running issues" in this document, even if it is a bit redundant]
See the README.md file in the repository for help with setup and running issues.

## 4. Features and Functionality

### 4.1 GUI Overview

Attached below is a view of the GUI on successful launch:

**![](https://lh5.googleusercontent.com/CFVJ2WTCP-fm_eeWc1hU_a3kHUz9TNeFe7y2UpBRp8JfrFWwZfPxxWh_QshoAuESh_zDqXyp6_G2bf4PeKuDuI4COeeS1KNhSxXhTHBsy2ZYZX60d6R73K4BQ3e6vQ5xgj8yhwSs)**

On the left side lies the **catalog view** as well as the **attribute view**.

The former is used to select a SimObject, and the latter will be used to configure a selected SimObject. The majority of the screen is populated by the **canvas**. This is where most of the user interaction will occur, and where users will build their system. The menu bar contains multiple convenience functions typical to GUI software, from copy-pasting to file saving, but there are also tabs for **debugging** , **running** , and **importing**. These are key functions of the GUI that work in tandem with gem5 to provide the users with the ability to check their system configuration, import both ui objects and configured subclasses, and instantiate their systems. [[Bobby] It took me a few attempts to understand what the following sentance meant. How about "The buttom for drawing ports between objects can be found directly below the 'File' menu button"]. Underneath the top menu is a button that allows the user to draw ports between objects

### 4.2 Catalog View

**![](https://lh5.googleusercontent.com/iv-iXWbl-zvDkwHlkJ9Adlp4xjj-vP9g_kb4yZYRMtSTrtOUnrlsVTdY73JieBOCWHBDno7JHm0YxuohtawUyQ5tb1EjewX45XU6Q5Z8NOC8WoIYGeZECXX4tcqR5dfbEmMt7Hp6)**

The catalog holds all the available SimObjects. Users can maneuver the tree view by specific category or search for an object via the search bar. Double clicking an object places what we call a SymObject on the canvas. A SymObject is a GUI representation of an gem5 SimObject that allows a user to interact with it in a tactile way.

### 4.3 Attribute Table

**![](https://lh3.googleusercontent.com/gxPj5FWqqfpwkIxH--c_LYTa0eCnfYEqxaqX2iR7ZFf9UwyQQSWjLWBjjDDfbSJrE-0oWVk9rkpOMOZnRdcNzUXfyP8h1144lTWUn-Hgt96BeBitZqRTqXr8Bv8A6RCwkzb7kOdt)**

Selecting an object brings up its attribute table. This table lists the object name, every child object, as well as all the object parameters. The parameter fields are modifiable, while the &quot;Name&quot; and &quot;Child Objects&quot; fields are only viewable. Hovering over the parameter name gives a description of the parameter, hovering over the value shows the type. Attributes for the specific object may also be searched for, aside from the &quot;Name&quot; and &quot;Child Objects&quot; parameters, which always lie at the top of the table.

### 4.4 Wiring

To enable wire drawing, click the wire icon between the menu and the catalog. While in wire drawing mode, objects cannot be interacted with. Clicking this button changes the cursor to a cross hair, allowing the user to connect ports with wires. Failing to connect two ports or connecting incompatible ports will result in an error message. Right clicking a wire brings up a context menu, which will allow for deletion and inspection.

**![](https://lh5.googleusercontent.com/k3X4PbsV-p_0oNeMGzexuSvBhwoxifQ28G0GGwRPh3QdDB7Q_zl1dCq-dSx7yF7OOA5lsIbB2maPyrQl_yaHlal2H-QIfMKeph4FpgnbwPfTdk0qWnVR9CFmdGq7VeEDV1wT5I9Q)**

### 4.5 Context

An important part of understanding the gem5 GUI is the way user context works. Whenever an object is created or selected, it is set as the current selected SymObject. Selected objects are typically highlighted in green, unless there are required attributes that need to be set by the user; then, the object is red. Any time an object is selected, the user can move it around freely and resize it in the canvas, with its attributes populated in the attribute table. Finally, it&#39;s important to note that wiring _is not_ dependent on the current context, so any ports for any objects may be connected to others regardless of whether they are in context.

### 4.6 Menu Overview
The menu contains tools to interact with the GUI. Most of these correspond to self explanatory standard window functionality, and all options in the menu correspond to a keyboard shortcut.

### 4.7 Run

**![](https://lh3.googleusercontent.com/w7zPXdpEmfvKHBrRCVVazTPXdZGHD4JeemIjvkwXMbomtK5lTdlMmlwplL3d6lF66SYRkinzCPXO1FbHSE4Ou-RjZbbX17yxBO1zkqwt6NBYw23eF7eRHQUiYMHP_WxubpwfzqVR)**

The run tab contains the instantiate and simulate option. Please note both are greyed out until a user drops in at least a root object to prevent the user from instantiating without a root. Once the instantiate button is pressed, the user _must_ save the file (since objects cannot be modified once instantiated), after which the results of instantiation are displayed within the command line. Once instantiation is complete, the user can press the simulate button, which will begin the simulation of the design with the output in the command line interface.

### 4.8 Debug

**![](https://lh4.googleusercontent.com/Plh1yAE1Sx3wgVY3w-fHRgmEh1ZyY2uCe0O2SX1984lYe4kgiUJH-C6_2aLZngWX0-eraXf8m--xC--ouErySfQJFGbAkLe-TuzNa3O5QKRf6F-UAThoJ5oyWi0KRsgLLH6LQVU2)**

By pressing the Debug button on the toolbar, the debug window will appear on the right side of the GUI. There will be two checkboxes: &quot;Log to File&quot; and &quot;Log to Stdout,&quot; with the former being set automatically. Logging to file will send debug and error messages to a file which can be renamed at any time in the text below. Logging to stdout will print these messages in the Terminal application running the GUI. Below these options is a table of debug flags that native to the gem5 system. These flags can be set and unset, and result in different gem5 debug messages. They are also searchable by an accompanying search bar.

### 4.9 Import and Export UI Objects

**![](https://lh3.googleusercontent.com/siEBwmcd6tGS7QHymwpDtJK7Is0zEQFH30jnCnhSTcjVKfo7rD3oPJskbw_Cty_lu05ifpWIkkwO3wKJqMoDKqtL7XqrEgVqwAXp9X57DmRIjZqkMRpErWt1kLeJYvXZ9Qn2YftK)**

Under file, we have import and export UI object, which allow users to save and load clusters of SymObjects. Exporting saves the configuration as a .obj file, which is in a JSON format [[Bobby] Remind me again, why are we saving to .obj even if this is in a JSON format?]. Importing places the custom object in the catalog, allowing for the same access methods as regular SimObjects.

### 4.10 Import SimObject

**![](https://lh6.googleusercontent.com/4ZZ0gDvbqz6o9YIB4-pHTZUBB2Cpxwd7CnC2szd_-dy-fO88NMUCzU1I6YmRTR_oSYgk5wgHl8gce3AAXd3RF7iRJcIZ9mU-qgJyBx13WN-7Ploe03yXLUQHQBnSpfUOaNo-AJoB)**

Users can import custom SimObjects, which are python classes inherited from base SimObjects. These imports appear under the catalog, and can be similarly added to the GUI just like regular objects. Imported SimObjects are saved as part of a .ui file, so you do not need to import again when opening a .ui file with imported SimObjects.

## 5. Troubleshooting

### 5.1 Could not load Qt platform plugin even though it was found

This error can come up if you ssh into a machine to run the GUI. Including the -Y option may fix this error

### 5.2 ImportError: No module named PySide2

When running the GUI this error might appear. This usually means either of the following has occurred:

- PySide2 was not installed. Use `pip show PySide2` to make sure it is installed on your machine and if not make sure to run `pip -r install requirments.txt`
- When installing PySide2 in a virtual environment it can become binded to a particular version of Python that is not being used in the virtual environment. If PySide2 is installed and you are using a virtual environment to run the GUI, try going through the installation steps again without the virtual environment.

## 6. Appendix

### 6.1 Requirements

Must Haves:

- Users can drag and drop new SimObjects into a model and connect them with wires.

    - Each SimObject has a GUI representation which is then stored in what we&#39;ll refer to as a &quot;catalog&quot;
      - These objects will be generated dynamically from the current SimObjects available in gem5
      - Users can &quot;import&quot; more objects by pointing to a python file with SimObject classes defined
      - SimObjects will be initialized in the GUI, which will allow users to modify the parameters for a specific instance of that SimObject
    - An object can be selected, which will bring up its modifiable parameters which will allow the user the change them as necessary
    - Connecting two objects is a matter of dragging a wire from one **port** to another
- As a user, I can easily modify simulation object parameters to easily configure and test different systems

    - Some parameters will have default settings based on the type of object selected
 In the attribute selection view hovering over each parameter should display a description of that parameter
- Users can save model files and access them later to make cross system development easier.
- As a researcher, I can easily design and test new architectures to shorten the development time.

    - The software should be able to manage multiple designs and load multiple files without any significant performance hit. The most expensive operation should happen at file export, where (ideally) code is generated for a user to run with the gem5 compiler.

Should Haves:

- Users can export the model into a JSON file format

    - The current plan is to allow the user to export to different files formats, like a python configuration script, for the obvious purpose of allowing users to continue development in Python if necessary. The actual simulator will be a tertiary feature that we&#39;ll account later down the line
- Users can create new simulation objects derived from existing objects to develop new architectures.
- As a user I will be able to select multiple objects and save them to the aforementioned catalog.
- Users can use shortcut keys (hot keys) to perform common tasks such as selecting a wire or run simulation.

    - Copy, Paste, Cut, multiple selection (will not bring up an attribute screen but will allow multiple objects to be moved around)

Could Haves:

- Besides a JSON file, users can export a design to multiple file formats, primarily to a python configuration script that can be essentially immediately run.
- As a user, I can visualize simulation results and compare results between different simulations and architectures to easily compare and contrast different systems.
- Users can run simulations from the GUI directly via a one click simulation button to shorten development time.
- Parameterize objects and run multiple simulations in parallel over these object parameters in order to determine the optimal configurations.

### 6.2 Technology Survey

[[Bobby] I take it this is still under construction? I'll just ignore it for now]
#### 6.2.1 Virtual Machine

Parallels

VirtualBox

VMWare Workstation

#### 6.2.2 Linux Distribution

Ubuntu

Fedora

Red Hat

Debian

#### 6.2.3 GUI

- Qt
  - Pros:
    - Cross-platform
    - Suggested by client
    - Extensively used by many organizations
    - Lots of documentation and tutorials
  - Cons:
    - No experience using it
- Kivy
  - Pros:
    - Cross-platform
    - Written in C and graphics engine is built in OpenGL Es2
    - Well integrated with Pycharm
    - Free to us under MIT license
  - Cons:
    - No experience using it
    - More suitable for developing games not really used for desktop apps
- GTK:
  - pros:
  - cross-platform
  - written in c, but has support for other languages
  - no licensing restrictions
  - cons:
    - no experience using it
- TKinter: (python)
  - pros:
    - simple, open source
    - bundled with python
    - lots of resources / tutorials
  - cons:
    - not as aesthetic as other technologies

### 6.3 FAQ [[Bobby] Good! I like this!]

#### 6.3.1 How do I know if I am in the wire drawing mode or selection mode?

- When in wire drawing mode, the wire tool icon will be &quot;pressed&quot; and the cursor will become a crosshair.

#### 6.3.2 How frequently is the catalog updated?

- The catalog is dynamically loaded from the gem5 repository whenever the GUI is launched.

#### 6.3.3 I instantiated a model but I forgot to specify some parameters, how can I modify them?

- Unfortunately, you cannot modify the model after instantiation because objects cannot be deleted and created again. To change parameters, open a new GUI file and load your saved UI file.

#### 6.3.4 How come when I place objects very near to each other but not overlapping they get added as children?

- The resize handles of the object are included in the collision detection between objects, so if they overlap (even when invisible) the GUI will interpret the action as placing an object in another.

### 6.4 Github Repository

[https://github.com/afarooqui98/gem5\_GUI.git](https://github.com/afarooqui98/gem5_GUI.git)

### 6.5 Glossary

- gem5: a computer architecture simulator

- SimObject: a standard gem5 object
- SymObject: a UI object with a pointer to the gem5 SimObject
- QWidget: the base class object for all UI objects, used as a basis for SymObjects
- QMainWindow: the base class for window management, used for the GUI layout

## 7. Future

Over the course of development, we have faced hurdles and came up with new ideas which we later implemented. We were therefore unable to allocate time to develop everything we had originally planned. Future development should focus on these features, as well as others that we believe are desired:

- Export to multiple file formats (current instantiation generates config.json)
- Visualization of simulation results, with comparison to other simulations
- Parameterize objects to allow for running multiple simulations in parallel and comparing results / identifying optimal parameter values

[[Bobby] Here, and in other parts of this document, you state users need to do this all through Github. Are we not going to upload this to Gerrit soon? If so, please update this documentation accordingly].
We have did our best to address bugs during development and through user testing. If you encounter a bug, please let us know by an [issue](https://github.com/afarooqui98/gem5_GUI/issues), submitting a [pull request](https://github.com/afarooqui98/gem5_GUI/pulls), or contacting us or the gem5 team directly [[Bobby] How?]. Please try to document the steps resulting in a fault, as well as including a screenshot of the terminal.
