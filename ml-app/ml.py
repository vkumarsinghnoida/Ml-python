from ultralytics import YOLO
from taipy import Gui

app = Gui()
model = YOLO("yolov8n.pt")

from taipy import Gui

Gui(page="# Object Detector").run(use_reloader=True)
