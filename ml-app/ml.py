from ultralytics import YOLO
from taipy import Gui



model = YOLO("yolov8n.pt")
content = ''
impath = 'plholder.svg'
savedir = "/home/"

from taipy import Gui

def on_change(state, var1, var2):
	if var1 == 'content':
		state.impath = var2
		results = model.predict(var2, save=True, save_dir=savedir)
		state.impath = savedir + path.removeprefix("/tmp/")


page='''

# Object Detector

<|{content}|file_selector|label=Select File|>
<|{impath}|image|>

'''

Gui(page).run(use_reloader=True, host='localhost')
