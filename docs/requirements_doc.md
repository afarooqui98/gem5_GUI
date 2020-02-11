# GUI for GEM5
### Team Brownies
#### Ahmed Farooqui, Ravishdeep Singh, Rohit Dhamankar, Shivam Desai

## Introduction

Currently, gem5 is a highly active open source project that simulates different experiments in Computer Architecture. The maintainers of gem5 originally developed this project for computer architecture research in academia. Given the scope of this project, however, this system can be used for computer system design, industry research, and for students in undergraduate architecture classes. The current software allows users to configure architectural models through python scripts. To make gem5 more accessible and allow new users to utilize all of its capabilities, the maintainers of this project want to create a user interface that will allow such ease of use and functionality. Our goal is to develop this front-end GUI integrated with gem5 in order to make configuring systems much more efficient.

## Glossary of Terms
* Gem5 - the current open source project used by research to configure computer architecture systems.
* SimObject - “Simulation Object”, individual components that can be individually configured and connected to other SimObjects to form a system. Examples include CPU, Cache, etc.

## System Architecture
![Sample Mockup for GUI](https://lh3.googleusercontent.com/Mt63W_M_vAmhWoj0TZRSEkX4HImpBlKc7CEHHW4LY3DWzmJIfQ8jLgpQIFRFAdGKx3nag5z9u1npWYqJejgRaT-A8lkSlHBF_XYKfpKS-qpZQwPz0ZaTyY9npvaBcDvN6mKt_2k)

Our primary architecture will be based on this general design mockup. There is a logical front and back end to this system, but physically they may exist in the same space. The categories are as follows:

Front-end: The primary UI interaction and design comprise the front end. Dragging and dropping objects, selecting them, and highlighting multiple objects are all part of the front-end.

Back-end: The front and back-end are quite tightly coupled, as all the objects that are draggable and selectable are mapped to what are called “simObjects” which define the schema and function of a particular computer architectural entity, like a CPU, for example. This list of objects will be colloquially known as the “catalog” which dynamically loads all of the simobjects at program initialization and allows users to select the component they want from a categorized and searchable menu. The description of the objects and their parameters are part of this category. Furthermore, users will commonly use this tool to save their work and subsequently export to a file format suited for running in the gem5 simulation environment. Finally, users will be able to save collections of objects within the GUI and then pull them from the aforementioned catalog, in a separate section dedicated to user collections

## Requirements

## Requirements

Must Haves:

* As a user I can drag and drop new SimObjects into a model and connect them with wires.

    * Each simObject has a Gui representation which is then stored in what we’ll refer to as a “catalog”

    * An object can be selected, which will bring up its modifiable parameters which will allow the user the change them as necessary

    * Connecting two objects is a matter of dragging a wire from one port to another

* As a user, I can easily modify simulation object parameters to easily configure and test different systems

    * Some parameters will have default settings based on the type of object selected

    * In the attribute selection view right clicking each parameter should show the option to display a description of that parameter

* As a user, I can use shortcut keys (hot keys) to perform common tasks such as selecting a wire or run simulation.

    * Copy, Paste, Cut, multiple selection (will not bring up an attribute screen but will allow multiple objects to be moved around)

* As a user, I can save model files and access them later to make cross system development easier.

* As a researcher, I can easily design and test new architectures to shorten the development time.

Should Haves:

* As a user, I can export the model into different file formats, such as JSON and python files, to examine the configuration scripts and make optimizations if necessary.

    * The current plan is to allow the user to export to different files formats, like a python configuration script, for the obvious purpose of allowing users to continue development in Python if necessary. The actual simulator will be a tertiary feature that we’ll account later down the line

* As a user, I can create new simulation objects derived from existing objects to develop new architectures.

* As a user I will be able to select multiple objects and save them to the aforementioned catalog.

Could Haves:

* As a user, I can visualize simulation results and compare results between different simulations and architectures to easily compare and contrast different systems.

* As a user, I can run simulations from the GUI directly via a one click simulation button to shorten development time.

* As a researcher, I can parameterize objects and run multiple simulations in parallel over these object parameters in order to determine the optimal configurations.



## Technologies Employed
Our GUI will be implemented in Python, using the GUI development framework PyQt5. For the development process, we will use a linux virtual machine running Ubuntu 18.04. We will study the existing GEM5 code base to maintain consistency between the GUI and the backend software. We will also be using JIRA as our product management tool to develop tasks as well as communicate with our client and other gem5 contributors.

## Cost Analysis
Since there is no hardware costs and all the technologies are free to use, we have no monetary costs to consider.

## Social and Legal Considerations
Our GUI for gem5 will be an open source project. This means that a multitude of users can use, modify, and share the work. Currently, all the files in the gem5 distribution have licenses based on BSD or MIT license. For our GUI we will be employing an GNU lgpl open-source license.
