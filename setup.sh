sudo apt update
sudo apt install xfce4 xfce4-goodies -y
sudo apt install tightvncserver -y
sudo apt install ranger -y
sudo apt install tmux -y
sudo apt install tilix -y 
sudp apt install neofetch -y
vncserver
vncserver -kill :1
cp /workspaces/Ml-python/startup.txt ~/.vnc/xstartup
chmod +x ~/.vnc/xstartup
vncserver -depth 16 -geometry 800x640 :1
