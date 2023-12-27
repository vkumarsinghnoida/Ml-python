from ultralytics import YOLO
from taipy import Gui
#import cv2
#import numpy as np

#app = Gui()
model = YOLO("yolov8n.pt")
content = ''
impath = 'plholder.svg'

from taipy import Gui

def on_change(state, var1, var2):
	if var1 == 'content':
		state.impath = var2
		result = model.predict(var2, save=True)
		state.impath = result.path
		print(var2)


page='''

# Object Detector

<|{content}|file_selector|label=Select File|>
<|{impath}|image|>

'''

Gui(page).run(use_reloader=True, host='localhost')
