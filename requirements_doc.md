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

## Requirements

* As a researcher, I can easily design and test new architectures to shorten the development time. 

* As a user, I can easily modify simulation object parameters to easily configure and test different systems.

* As a user, I can create new simulation objects derived from existing objects to develop new architectures.

* As a user, I can export the model into different file formats, such as JSON and python files, to examine the configuration scripts and make optimizations if necessary.

* As a user, I can save model files and access them later to make cross system development easier.

* As a user, I can run simulations from the GUI directly via a one click simulation button to shorten development time. 

* As a researcher, I can parameterize objects and run multiple simulations in parallel over these object parameters in order to determine the optimal configurations.

* As a user, I can visualize simulation results and compare results between different simulations and architectures to easily compare and contrast different systems.

* As a user, I can drag and drop new SimObjects into a model and connect them with wires.

* As a user, I can use shortcut keys (hot keys) to perform common tasks such as selecting a wire or run simulation.

## Technologies Employed
Our GUI will be implemented in Python, using the GUI development framework PyQt5. For the development process, we will use a linux virtual machine running Ubuntu 18.04. We will study the existing GEM5 code base to maintain consistency between the GUI and the backend software. We will also be using JIRA as our product management tool to develop tasks as well as communicate with our client and other gem5 contributors. 

## Cost Analysis
Since there is no hardware costs and all the technologies are free to use, we have no monetary costs to consider. 

## Social and Legal Considerations
Our GUI for gem5 will be an open source project. This means that a multitude of users can use, modify, and share the work. Currently, all the files in the gem5 distribution have licenses based on BSD or MIT license. For our GUI we will be employing an MIT open source license. 
