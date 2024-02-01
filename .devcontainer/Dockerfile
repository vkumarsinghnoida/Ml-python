FROM ubuntu:22.04

COPY requirements.txt .
RUN apt update 
RUN apt install sudo -y && sudo apt install openssh-server python3 python3-pip git wget nano -y && sudo service ssh start 
RUN pip install -r requirements.txt 
