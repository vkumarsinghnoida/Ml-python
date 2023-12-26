from ultralytics import YOLO
from taipy import Gui

app = Gui()
model = YOLO("yolov8n.pt")
