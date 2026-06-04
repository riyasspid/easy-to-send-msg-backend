from fastapi import FastAPI
from client import supabase
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def give_name():
    return{"riyas"}

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