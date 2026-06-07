import os
from supabase import create_client
from dotenv import load_dotenv
from google import genai

load_dotenv()

supabase = create_client(
    os.getenv("url"), 
    os.getenv("apikey"))

gemclient = genai.Client(api_key=os.getenv("geminikey"))    