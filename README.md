# zwave2homekit
Expose Z-Wave accessories to HomeKit

For now it exposes all thermostats to HomeKit.
The setpoint can be controlled through HomeKit.
Changing the setpoint on the device itself is also propagated to HomeKit.

This was tested using Docker on Synology,
an Aeotec Gen5 Z-Wave stick,
and Danfoss LC-13 014G0013 thermostats.


## Requirements

The Z-Wave devices are interfaced using
[python-openzwave](https://github.com/OpenZWave/python-openzwave>).

HomeKit supported is provided through
[HAP-python](https://github.com/ikalchev/HAP-python>).

See the [Dockerfile](Dockerfile) for the required packages.
