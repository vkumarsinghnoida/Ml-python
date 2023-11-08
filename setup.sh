sudo apt update
sudo apt install lxde-core
sudo apt install tightvncserver
vncserver
vncserver -kill :1
cp /workspaces/ML-python/startup.txt ~/.vnc/xstartup
chmod +x ~/.vnc/xstartup
vncserver
