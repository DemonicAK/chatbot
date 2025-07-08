# Ollama Integration Guide

This guide explains how to integrate and use Llama 3.1 8B with the TalentScout Chatbot using Ollama.

## Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
./setup_ollama.sh
```

### Option 2: Manual Setup

1. **Install Ollama**:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Start Ollama server**:
   ```bash
   ollama serve
   ```

3. **Pull Llama 3.1 8B model**:
   ```bash
   ollama pull llama3.1:8b
   ```

4. **Test the model**:
   ```bash
   ollama run llama3.1:8b
   ```

## Usage

1. **Start the chatbot**:
   ```bash
   streamlit run main.py
   ```

2. **Select AI Provider**:
   - In the sidebar, select "Llama 3.1 8B (Ollama)" from the AI provider dropdown
   - The status indicator will show ✅ if Ollama is running correctly

3. **Chat with your local AI**:
   - All responses will be generated using your local Llama 3.1 8B model
   - No internet connection required for AI responses
   - Your data stays completely private

## Features

### AI Provider Comparison

| Feature | OpenAI GPT-3.5-turbo | Llama 3.1 8B (Ollama) |
|---------|----------------------|------------------------|
| **Speed** | Fast (cloud) | Medium (local) |
| **Privacy** | Data sent to OpenAI | Complete privacy |
| **Cost** | Pay per API call | Free after setup |
| **Internet** | Required | Not required |
| **Quality** | Very High | High |
| **Customization** | Limited | Highly customizable |

### Benefits of Ollama Integration

1. **Privacy**: All data processing happens locally
2. **Cost**: No API costs after initial setup
3. **Reliability**: No internet dependency
4. **Customization**: Can fine-tune models
5. **Control**: Full control over the AI model

## Troubleshooting

### Common Issues

1. **"Ollama not available" error**:
   ```bash
   # Check if Ollama is running
   ps aux | grep ollama
   
   # Start Ollama if not running
   ollama serve
   ```

2. **"Model not found" error**:
   ```bash
   # Check available models
   ollama list
   
   # Pull the model if missing
   ollama pull llama3.1:8b
   ```

3. **Slow responses**:
   - Ensure your system has sufficient RAM (8GB+ recommended)
   - Consider using a smaller model like `llama3.1:7b` for faster responses

4. **Port conflicts**:
   ```bash
   # Check if port 11434 is in use
   netstat -an | grep 11434
   
   # Kill process using the port
   sudo kill -9 $(lsof -t -i:11434)
   ```

### Performance Tips

1. **System Requirements**:
   - RAM: 8GB minimum, 16GB recommended
   - Storage: 5GB free space for the model
   - CPU: Modern multi-core processor

2. **Optimization**:
   - Close unnecessary applications
   - Use SSD storage for better performance
   - Consider GPU acceleration if available

## Model Information

### Llama 3.1 8B Specifications
- **Parameters**: 8 billion
- **Context Length**: 128k tokens
- **Languages**: Multilingual support
- **Training**: Instruction-tuned for chat
- **Size**: ~4.7GB download

### Alternative Models
You can also use other Ollama models:

```bash
# Smaller, faster model
ollama pull llama3.1:7b

# Larger, more capable model (requires more RAM)
ollama pull llama3.1:70b
```

Update the model in `config.py`:
```python
AI_PROVIDERS = {
    "ollama": {
        "name": "Llama 3.1 7B (Ollama)",
        "model": "llama3.1:7b",  # Change model here
        "enabled": True
    }
}
```

## Security Considerations

1. **Local Processing**: All AI processing happens locally
2. **No Data Transmission**: Candidate data never leaves your system
3. **Access Control**: Only accessible from your local machine
4. **Audit Trail**: Full control over logs and data

## Next Steps

1. **Custom Fine-tuning**: Train the model on your specific interview data
2. **Multiple Models**: Use different models for different question types
3. **GPU Acceleration**: Set up CUDA for faster inference
4. **Containerization**: Deploy with Docker for easier management

## Support

For issues related to:
- **Ollama**: Check [Ollama GitHub](https://github.com/ollama/ollama)
- **Llama 3.1**: Check [Meta's documentation](https://ai.meta.com/llama/)
- **Chatbot**: Check the main README.md

## License

This integration follows the same MIT license as the main project. Llama 3.1 has its own license terms from Meta.
