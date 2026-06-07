from fastapi import FastAPI
from client import supabase
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from client import gemclient
import json


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("data.json", "r", encoding="utf-8") as f:
    profile = json.load(f)

@app.get("/ai")
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):

    prompt = f"""
You are Riyas.

Answer as Riyas in first person.

Never say you are an AI model.
Never mention Gemini or Google.

Use ONLY the information below.

PROFILE:
{json.dumps(profile, indent=2)}

QUESTION:
{request.message}

If the answer is not found in the profile, say:
"I haven't added that information to my portfolio yet."
"""

    response = gemclient.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "reply": response.text
    }


@app.get("/")
def give_name():
    return{"Health":"Good"}

class Message(BaseModel):
    text:str

@app.post("/send")    
def send_msg(message: Message):
    if message.text is None:
        return{"Enter a message by extending url with quetion mark, for eg(?text=Hi)"}
    else: 
        payload = {
            "text" : message.text 
        }
        data = supabase.table("jarvis").insert(payload).execute()
        return{"result":"success"}

class Clinum(BaseModel): 
    clireq:int = 1

@app.post("/fetch")
def get_msg(clireq: Clinum):
    data = supabase.table("jarvis").select("text").order("created_at", desc=True).limit(clireq.clireq).execute()
    return {
        "messages": data.data
    }
