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

echo "DONE!"