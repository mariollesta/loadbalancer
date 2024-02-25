"""
File name: server_db.py
Author: Mario Llesta
Created: 2024-02-18
Last Edited:

Summary:

"""

# --- Imports ---
import json


# --- Constants and variables ---
SERVER_DB = "./server/server_db.json"


# --- Functions ---
def load_serverdb(server_db):
    server_info = {}
    with open(server_db, encoding="utf-8") as f:
        server_info = json.load(f)
    return server_info


server_info = load_serverdb(SERVER_DB)