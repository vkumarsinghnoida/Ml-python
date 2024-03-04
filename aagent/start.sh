#!/usr/bin/sh

ollama serve & sleep 5 && streamlit run streamlit_chat.py
