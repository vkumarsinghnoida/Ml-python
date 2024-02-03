FROM ubuntu

COPY requirements.txt .
RUN apt update 
RUN apt install sudo -y 
RUN sudo apt install openssh-server git wget tar nano curl -y && service ssh start

