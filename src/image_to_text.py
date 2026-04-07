from ollama import chat
import base64
from pathlib import Path


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



def explain_image(image_path: str, content: str = None, model: str="gemma4:31b-cloud",) -> str:
    # Read and encode the image as base64
    image_data = base64.b64encode(Path(image_path).read_bytes()).decode()

    if not content:
        content = "Describe the image in 1 sentence."

    response = chat(
        model=model,
        messages=[
            {
                'role': 'user',
                'content': content,
                'images': [image_data],  # Pass base64-encoded image(s)
            }
        ],
    )
    return response.message.content

