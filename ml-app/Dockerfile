FROM ubuntu:23.10

#RUN apt update && apt install python3-full -y && apt install pipx -y
#RUN pipx install ultralytics

RUN apt update \
    && apt install --no-install-recommends -y python3-pip git libgl1 libglib2.0-0 libpython3-dev libusb-1.0-0

RUN rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED

