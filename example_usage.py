#!/usr/bin/env python3
"""
Example usage script for Novel TTS Reader
Demonstrates different ways to use the system
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and display the description"""
    print(f"\n{'='*60}")
    print(f"🎭 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Demonstrate different usage patterns"""
    
    print("🎭📚 Novel TTS Reader - Example Usage Demonstrations")
    print("=" * 60)
    
    # Check if we're in the right environment
    if not Path("novel_tts.py").exists():
        print("❌ Error: novel_tts.py not found. Run this from the project directory.")
        sys.exit(1)
    
    # Example 1: Demo with analysis
    run_command(
        ["python", "novel_tts.py", "--demo", "--analyze"],
        "Demo: Analyze sample text structure"
    )
    
    input("\n📋 Press Enter to continue to the next example...")
    
    # Example 2: Demo with actual reading (a few segments)
    print("\n⚠️  The next example will attempt TTS reading.")
    print("   In headless environments, you'll see ALSA errors - this is normal.")
    choice = input("   Continue? (y/N): ").lower().strip()
    
    if choice == 'y':
        run_command(
            ["python", "novel_tts.py", "--demo"],
            "Demo: Read sample text with different voices"
        )
    
    # Example 3: Custom text analysis
    custom_text = '''
    "I must leave immediately," Princess Elena declared urgently.
    The ancient dragon Smaug raised his massive head. "Where do you think you're going, little one?" he rumbled.
    Sir Gareth stepped forward boldly. "She goes where she pleases, beast!"
    "Graarrgh!" roared the orc chieftain. "No one leaves alive!"
    The wizard Merlin stroked his beard thoughtfully, knowing that only wisdom could resolve this conflict.
    '''
    
    input("\n📋 Press Enter to analyze custom text...")
    
    run_command(
        ["python", "novel_tts.py", "--text", custom_text, "--analyze"],
        "Analyze custom text with multiple character types"
    )
    
    # Example 4: Reading from sample file if it exists
    if Path("sample_novel.txt").exists():
        input("\n📋 Press Enter to analyze the sample novel file...")
        
        run_command(
            ["python", "novel_tts.py", "--file", "sample_novel.txt", "--analyze"],
            "Analyze the complete sample novel file"
        )
    
    # Example 5: Show help
    input("\n📋 Press Enter to see help information...")
    
    run_command(
        ["python", "novel_tts.py", "--help"],
        "Display help information"
    )
    
    print("\n🎉 All examples completed!")
    print("\n📚 Next steps:")
    print("   • Try with your own text files: python novel_tts.py --file your_novel.txt")
    print("   • Customize voices with config.json")
    print("   • Read the USAGE_GUIDE.md for more details")
    print("\n   Happy reading! 🎭📚✨")

if __name__ == "__main__":
    main()