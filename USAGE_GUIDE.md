# Novel TTS Reader - Usage Guide 🎭📚

A sophisticated text-to-speech system that reads novels naturally with different voices for narration and character dialogue.

## 🌟 Features

✅ **Intelligent Dialogue Detection** - Automatically identifies dialogue vs narration  
✅ **Character Voice Assignment** - Different voices for different character types  
✅ **Character Type Classification** - Recognizes male, female, dragon, orc, and other character types  
✅ **Natural Reading Flow** - Smooth transitions between narration and dialogue  
✅ **Customizable Voice Settings** - Configure speech rate, volume, and voice preferences  
✅ **Text Analysis** - Analyze text structure before reading  
✅ **Beautiful CLI Interface** - Rich terminal output with progress tracking  

## 🚀 Quick Start

### Installation

```bash
# Clone or download the project
cd novel-tts-reader

# Create virtual environment
python3 -m venv novel_tts_env
source novel_tts_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

#### Run Demo
```bash
python novel_tts.py --demo
```

#### Analyze Sample Text
```bash
python novel_tts.py --demo --analyze
```

#### Read a Text File
```bash
python novel_tts.py --file your_novel.txt
```

#### Read Direct Text
```bash
python novel_tts.py --text "Hello, this is a test"
```

#### Analyze Text Structure
```bash
python novel_tts.py --file your_novel.txt --analyze
```

## 📖 Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--file` | `-f` | Novel text file to read |
| `--text` | `-t` | Direct text to read |
| `--output` | `-o` | Output audio file (planned feature) |
| `--analyze` | `-a` | Analyze text without reading |
| `--demo` | | Run demo with sample text |
| `--config` | `-c` | Custom configuration file path |
| `--help` | | Show help message |

## 🎭 Character Voice Types

The system automatically detects and assigns voices to different character types:

### **Narrator** 📚
- **Voice**: Neutral, clear
- **Rate**: 180 WPM
- **Usage**: All narration text

### **Male Characters** 👨
- **Voice**: Male preference
- **Rate**: 170 WPM  
- **Detection**: Pronouns (he, him), titles (lord, king, prince)

### **Female Characters** 👩
- **Voice**: Female preference
- **Rate**: 160 WPM
- **Detection**: Pronouns (she, her), titles (lady, queen, princess)

### **Dragon Characters** 🐲
- **Voice**: Deep, slow
- **Rate**: 120 WPM
- **Detection**: Keywords (dragon, wyrm, drake, roar, flame)

### **Orc Characters** 👹
- **Voice**: Gruff, faster
- **Rate**: 140 WPM
- **Detection**: Keywords (orc, goblin, troll, grunt, growl)

## ⚙️ Configuration

### Default Configuration
The system uses a built-in configuration, but you can customize it with a `config.json` file:

```json
{
    "voice_settings": {
        "narrator": {
            "rate": 180,
            "volume": 0.9,
            "voice_preference": "neutral"
        },
        "male": {
            "rate": 170,
            "volume": 0.95,
            "voice_preference": "male"
        },
        "female": {
            "rate": 160,
            "volume": 0.95,
            "voice_preference": "female"
        },
        "dragon": {
            "rate": 120,
            "volume": 1.0,
            "voice_preference": "male"
        },
        "orc": {
            "rate": 140,
            "volume": 1.0,
            "voice_preference": "male"
        }
    },
    "character_classifications": {
        "dragon_keywords": ["dragon", "wyrm", "drake", "smaug", "draconic"],
        "orc_keywords": ["orc", "goblin", "troll", "ogre", "grunt"],
        "male_keywords": ["he", "him", "man", "lord", "king", "prince"],
        "female_keywords": ["she", "her", "woman", "lady", "queen", "princess"]
    }
}
```

### Custom Configuration
```bash
python novel_tts.py --config my_config.json --file novel.txt
```

## 📝 Supported Text Formats

### Dialogue Detection
The system recognizes dialogue in these formats:

- `"Hello," said John.`
- `"How are you?" she asked.`
- `'I am fine,' he replied.`
- `"What's happening?"` (standalone)

### Character Recognition
Characters are identified through:

- **Context clues** in surrounding text
- **Keywords** specific to character types
- **Pronouns** and gender indicators
- **Fantasy creature** descriptors

## 📊 Text Analysis Output

When using `--analyze`, you'll see:

```
        Text Analysis         
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Metric             ┃ Value ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Total Segments     │ 54    │
│ Narration Segments │ 26    │
│ Dialogue Segments  │ 28    │
└────────────────────┴───────┘

     Character Breakdown     
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Character Type ┃ Segments ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Narrator       │ 26       │
│ Male           │ 14       │
│ Dragon         │ 6        │
│ Female         │ 6        │
│ Orc            │ 2        │
└────────────────┴──────────┘
```

## 🎯 Usage Examples

### Example 1: Fantasy Novel
```bash
# Analyze the structure first
python novel_tts.py --file fantasy_novel.txt --analyze

# Then read it aloud
python novel_tts.py --file fantasy_novel.txt
```

### Example 2: Custom Text
```bash
python novel_tts.py --text "The wizard Gandalf spoke clearly. 'You shall not pass!' he declared. The dragon roared in response."
```

### Example 3: Quick Demo
```bash
# Just run the demo to see how it works
python novel_tts.py --demo
```

## 🔧 Troubleshooting

### Audio Issues
- **No Sound**: Check system audio settings and available TTS voices
- **Wrong Voice**: The system uses available system voices; install additional voices if needed
- **ALSA Errors**: Normal in headless environments; functionality isn't affected

### Text Processing Issues
- **Dialogue Not Detected**: Ensure dialogue uses quotes (`"` or `'`)
- **Wrong Character Assignment**: Check if character context contains recognizable keywords
- **Missing Characters**: Add custom keywords to `config.json`

### Dependencies
```bash
# If installation fails, try:
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

## 🚧 Planned Features

- [ ] **Audio File Output** - Save readings to WAV/MP3 files
- [ ] **Voice Cloning** - Custom character voices
- [ ] **Emotion Detection** - Adjust tone based on context
- [ ] **Multiple Languages** - Support for other languages
- [ ] **GUI Interface** - Desktop application
- [ ] **Batch Processing** - Process multiple files
- [ ] **Character Profiles** - Save character voice assignments

## 🤝 Contributing

Feel free to contribute by:
- Adding new character types
- Improving dialogue detection
- Enhancing voice classification
- Adding new output formats
- Reporting bugs and issues

## 📄 License

This project is open source and available under standard licensing terms.

---

**Enjoy your immersive novel reading experience!** 🎭📚✨