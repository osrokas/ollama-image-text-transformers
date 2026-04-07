from src.text_to_speech import text_to_speech, tts_fixed_duration 
from src.text_to_srt import text_to_srt
from src.image_to_text import explain_image

def main(input_image_path: str, output_text_path: str, output_srt_path: str, model: str = 'gemma4:31b-cloud', output_speech_path: str = "output.mp3") -> None:
    # Step 1: Explain the image
    explanation = explain_image(input_image_path, model=model)

    # Step 2: Save the explanation to a text file
    with open(output_text_path, 'w', encoding='utf-8') as output_file:
        output_file.write(explanation)

    # Step 3: Convert the explanation text to SRT format
    srt_data = text_to_srt(explanation, dursec=4)

    # Step 4: Save the SRT data to a file
    with open(output_srt_path, 'w', encoding='utf-8') as srt_file:
        srt_file.write(srt_data)

    # Get last timestamp from SRT data to determine total duration for TTS
    last_timestamp = srt_data.strip().splitlines()[-2].split(' --> ')[1].split(',')[0]  # Get end time of last subtitle
    h, m, s = map(float, last_timestamp.split(':'))
    total_duration_ms = int((h * 3600 + m * 60 + s) * 1000)
    text_to_speech(output_text_path, output_path=output_speech_path)
    tts_fixed_duration(output_speech_path, target_duration_ms=total_duration_ms, output_path=output_speech_path)


if __name__ == "__main__":
    import os
    main(
        input_image_path=os.path.join(os.path.dirname(__file__), "assets", "tower.png"),
        output_text_path=os.path.join(os.path.dirname(__file__), "assets", "explanation.txt"),
        output_srt_path=os.path.join(os.path.dirname(__file__), "assets", "subtitles.srt"),
        output_speech_path=os.path.join(os.path.dirname(__file__), "assets", "output.mp3"),
        model='gemma4:31b-cloud'
    )
    
