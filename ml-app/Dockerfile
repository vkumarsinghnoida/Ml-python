FROM ubuntu:23.10

RUN apt update \
    && apt install --no-install-recommends -y python3-pip libgl1 libglib2.0-0 libpython3-dev libusb-1.0-0

RUN rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED

RUN python3 -m pip install --upgrade pip wheel

WORKDIR /home/
COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache ultralytics 
RUN pip install --no-cache taipy

COPY ml.py plholder.svg yolov8n.pt .
CMD ["python3","ml.py"]
