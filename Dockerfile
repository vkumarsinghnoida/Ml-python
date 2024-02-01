FROM ubuntu

RUN apt update && apt install git wget python3-venv npm tar python3 -y
RUN wget https://github.com/neovim/neovim/releases/download/nightly/nvim-linux64.tar.gz && apt install tar && tar xzvf nvim-linux64.tar.gz 
