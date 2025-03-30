
#!/bin/bash

#install required python packages
pip install langchain-community streamlit langchain faiss-cpu sentence-transformers nltk

#Download NLTK Tokenizer data
python -c "import nltk;nltk.download('punkt')"

#install npm dependencies
xargs npm install < npm_requirements.txt

# Run Python script to execute commands
python -c "from ollama_install_helper_module import run_commands; run_commands(['curl -fsSL https://ollama.com/install.sh | sh'])"

#Start the Ollama server in the background.
/usr/local/bin/ollama serve &

# Print a test message
echo "ollama test"

#Define the llm model.
MODEL="llama3.1:8b-instruct-q8_0"

# Run the LLM Model with Ollama using Python
python -c "from ollama_install_helper_module import run_commands; run_commands(['ollama run $MODEL'])"

#Retrieve a temporary password for the local tunnel server.
curl -s https://loca.lt/mytunnelpassword | awk '{print "\n\nPassword: "$0}'

# Start the Streamlit app and expose it via LocalTunnel
streamlit run app.py &> ./logs.txt & npx localtunnel --port 8501
