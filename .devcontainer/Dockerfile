FROM ubuntu

COPY requirements.txt .
RUN     apt update 
RUN     apt install sudo -y 
RUN     sudo apt install openssh-server python3 python3-pip git curl -y && service ssh start
RUN pip install -r requirements.txt
