# casu-airflow

Driver code for the BBG controlling the FESTO pneumatic valves and airflow sensor.
It acts as a proxy to the valves for ohter CASUs.

## Prerequisites

The following packages need to be installed on the BBG

`sudo pip install pymodbus`

## Deployment

The BeagleBone controlling the valves must have hostname `bbg-airflow` and IP address `10.42.0.253`.

- `valve_controller.py` must me started on system boot (from `/etc/rc.local`); it provides the interface to the valves

- `airflow_sensor` can be run from the command line, it prints sensor reading to the console; it expects the Honeywell Zephyr sensor to be connected to the I2C bus 2, on address 73



