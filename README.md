# ZWave2HomeKit
Expose Z-Wave accessories to HomeKit


## Features

 * Expose Z-Wave thermostats to HomeKit.
 * Change the setpoint via HomeKit


This program was tested using Docker on Synology,
an Aeotec Gen5 Z-Wave stick,
and Danfoss LC-13 014G0013 thermostats.


## Requirements

The Z-Wave devices are interfaced using
[python-openzwave](https://github.com/OpenZWave/python-openzwave>).

HomeKit supported is provided through
[HAP-python](https://github.com/ikalchev/HAP-python>).

See the [Dockerfile](Dockerfile) for the required packages.


## Environment Variables

 * `ZWAVE_DEVICE`: Device name of the Z-Wave device (default: `/dev/ttyACM0`).
 * `BRIDGE_NAME`:  Display name of the bridge in HomeKit (default: `Z-Wave Bridge`).
 * `MAC`:          MAC address for the bridge, can be any unique address not used on your network (default: `AA:11:22:33:44:55`).
 * `PINCODE`:      PIN for added the accessory in HomeKit (default: `123-45-678`).


## Running on Synology

The Docker image can be installed on Synology.
When adding the container, ensure that

 * running with "high privileged" is activated
   (necessary for accessing the Z-Wave device,
    as Synology's interface does not allow configuring passthrough of single devices),
 * some directory on the NAS is bound to `/config`,
 * and environment variables are set as desired (see above).
