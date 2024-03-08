curl https://ollama.ai/install.sh | sh
ollama serve & sleep 3 && ollama pull nomic-embed-text
apt update && apt install tmux -y && pip install -r requirements.txt

