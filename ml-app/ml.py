from ultralytics import YOLO
from taipy import Gui

model = YOLO("yolov8n.pt")
content = ''
impath1 = 'plholder.svg'
impath2 = 'plholder.svg'

def on_change(state, var1, var2):
	if var1 == 'content':
		state.impath1 = var2
		results = model.predict(var2, save=True)
		for r in results:
			print(r.save_dir)
			path = r.save_dir
		state.impath2 = '/home/' + path + '/' + var2.removeprefix('/tmp/')
		print(state.impath2)

page='''
<|text-center|
# OBJECT DETECTOR
<|{content}|file_selector|label=Select File|>

<|{impath1}|image|> <|{impath2}|image|>
>
'''

Gui(page).run(use_reloader=True, host='localhost')
