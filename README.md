# ollama-image-text-transformers

Small Python demo for describing an image with an Ollama vision model and turning the response into speech.

The current script:

- Sends an image to an Ollama-compatible chat model
- Asks for a one-sentence description of the image
- Prints the response to the terminal
- Saves the response as an MP3 file

## What It Does

The main script, `ollama_run.py`, loads `assets/tower.png`, sends it to a model through the `ollama` Python client, and generates audio output in `output.mp3`.

At the moment, the script is configured as a simple runnable example rather than a reusable CLI.

## Project Structure

```text
py-ollama/
|- assets/
|  |- image1.png
|  `- tower.png
|- ollama_run.py
|- requirements.txt
`- .env.example
```

## Requirements

- Python 3.10+
- Access to an Ollama model that supports image input
- Optional: Ollama cloud API key if you plan to use hosted access

## Installation

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gTTS
```

`gTTS` is required by the current script but is not listed in `requirements.txt` yet.

## Environment Variables

An example environment file is included:

```env
OLLAMA_API_KEY=<your_api_key_here>
```

The script currently contains commented example code showing how an API key could be passed to the Ollama client. If you use hosted Ollama access, copy `.env.example` to `.env` and provide your key.

## Usage

Run the script directly:

```bash
python ollama_run.py
```

By default, it uses:

- Image: `assets/tower.png`
- Model: `gemma4:e2b`

If the call succeeds, you should see a one-line description printed in the terminal and a new `output.mp3` file created in the project root.

## How It Works

`explain_image()` does the following:

1. Reads the image from disk
2. Encodes it as base64
3. Sends the encoded image in a chat request through `ollama.chat()`
4. Returns the model response text
5. Passes that text to `gTTS` to generate speech

## Notes

- `edge-tts` and `pyttsx3` are listed in `requirements.txt`, but the current script uses `gTTS` for audio generation.
- The script is hardcoded for a single image and model selection.
- There is no error handling yet for missing files, failed model responses, or audio generation failures.

## Next Improvements

Possible follow-up changes:

- Add command-line arguments for image path and model name
- Load environment variables automatically with `python-dotenv`
- Add basic error handling and validation
- Move output filenames and prompt text into configuration
- Update `requirements.txt` so it matches the imports used by the script
