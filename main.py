from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from google import genai
import time
import requests
import os
import io
from dotenv import load_dotenv
load_dotenv()


import time
from google import genai
from google.genai import types

client = genai.Client()

prompt = """A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"""

operation = client.models.generate_videos(
    model="veo-3.0-generate-preview",
    prompt=prompt,
)

# Poll the operation status until the video is ready.
while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(10)
    operation = client.operations.get(operation)

# Download the generated video.
generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)
generated_video.video.save("dialogue_example.mp4")
print("Generated video saved to dialogue_example.mp4")

# class VideoPrompt(BaseModel):
#     prompt: str

# app = FastAPI()
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# @app.post("/generate_video")
# async def generate_video(payload: VideoPrompt):
#     try:
#         # Start video generation
#         operation = client.models.generate_videos(
#             model="veo-3.0-generate-preview",
#             prompt=payload.prompt,
#         )

#         # Poll until complete
#         while not operation.done:
#             time.sleep(5)
#             operation = client.operations.get(operation)

#         video_response = operation.result

#         # ✅ Access the download URI
#         if not hasattr(video_response, "generated_videos"):
#             raise HTTPException(status_code=500, detail=f"Unexpected response: {video_response}")

#         # ✅ Get secure download URI
#         video_uri = video_response.generated_videos[0].video.uri
#         print(f"Video URI: {video_uri}")

#         # ✅ Download with API key
#         headers = {
#             "Authorization": f"Bearer {os.getenv('GEMINI_API_KEY')}",
#             "Accept": "application/octet-stream"
#         }
#         resp = requests.get(video_uri, headers=headers, stream=True)
#         print(f"resp: {resp}")
        
#         if resp.status_code != 200:
#             raise HTTPException(status_code=500, detail="Failed to download video from Gemini")

#         file_id = video_uri.split("/files/")[1].split(":")[0]  # extract the file id
#         video_file = client.files.download(name=f"files/{file_id}")

#         # Save or stream
#         return StreamingResponse(
#             io.BytesIO(video_file.data),
#             media_type="video/mp4",
#             headers={"Content-Disposition": "inline; filename=generated.mp4"}
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))