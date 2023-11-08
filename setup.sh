sudo apt update
sudo apt install xfce4 xfce4-goodies
sudo apt install tightvncserver
vncserver
vncserver -kill :1
cp /workspaces/Ml-python/startup.txt ~/.vnc/xstartup
chmod +x ~/.vnc/xstartup
vncserver -depth 16 -geometry 800x640 :1
