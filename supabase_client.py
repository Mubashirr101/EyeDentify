from supabase import create_client, Client
import os
from dotenv import load_dotenv

def init_supabase_clients():
	load_dotenv(override=True)
	url = os.getenv("sburl")
	key1 = os.getenv("spbkey")
	key2 = os.getenv("sb_sr_key")
	supabase1 = create_client(url, key1)
	supabase2 = create_client(url, key2)
	return supabase1, supabase2

supabase1, supabase2 = init_supabase_clients()
