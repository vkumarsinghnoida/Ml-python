apt update
apt install sudo -y
sudo apt install xfce4 xfce4-goodies -y
sudo apt install tightvncserver -y
sudo apt install ranger -y
sudo apt install tmux -y
sudo apt install tilix -y 
sudo apt install neofetch -y
sudo apt install midori -y
vncserver
vncserver -kill :1
cp /workspaces/Ml-python/startup.txt ~/.vnc/xstartup
chmod +x ~/.vnc/xstartup
vncserver -depth 16 -geometry 800x600 :1
echo -e  "vncserver -depth 16 -geometry 1280x640 :1 \nzsh \nclear" >> ~/.bashrc
cp zshhistory ~/.zsh_history
