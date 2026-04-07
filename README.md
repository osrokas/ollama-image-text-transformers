# ollama-image-text-transformers

Small Python project for turning an image into a short description, converting that text into subtitles, and generating speech audio.

## What It Does

The current codebase is centered around `run.py`, which coordinates four steps:

- Describe an image with an Ollama vision-capable model
- Save the description to a text file
- Convert the text into `.srt` subtitles
- Generate an MP3 narration from the text

There is also a separate utility module for converting `.srt` files back into plain text.

## Current Project Structure

```text
py-ollama/
|- assets/
|  `- example/
|     |- explanation.txt
|     |- output.mp3
|     |- subtitles.srt
|     `- tower.png
|- run.py
|- requirements.txt
|- README.md
`- src/
	|- __init__.py
    |- image_to_text.py
	|- srt_to_text.py
	|- text_to_speech.py
	`- text_to_srt.py
```

## Modules

- `src/image_to_text.py`: sends a base64-encoded image to `ollama.chat()` and returns a one-sentence description
- `src/text_to_srt.py`: splits text into subtitle blocks and formats them as `.srt`
- `src/text_to_speech.py`: uses `gTTS` to create speech audio and `pydub` plus `ffmpeg` to adjust duration
- `src/srt_to_text.py`: parses `.srt`, rebuilds plain text, and can optionally split subtitle groups by timing gaps
- `run.py`: pipeline entry point that ties the image, text, subtitles, and speech steps together

## Requirements

- Python 3.10+
- Access to an Ollama model that supports image input
- `ffmpeg` available on your system path
- Optional: an Ollama API key for hosted access

## Installation

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gTTS pydub
```

Notes:

- `requirements.txt` currently lists `ollama`, `python-dotenv`, `edge-tts`, and `pyttsx3`
- The active code imports `gTTS` and `pydub`, but they are not listed in `requirements.txt` yet
- `python-dotenv`, `edge-tts`, and `pyttsx3` are currently not used by the main pipeline

## Environment Variables

An example environment file is included:

```env
OLLAMA_API_KEY=<your_api_key_here>
```

At the moment, the repository does not automatically load `.env`. The API key is only referenced in commented example code inside `src/image_to_text.py`. If you use hosted Ollama access, you will need to wire environment loading into the code or export the variable in your shell.

## Running The Pipeline

Run the main pipeline with either of these commands:

```bash
python run.py
```

or:

```bash
python -m run
```

### Default Behavior

`run.py` currently calls:

- image input: `assets/tower.png`
- text output: `assets/explanation.txt`
- subtitle output: `assets/subtitles.srt`
- speech output: `assets/output.mp3`
- model: `gemma4:31b-cloud`

Important: the repository currently ships the sample image in `assets/example/tower.png`, not `assets/tower.png`. Before running the default script, either:

1. Copy `assets/example/tower.png` to `assets/tower.png`, or
2. Edit the paths passed to `main()` in `run.py`

If the run succeeds, the pipeline will create text, subtitle, and audio files in the `assets/` directory.

## Example Assets

The repository includes an example output set in `assets/example/`:

- `tower.png`: sample image
- `explanation.txt`: generated one-sentence description
- `subtitles.srt`: subtitle output built from that description
- `output.mp3`: generated narration audio

These files are useful as a reference for the expected output format.

## How The Main Pipeline Works

`run.py` performs these steps:

1. Calls `explain_image()` to describe the input image
2. Writes the returned text to a plain text file
3. Calls `text_to_srt()` to build subtitle blocks
4. Writes the subtitle text to an `.srt` file
5. Uses `text_to_speech()` to create an MP3 from the text file
6. Reads the final subtitle timestamp and calls `tts_fixed_duration()` to match audio duration to the subtitle length

## Converting SRT Back To Text

The `src/srt_to_text.py` module provides utilities for restoring text from subtitle files.

Available functions include:

- `text_from_srt(srt_text, gap_threshold_seconds=0.0)`
- `write_gap_segments(srt_text, output_dir, base_name='subtitles', gap_threshold_seconds=0.0)`
- `main(srt_path=None, gap_threshold_seconds=0.0, create_gap_files=False)`

This module is currently library-style code rather than a command-line interface.

## Current Limitations

- `run.py` is still hardcoded rather than configurable from the command line
- The default input image path does not match the bundled example asset location
- `.env` loading is not implemented
- Dependency declarations do not yet match the actual imports
- Error handling is minimal for missing files, model failures, and audio generation failures
- `tts_fixed_duration()` currently writes to `temp_output.mp3` and does not use its `output_path` parameter

## Next Improvements

- Add CLI arguments for input image, model, and output paths
- Update `requirements.txt` to match the imported packages
- Add `.env` loading or remove unused `python-dotenv`
- Add validation and error handling across the pipeline
- Make audio duration adjustment write to the requested output path
