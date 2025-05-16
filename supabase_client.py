from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("sburl")
key1 = os.getenv("spbkey")

supabase1: Client = create_client(url, key1)

key2 = os.getenv("sb_sr_key")

supabase2: Client = create_client(url, key2)
