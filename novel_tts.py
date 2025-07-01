#!/usr/bin/env python3
"""
Novel TTS Reader - A text-to-speech system that reads novels naturally
with different voices for narration and character dialogue.
"""

import re
import os
import json
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

import pyttsx3
import nltk
from nltk.tokenize import sent_tokenize
import click
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

console = Console()

@dataclass
class Voice:
    """Voice configuration for different character types"""
    name: str
    rate: int
    volume: float
    voice_preference: str

@dataclass
class TextSegment:
    """Represents a segment of text with its type and assigned voice"""
    text: str
    segment_type: str  # 'narration', 'dialogue'
    character_type: str  # 'narrator', 'male', 'female', 'dragon', 'orc', etc.
    voice: Voice

class NovelTTSReader:
    """Main class for the Novel TTS Reader system"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.engine = pyttsx3.init()
        self.voices = self.setup_voices()
        
        # Pattern for detecting dialogue
        self.dialogue_patterns = [
            r'"([^"]+)"',  # Text in double quotes
            r"'([^']+)'",  # Text in single quotes
            r'"([^"]+)"',  # Curly quotes
            r"'([^']+)'",  # Curly single quotes
        ]
        
        # Character type detection patterns
        self.character_patterns = {
            'dragon': [r'\b(?:dragon|wyrm|drake|draconic|scaled)\b', r'\broar(?:ed|ing)?\b', r'\bflame(?:s|d)?\b'],
            'orc': [r'\b(?:orc|orcish|goblin|troll|ogre)\b', r'\bgrunt(?:ed|ing)?\b', r'\bgrowl(?:ed|ing)?\b'],
            'female': [r'\b(?:she|her|woman|lady|girl|princess|queen|mother|sister|daughter)\b'],
            'male': [r'\b(?:he|him|man|lord|boy|prince|king|father|brother|son)\b'],
        }
    
    def load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            console.print(f"[yellow]Warning: Config file {self.config_path} not found. Using defaults.[/yellow]")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "voice_settings": {
                "narrator": {"rate": 180, "volume": 0.9, "voice_preference": "neutral"},
                "male": {"rate": 170, "volume": 0.95, "voice_preference": "male"},
                "female": {"rate": 160, "volume": 0.95, "voice_preference": "female"},
                "dragon": {"rate": 120, "volume": 1.0, "voice_preference": "male"},
                "orc": {"rate": 140, "volume": 1.0, "voice_preference": "male"}
            },
            "character_classifications": {
                "dragon_keywords": ["dragon", "wyrm", "drake", "smaug", "draconic"],
                "orc_keywords": ["orc", "goblin", "troll", "ogre", "grunt"],
                "male_keywords": ["he", "him", "man", "lord", "king", "prince"],
                "female_keywords": ["she", "her", "woman", "lady", "queen", "princess"]
            }
        }
    
    def setup_voices(self) -> Dict[str, Voice]:
        """Setup voice configurations"""
        voices = {}
        for voice_type, settings in self.config["voice_settings"].items():
            voices[voice_type] = Voice(
                name=voice_type,
                rate=settings["rate"],
                volume=settings["volume"],
                voice_preference=settings["voice_preference"]
            )
        return voices
    
    def detect_dialogue(self, text: str) -> List[Tuple[str, str]]:
        """Detect dialogue in text and return (text, type) tuples"""
        segments = []
        remaining_text = text
        
        # Find all dialogue matches
        dialogue_matches = []
        for pattern in self.dialogue_patterns:
            for match in re.finditer(pattern, text):
                dialogue_matches.append((match.start(), match.end(), match.group(1)))
        
        # Sort by position
        dialogue_matches.sort(key=lambda x: x[0])
        
        last_end = 0
        for start, end, dialogue in dialogue_matches:
            # Add narration before dialogue
            if start > last_end:
                narration = text[last_end:start].strip()
                if narration:
                    segments.append((narration, 'narration'))
            
            # Add dialogue
            segments.append((dialogue, 'dialogue'))
            last_end = end
        
        # Add remaining narration
        if last_end < len(text):
            remaining = text[last_end:].strip()
            if remaining:
                segments.append((remaining, 'narration'))
        
        # If no dialogue found, treat entire text as narration
        if not segments:
            segments.append((text, 'narration'))
        
        return segments
    
    def classify_character(self, text: str, segment_type: str) -> str:
        """Classify character type based on text content"""
        if segment_type == 'narration':
            return 'narrator'
        
        text_lower = text.lower()
        
        # Check for specific character types
        for char_type, patterns in self.character_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return char_type
        
        # Default to male for unclassified dialogue
        return 'male'
    
    def process_text(self, text: str) -> List[TextSegment]:
        """Process text into segments with voice assignments"""
        sentences = sent_tokenize(text)
        segments = []
        
        for sentence in sentences:
            dialogue_segments = self.detect_dialogue(sentence)
            
            for segment_text, segment_type in dialogue_segments:
                character_type = self.classify_character(segment_text, segment_type)
                voice = self.voices.get(character_type, self.voices['narrator'])
                
                segments.append(TextSegment(
                    text=segment_text,
                    segment_type=segment_type,
                    character_type=character_type,
                    voice=voice
                ))
        
        return segments
    
    def configure_voice(self, voice: Voice):
        """Configure TTS engine with voice settings"""
        self.engine.setProperty('rate', voice.rate)
        self.engine.setProperty('volume', voice.volume)
        
        # Try to set voice based on preference
        available_voices = self.engine.getProperty('voices')
        if available_voices:
            for av in available_voices:
                if voice.voice_preference.lower() in av.name.lower():
                    self.engine.setProperty('voice', av.id)
                    break
    
    def speak_text(self, text: str, voice: Voice):
        """Speak text with specified voice"""
        self.configure_voice(voice)
        self.engine.say(text)
        self.engine.runAndWait()
    
    def read_novel(self, text: str, output_file: Optional[str] = None):
        """Read novel text with appropriate voices"""
        segments = self.process_text(text)
        
        console.print(f"[green]Processing {len(segments)} text segments...[/green]")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Reading novel...", total=len(segments))
            
            for i, segment in enumerate(segments):
                # Display current segment info
                console.print(f"[blue]Segment {i+1}:[/blue] [{segment.character_type}] {segment.segment_type}")
                console.print(f"[dim]Text: {segment.text[:100]}{'...' if len(segment.text) > 100 else ''}[/dim]")
                
                if output_file:
                    # Save to audio file (would need additional implementation)
                    console.print(f"[yellow]Audio file output not implemented yet[/yellow]")
                else:
                    # Read aloud
                    self.speak_text(segment.text, segment.voice)
                
                progress.update(task, advance=1)
                time.sleep(0.5)  # Small pause between segments
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze text and return statistics"""
        segments = self.process_text(text)
        
        stats = {
            'total_segments': len(segments),
            'narration_segments': len([s for s in segments if s.segment_type == 'narration']),
            'dialogue_segments': len([s for s in segments if s.segment_type == 'dialogue']),
            'character_breakdown': {}
        }
        
        for segment in segments:
            char_type = segment.character_type
            if char_type not in stats['character_breakdown']:
                stats['character_breakdown'][char_type] = 0
            stats['character_breakdown'][char_type] += 1
        
        return stats

