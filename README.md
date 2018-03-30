# zwave2homekit
Expose Z-Wave accessories to HomeKit

For now it does nothing more than exposing all thermostats to HomeKit.

This was tested using Docker on Synology,
an Aeotec Gen5 Z-Wave stick,
and Danfoss LC-13 014G0013 thermostats.


## Requirements

The Z-Wave devices are interfaced using
`python-openzwave <https://github.com/OpenZWave/python-openzwave>`_.

HomeKit supported is provided through
`HAP-python <https://github.com/ikalchev/HAP-python>`_.

See the `Dockerfile` for the required packages.
