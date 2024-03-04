# Use the official Ubuntu image as a parent image
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /home

# Update the package lists
RUN apt-get update

# Install Python 3.11.4
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.11

# Install tmux
RUN apt-get install -y tmux

# Install curl
RUN apt-get install -y curl

# Clone the GitHub repository
RUN git clone https://github.com/kamleshvkumarsingh/Ml-python.git

# Change directory to the cloned repository
WORKDIR /home/Ml-python

# Install Ollama and other dependencies
RUN curl https://ollama.ai/install.sh | sh
RUN pip install groq lamachain ollama chromadb

# Set the default command to run when the container starts
CMD ["bash"]
