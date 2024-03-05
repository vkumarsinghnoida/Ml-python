curl https://ollama.ai/install.sh | sh
ollama serve & sleep 3 && ollama pull nomic-embed-text
sudo apt update && sudo apt install tmux -y && pip install -r requirements.txt

