#!/bin/bash

# Ollama Setup Script for TalentScout Chatbot
# This script helps set up Ollama with Llama 3.1 8B model

echo "🚀 Setting up Ollama with Llama 3.1 8B for TalentScout Chatbot"
echo "================================================================="

# Check if Ollama is already installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed"
else
    echo "📦 Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
    
    if [ $? -eq 0 ]; then
        echo "✅ Ollama installed successfully"
    else
        echo "❌ Failed to install Ollama"
        exit 1
    fi
fi

# Start Ollama service
echo "🔄 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to start
echo "⏳ Waiting for Ollama to start..."
sleep 5

# Check if Ollama is running
if pgrep -f "ollama serve" > /dev/null; then
    echo "✅ Ollama service is running"
else
    echo "❌ Failed to start Ollama service"
    exit 1
fi

# Pull Llama 3.1 8B model
echo "📥 Pulling Llama 3.1 8B model (this may take a while)..."
ollama pull llama3.1:8b

if [ $? -eq 0 ]; then
    echo "✅ Llama 3.1 8B model downloaded successfully"
else
    echo "❌ Failed to download Llama 3.1 8B model"
    exit 1
fi

# Test the model
echo "🧪 Testing Llama 3.1 8B model..."
echo "Hello! This is a test." | ollama run llama3.1:8b

echo ""
echo "🎉 Setup complete!"
echo "================================================================="
echo "Your chatbot is now ready to use Llama 3.1 8B via Ollama!"
echo ""
echo "To use the chatbot:"
echo "1. Make sure Ollama is running: ollama serve"
echo "2. Run your Streamlit app: streamlit run main.py"
echo "3. Select 'Llama 3.1 8B (Ollama)' from the AI provider dropdown"
echo ""
echo "To stop Ollama: kill $OLLAMA_PID"
