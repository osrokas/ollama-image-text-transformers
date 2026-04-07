from gtts import gTTS
import os
from gtts import gTTS
from pydub import AudioSegment
import subprocess

def tts_fixed_duration(input_path, target_duration_ms=5000, output_path="output_fixed_duration.mp3"):
    
    # Load and measure
    audio = AudioSegment.from_mp3(input_path)
    current_duration = len(audio)  # in ms
    
    # Calculate speed ratio
    speed = current_duration / target_duration_ms
    
    # Apply speed change via ffmpeg (preserves pitch)
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-filter:a", f"atempo={speed}",
        "temp_output.mp3"
    ])

def text_to_speech(text_path: str, output_path: str = "output") -> None:
    with open(text_path, 'r', encoding='utf-8') as text_file:
        text_content = text_file.read()
        gTTS(text=text_content, lang='en').save(output_path)
