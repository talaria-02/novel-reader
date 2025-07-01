# Novel TTS Reader 🎭📚

A sophisticated text-to-speech system that reads novels naturally with different voices for narration and character dialogue. The system automatically detects dialogue, identifies character types, and assigns appropriate voices for a more immersive reading experience.

## Features ✨

- **Intelligent Dialogue Detection**: Automatically identifies dialogue vs narration
- **Character Voice Assignment**: Different voices for different character types
- **Character Type Classification**: Recognizes male, female, dragon, orc, and other character types
- **Natural Reading Flow**: Smooth transitions between narration and dialogue
- **Customizable Voice Settings**: Configure speech rate, volume, and voice preferences
- **Multiple Output Options**: Read aloud or save to audio files
- **Beautiful CLI Interface**: Rich terminal interface with progress tracking

## Character Voices 🎪

- **Narrator**: Neutral voice for story narration
- **Male Characters**: Masculine voice for male characters
- **Female Characters**: Feminine voice for female characters  
- **Dragons**: Deep, slow voice for dragon characters
- **Orcs**: Gruff, harsh voice for orc/goblin characters

## Installation 🚀

1. **Quick Setup** (recommended):
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Manual Setup**:
   ```bash
   # Install system dependencies
   sudo apt-get update
   sudo apt-get install -y espeak espeak-data libespeak1 libespeak-dev ffmpeg

   # Install Python dependencies
   pip install -r requirements.txt
   
   # Download language models
   python -m spacy download en_core_web_sm
   python -c "import nltk; nltk.download('punkt')"
   ```

## Usage 📖

### Command Line Interface

```bash
# Run a demonstration
python novel_tts.py --demo

# Analyze text structure
python novel_tts.py --demo --analyze

# Read a novel file
python novel_tts.py --file your_novel.txt

# Read sample novel
python novel_tts.py --file sample_novel.txt

# Speak text directly
python novel_tts.py --text "Hello, this is a test of the TTS system!"

# Analyze a file
python novel_tts.py --file novel.txt --analyze

# Save to audio files (planned feature)
python novel_tts.py --file novel.txt --output my_audiobook
```

### Python API

```python
from novel_tts import NovelTTSReader

# Create TTS instance
reader = NovelTTSReader()

# Read text with character voices
text = '''
"Hello there!" said Princess Luna cheerfully.
The dragon Smaug growled in response, "Who dares disturb my slumber?"
'''

reader.read_novel(text)

# Analyze text structure
stats = reader.analyze_text(text)
print(f"Found {stats['dialogue_segments']} dialogue segments")
```

## How It Works 🔧

### 1. Text Parsing
The system uses advanced NLP to:
- Split text into sentences using NLTK
- Identify dialogue using regex patterns
- Extract speaker names from attribution

### 2. Character Classification
Characters are classified based on:
- **Name patterns** (e.g., names ending in 'a' for females)
- **Context keywords** (e.g., 'dragon', 'scales' for dragons)
- **Predefined name lists** for common character names

### 3. Voice Assignment
- Each character type gets a specific voice configuration
- Speech rate and volume are adjusted per character type
- System voices are intelligently mapped to character types

### 4. Natural Reading
- Smooth transitions between narration and dialogue
- Appropriate pauses between segments
- Progress tracking for long texts

## Configuration ⚙️

Edit `config.json` to customize:

```json
{
    "voice_settings": {
        "narrator": {
            "rate": 180,
            "volume": 0.9,
            "voice_preference": "neutral"
        },
        "dragon": {
            "rate": 120,
            "volume": 1.0,
            "voice_preference": "male"
        }
    },
    "character_classifications": {
        "dragon_keywords": ["dragon", "wyrm", "drake"],
        "female_names": ["luna", "aria", "elena"]
    }
}
```

## Supported Text Formats 📄

The system works best with:
- **Standard dialogue formatting**: `"Hello," said John.`
- **Attribution patterns**: `John said, "Hello."`
- **Character name consistency**: Using the same name for each character
- **Clear speaker attribution**: Identifying who is speaking

### Example Text Format
```
The wizard looked thoughtful. "We must be careful," Gandalf said solemnly.

"I agree," replied Princess Luna, her voice filled with concern.

From the shadows, a growling voice emerged. "Foolish mortals," snarled Grothak the orc.
```

## Troubleshooting 🔧

### No Audio Output
```bash
# Check audio system
pulseaudio --check -v

# Test system audio
speaker-test -t wav -c 2
```

### Missing Dependencies
```bash
# Reinstall audio dependencies
sudo apt-get install --reinstall espeak espeak-data

# Check Python packages
pip install --force-reinstall pyttsx3
```

### spaCy Model Issues
```bash
# Reinstall spaCy model
python -m spacy download en_core_web_sm --force
```

## Advanced Features 🎯

### Custom Character Voices
You can train the system to recognize custom character types by:
1. Adding keywords to `config.json`
2. Creating voice profiles for new character types
3. Using consistent character naming in your novels

### Batch Processing
Process multiple novels:
```bash
for file in *.txt; do
    python novel_tts.py read "$file" --output "${file%.txt}_audio"
done
```

### Voice Customization
- Adjust speech rate for different character types
- Modify volume levels for dramatic effect
- Map specific system voices to character types

## Contributing 🤝

Contributions welcome! Areas for improvement:
- Additional character type recognition
- Better dialogue parsing algorithms
- More voice customization options
- Support for different languages
- Advanced audio processing features

## License 📄

MIT License - feel free to use and modify for your projects!

---

**Enjoy your immersive novel reading experience!** 🎭📚🔊
