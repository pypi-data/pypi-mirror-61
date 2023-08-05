# SpaceRoom

By [YetiCraft](https://www.yeticraft.net), @CDEguia, and @jscott for [Eureka Room](http://www.theeurekaroombham.com/)

Code for running escape room hardware comprised of Arduinos and Raspberry Pi's running Rasbian.

## General Setup

The following section describes the setup process in generic detail.

1. First, create an SD card with the Raspbian OS (latest) image using the methods found [online](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).
2. Write ssh and wifi configs to the /boot partition so that both will be available upon first boot (with or without a screen attached)
   1. [Enable SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md#3-enable-ssh-on-a-headless-raspberry-pi-add-file-to-sd-card-on-another-machine)
3. Insert the prepared card and boot the device.
4. Connect to the device.

## Development

### Clone Repo

Clone this repo or copy the code to the target linux system.  To clone the repo to a Linux system, ensure that you have `git` installed properly and then use the following command from a terminal:

    git clone git@gitlab.com:growlf/eurekaroom.git

> This will expect that your SSH keys are installed on this system in the correct path.  

### Add system dependencies

Next, open a terminal shell and execute the following, which will update packages and install the system dependencies:

    sudo apt-get update && sudo apt install -y git python3-pip python3-tk libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev libopenjp2-7-dev libdbus-1-dev libtiff5
    pip3 install --user pipenv
    export PATH=$PATH:/home/pi/.local/bin # Add new path
    exit # Reboot the Pi

### Activate development ecmd

Next, open a terminal shell within the code directory to execute the following commands:

    pipenv shell
    pip install -e .

This will create and activate a local Python3 virtual environment that allows isolation from the system's copy of Python and it's libraries. This Python environment will be completely dedicated to this project and will not affect the system Python interpreter - nor be affected by it.

### Development Media

Next, add your media files (Images and Videos folders) into system.  It is recommended to use a layout similar to the following for default configuration:

    eurekaroom (project root, created from the git clone operation)
    |
    +-/bin
    | +-/ecmd (commandline tool)
    |
    +-/eurekaroom (module folder)
    | | ...(class definition files)  
    |
    +-/Media
    | | ... (misc media - should be none)
    | +-/Images
    | | ... (image files)
    | +-/Videos
    |   ... (video files)
    |
    +-/tests (test folder)
    | | ...(test files)  
    |
    +-/eurekanode.log
    +-/README.md
    +-/requirements.txt
    +-/Pipfile
    +-/Pipfile.lock
    +-/setup.py

### Developer Notes

The following are mostly links and random bits of info that the developers thought were important or needed to share with each other.

#### Development Environment

- Get [Visual Code](https://code.visualstudio.com/download), a graphical programing interface
- [Adding tests](https://code.visualstudio.com/docs/python/testing) to python code with Visual Code

#### Python

- [python3-tk](https://docs.python.org/3/library/tk.html), GUI framework for graphical interfaces using Tk
- [RPi.GPIO](https://sourceforge.net/projects/raspberry-gpio-python/), library to allow using the code on a NON-Raspberry Pi during development.
  - https://blog.withcode.uk/wp-content/uploads/2016/10/RPi_GPIO_python_quickstart_guide.pdf
- [gpiosimulator](https://gitlab.com/shezi/GPIOSimulator)
- [argparse](https://docs.python.org/3/howto/argparse.html), an option parsing library for command line processing
- [configparser](https://docs.python.org/3/library/configparser.html) a configuration file library.
- [Logging](https://docs.python.org/3/howto/logging.html) with python
- A guide to [Working with files in Python](https://realpython.com/working-with-files-in-python/)
  
#### Other

- [Real favicon generator](https://realfavicongenerator.net/)

## Production

For production purposes, each Eurekaroom node will run on a Raspberry Pi (version 3b or higher) with Raspbian (latest) as the OS.

### Install Eurekaroom

    pip install eurekaroom

Enable auto-login with `raspi-config`.

### Usage

To use the command utility, simply execute the following on the linux system in a terminal where you have installed the code:

    ./ecmd -h

> This will display a short description and command help content.

#### Setup

    ecmd -a -w -m PATH_TO_MEDIA -n displayname
    ecmd -s

> This will create a config file with the node specific info and ensure that the system runs the service correctly and as desired.

#### Auto start on boot

If eurekaroom was installed with the `pip install eurekaroom` command you can run:

    ecmd --installservice

> Else, set the autostart application in the auto-login account to be the `/full/path/to/ecmd -s` command.

Reboot and ensure the system is responding on the expected when port and to command line execution.

## Table of Contents

- [SpaceRoom](#spaceroom)
  - [General Setup](#general-setup)
  - [Development](#development)
    - [Clone Repo](#clone-repo)
    - [Add system dependencies](#add-system-dependencies)
    - [Activate development ecmd](#activate-development-ecmd)
    - [Development Media](#development-media)
    - [Developer Notes](#developer-notes)
      - [Development Environment](#development-environment)
      - [Python](#python)
      - [Other](#other)
  - [Production](#production)
    - [Install Eurekaroom](#install-eurekaroom)
    - [Usage](#usage)
      - [Setup](#setup)
      - [Auto start on boot](#auto-start-on-boot)
  - [Table of Contents](#table-of-contents)
