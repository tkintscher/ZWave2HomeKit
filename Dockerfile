FROM python:3.6-jessie

MAINTAINER Thomas Kintscher


#
# build required packages
#

USER root

RUN apt-get update && apt-get install -y \
        build-essential \
        libudev-dev \
        make \
        g++ \
        libyaml-dev \
        libavahi-compat-libdnssd-dev

RUN pip install --trusted-host pypi.python.org \
        cython \
        wheel \
        six \
        PyDispatcher \
        python-openzwave \
        HAP-python


#
# add and configure script
#


ADD server.py /root/server.py

EXPOSE 5353 51826

ENV ZWAVE_DEVICE /dev/ttyACM0
ENV BRIDGE_NAME  Z-Wave Bridge
ENV MAC          AA:11:22:33:44:55
ENV PINCODE      123-45-678
ENV DS_HOSTNAME  diskstation

CMD ["python3", "/root/server.py"]
