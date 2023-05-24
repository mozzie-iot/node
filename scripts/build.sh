#!/bin/bash

sudo apt-get install gcc-arm-none-eabi libnewlib-arm-none-eabi
sudo apt-get install build-essential
sudo apt-get install cmake

if ! git clone https://github.com/micropython/micropython.git ; then 
    printf "Failed to clone micropython repo"
    exit 0
fi

if ! cd micropython/mpy-cross ; then
    printf "No directory: micropython/mpy-cross"
    exit 0
fi

if ! make ; then 
    printf "Failed to make in 'micropython/mpy-cross'"
    exit 0 
fi

if ! cd ~ && git clone -b v4.0.2 --recursive https://github.com/espressif/esp-idf.git ; then 
    printf "Failed to clone https://github.com/espressif/esp-idf.git"
    exit 0
fi

if ! ./esp-idf/install.sh ; then 
    printf "Failed to run script: ./esp-idf/install.sh"
    exit 0
fi

if ! source esp-idf/export.sh ; then 
    printf "Failed to source script: ./esp-idf/export.sh"
    exit 0
fi

echo "DONE!"