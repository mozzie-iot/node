#!/bin/bash

ls 

# cd ..

# sudo apt-get install gcc-arm-none-eabi libnewlib-arm-none-eabi
# sudo apt-get install build-essential
# sudo apt-get install cmake

# if ! git clone https://github.com/micropython/micropython.git ; then 
#     printf "Failed to clone micropython repo"
#     exit 1
# fi

# cd micropython/mpy-cross

# if ! make ; then 
#     printf "Failed to make in 'micropython/mpy-cross'"
#     exit 1 
# fi

# cd ../../

# if ! git clone -b v4.0.2 --recursive https://github.com/espressif/esp-idf.git ; then 
#     printf "Failed to clone https://github.com/espressif/esp-idf.git"
#     exit 1
# fi

# if ! ./esp-idf/install.sh ; then 
#     printf "Failed to run script: ./esp-idf/install.sh"
#     exit 1
# fi

# if ! source ./esp-idf/export.sh ; then 
#     printf "Failed to source script: ./esp-idf/export.sh"
#     exit 1
# fi

# cd micropython/ports/esp32

# if ! make submodules ; then 
#     printf "Failed to make submodules in 'micropython/ports/esp32'"
#     exit 1
# fi 



echo "DONE!"