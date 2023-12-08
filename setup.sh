sudo apt update
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
if command -v curl >/dev/null 2>&1; then   sh -c "$(curl -fsSL https://raw.githubusercontent.com/romkatv/zsh4humans/v5/install)"; else   sh -c "$(wget -O- https://raw.githubusercontent.com/romkatv/zsh4humans/v5/install)"; fi

echo -e  "vncserver -depth 16 -geometry 1280x640 :1 \nzsh \nclear" >> ~/.bashrc
cp zshhistory ~/.zsh_history
