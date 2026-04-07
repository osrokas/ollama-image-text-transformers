from ollama import chat
import base64
from pathlib import Path
from gtts import gTTS
# client = Client(
#     host='https://ollama.com',
#     headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
# )

# messages = [
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ]

# for part in client.chat('gpt-oss:120b', messages=messages, stream=True):
#   print(part.message.content, end='', flush=True)

def explain_image(image_path: str, model: str="gemma4:31b-cloud") -> str:
    # Read and encode the image as base64
    image_data = base64.b64encode(Path(image_path).read_bytes()).decode()

    response = chat(
        model=model,
        messages=[
            {
                'role': 'user',
                'content': 'Please explain what is shown in this image in one sentence.',
                'images': [image_data],  # Pass base64-encoded image(s)
            }
        ],
    )
    return response.message.content


# Usage
result = explain_image('assets/tower.png', model='gemma4:e2b')
print(result)



gTTS(text=result, lang='en').save("output.mp3")