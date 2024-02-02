FROM ubuntu

COPY requirements.txt .
RUN apt update 
RUN apt install sudo -y 
RUN sudo apt install openssh-server python3 python3-pip git wget python3-venv npm tar nano curl -y && service ssh start
RUN pip install -r requirements.txt
RUN wget https://github.com/neovim/neovim/releases/download/nightly/nvim-linux64.tar.gz && apt install tar && tar xzvf nvim-linux64.tar.gz
RUN git clone https://github.com/LazyVim/starter ~/.config/nvim
