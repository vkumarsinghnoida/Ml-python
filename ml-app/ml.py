from ultralytics import YOLO
from taipy import Gui
import cv2
import numpy as np

app = Gui()
model = YOLO("yolov8n.pt")
content = ''

from taipy import Gui

def save(state, var1, var2):
        #cv2.imwrite('output.png', img)
        print(var1, var2)


page='''
# Object Detector
<|{content}|file_selector|label=Select File|on_action=save|>
'''

Gui(page).run(use_reloader=True, host='localhost')
