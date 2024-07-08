from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
import uvicorn

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

@app.post("/generate_response/")
async def generate_response(message: Message):
    url = "https://il-openai-poc1.openai.azure.com/openai/deployments/POC1/chat/completions?api-version=2024-02-15-preview&api-key=321caa2fd2e4493897e027a9a1469bc0"

    payload = {
        "messages": [
            {
                "role": message.role,
                "content": message.content
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": None
    }
    
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error from OpenAI")

    try:
        content = response.json()['choices'][0]['message']['content']
        return {"response": content}
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Invalid response from OpenAI")

# Add CORS middleware with allow_origins=["*"] to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

























# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import requests
# import json
# import uvicorn

# app = FastAPI()

# class Message(BaseModel):
#     role: str
#     content: str

# @app.post("/generate_response/")
# async def generate_response(message: Message):
#     url = "https://il-openai-poc1.openai.azure.com/openai/deployments/POC1/chat/completions?api-version=2024-02-15-preview&api-key=321caa2fd2e4493897e027a9a1469bc0"

#     payload = {
#         "messages": [
#             {
#                 "role": message.role,
#                 "content": message.content
#             }
#         ],
#         "temperature": 0.7,
#         "top_p": 0.95,
#         "frequency_penalty": 0,
#         "presence_penalty": 0,
#         "max_tokens": 800,
#         "stop": None
#     }
    
#     headers = {
#         'Content-Type': 'application/json'
#     }

#     response = requests.post(url, headers=headers, data=json.dumps(payload))
#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code, detail="Error from OpenAI")

#     try:
#         content = response.json()['choices'][0]['message']['content']
#         return {"response": content}
#     except (KeyError, IndexError):
#         raise HTTPException(status_code=500, detail="Invalid response from OpenAI")

# if __name__ == "__main__":
    
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload = True)


# import requests
# import json

# url = "https://il-openai-poc1.openai.azure.com/openai/deployments/POC1/chat/completions?api-version=2024-02-15-preview&api-key=321caa2fd2e4493897e027a9a1469bc0"

# payload = json.dumps({
#   "messages": [
#     {
#       "role": "system",
#       "content": "What is secret key of happiness?"
#     }
#   ],
#   "temperature": 0.7,
#   "top_p": 0.95,
#   "frequency_penalty": 0,
#   "presence_penalty": 0,
#   "max_tokens": 800,
#   "stop": None
# })
# headers = {
#   'Content-Type': 'application/json'
# }

# response = requests.request("POST", url, headers=headers, data=payload)

# # Extract content from the choices
# content = response.text['choices'][0]['message']['content']

# print(response.text)

