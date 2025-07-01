#!/bin/bash

echo "🎭 Setting up Novel TTS Reader..."

# Update package lists
echo "📦 Updating package lists..."
sudo apt-get update

# Install system dependencies for audio
echo "🔊 Installing system audio dependencies..."
sudo apt-get install -y espeak espeak-data libespeak1 libespeak-dev ffmpeg portaudio19-dev python3-pyaudio alsa-utils

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Download spaCy model
echo "🧠 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Download NLTK data
echo "📚 Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt')"

# Make the script executable
chmod +x novel_tts.py

echo "✅ Setup complete!"
echo ""
echo "🚀 Usage examples:"
echo "  python novel_tts.py demo                    # Run demo"
echo "  python novel_tts.py read sample_novel.txt   # Read sample novel"
echo "  python novel_tts.py voices                  # List available voices"
echo "  python novel_tts.py speak 'Hello world'     # Speak text directly"
echo ""
echo "📖 To read your own novel, just place a .txt file in this directory and use:"
echo "  python novel_tts.py read your_novel.txt"