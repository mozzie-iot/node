#!/bin/bash

sudo apt-get install gcc-arm-none-eabi libnewlib-arm-none-eabi
sudo apt-get install build-essential
sudo apt-get install cmake

git clone git@github.com:micropython/micropython.git

cd micropython/myp-cross
make

echo "DONE!"