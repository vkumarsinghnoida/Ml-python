curl https://ollama.ai/install.sh | sh
ollama serve & sleep 3 && ollama pull nomic-embed-text
apt update && apt install tmux -y && pip install -r requirements.txt
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
~/miniconda3/bin/conda init bash