def display_stats(stats: Dict):
    """Display text analysis statistics"""
    table = Table(title="Text Analysis")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Total Segments", str(stats['total_segments']))
    table.add_row("Narration Segments", str(stats['narration_segments']))
    table.add_row("Dialogue Segments", str(stats['dialogue_segments']))
    
    console.print(table)
    
    # Character breakdown
    char_table = Table(title="Character Breakdown")
    char_table.add_column("Character Type", style="cyan")
    char_table.add_column("Segments", style="magenta")
    
    for char_type, count in stats['character_breakdown'].items():
        char_table.add_row(char_type.title(), str(count))
    
    console.print(char_table)

@click.command()
@click.option('--file', '-f', help='Novel text file to read')
@click.option('--text', '-t', help='Direct text to read')
@click.option('--output', '-o', help='Output audio file (not implemented yet)')
@click.option('--analyze', '-a', is_flag=True, help='Analyze text without reading')
@click.option('--demo', is_flag=True, help='Run demo with sample text')
@click.option('--config', '-c', default='config.json', help='Configuration file path')
def main(file, text, output, analyze, demo, config):
    """Novel TTS Reader - Read novels with character-appropriate voices"""
    
    console.print(Panel.fit(
        "[bold blue]Novel TTS Reader[/bold blue]\n"
        "[dim]Reading novels naturally with character voices[/dim]",
        border_style="blue"
    ))
    
    reader = NovelTTSReader(config)
    
    if demo:
        # Use sample text from file if it exists
        sample_file = Path("sample_novel.txt")
        if sample_file.exists():
            with open(sample_file, 'r', encoding='utf-8') as f:
                demo_text = f.read()
        else:
            demo_text = '''
            The ancient castle stood silently against the moonlit sky. 
            "Are you certain this is wise?" asked Princess Luna, her voice trembling.
            The old wizard stroked his beard. "Child, wisdom requires facing our fears," he said gently.
            From the shadows, a massive dragon emerged. "Fear not, young princess," the dragon rumbled like thunder.
            '''
        
        console.print("[green]Running demo with sample text...[/green]")
        
        if analyze:
            stats = reader.analyze_text(demo_text)
            display_stats(stats)
        else:
            reader.read_novel(demo_text, output)
    
    elif file:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                file_text = f.read()
            
            if analyze:
                stats = reader.analyze_text(file_text)
                display_stats(stats)
            else:
                reader.read_novel(file_text, output)
                
        except FileNotFoundError:
            console.print(f"[red]Error: File '{file}' not found.[/red]")
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
    
    elif text:
        if analyze:
            stats = reader.analyze_text(text)
            display_stats(stats)
        else:
            reader.read_novel(text, output)
    
    else:
        console.print("[yellow]Please provide text to read using --file, --text, or --demo[/yellow]")
        console.print("Use --help for more options")

if __name__ == "__main__":
    main()