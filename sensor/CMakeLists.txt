# Top-level CMakeLists.txt file for the Casu Airflow Beaglebone firmware
cmake_minimum_required(VERSION 2.8)
project(airflow_sensor)

# Set up include directories
include_directories(${CMAKE_SOURCE_DIR}/i2c
                    ${CMAKE_FIND_ROOT_PATH}/include/)

# Casu firmware sources
set(airflow_sensor_SOURCES sensor/airflow_sensor.cpp
                           i2c/i2cDevice.cpp
                           i2c/i2cSlaveMCU.cpp)
                 
# Set -rpath-link linker flags, to prevent weird 2nd-order-dependency linker errors that cost me a handfll of gray hair
set(CMAKE_EXE_LINKER_FLAGS "-Wl,-rpath-link,${CMAKE_FIND_ROOT_PATH}/usr/lib/ -Wl,-rpath,${CMAKE_FIND_ROOT_PATH}/usr/lib/ -Wl,-rpath-link,${CMAKE_FIND_ROOT_PATH}/lib/arm-linux-gnueabihf -Wl,-rpath,${CMAKE_FIND_ROOT_PATH}/lib/arm-linux-gnueabihf")

add_executable(airflow_sensor ${airflow_sensor_SOURCES})
