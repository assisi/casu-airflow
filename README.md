# casu-airflow-controller

Controller code for the FESTO pneumatic valves. This code runs on the BeagleBone board which controls the pneumatic valves. It acts as a proxy to the valves for ohter CASUs.

## Deployment

The BeagleBone controlling the valves must have hostname `bbg-festo` and IP address `10.42.0.253`.

- `valve_controller.py` must me started on system boot; it provides the interface to the valves
- ??? - airflow sensor ...


