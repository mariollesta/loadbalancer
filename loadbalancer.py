"""
File name: loadbalancer.py
Author: Mario Llesta
Created: 2024-02-18
Last Edited: 2024-02-28

Summary:
This module will be the load balancer.
"""

# --- Imports ---
import json
import socket
import sys
from threading import Thread
from typing import List, Tuple
from backend.Beserver import Beserver
from server.server_db import server_info
from algorithm.roundrobin import RoundRobin


# --- Constants and variables ---
HOST: str = 'localhost'
if len(sys.argv) <= 1:
    PORT = 5432
else:
    PORT = int(sys.argv[1])

server_db = server_info["server_list"]
servers: List[Beserver] = []
for server in server_db:
    servers.append(Beserver(int(server["id"]), 
                            server["host"],
                            int(server["port"])))


# --- Functions ---
def main():
    lb_algorithm = None
    
    # LB Algorithm selection
    lb_algorithm = RoundRobin(servers)
    
    lb_threads: List[Thread] = []
    
    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:    
        # Bind it to an specific address an port
        sock.bind((HOST, PORT))
        
        # Listen for incoming connections
        sock.listen(100) # number of clients waiting in queue for "accept"
        print(f"[LB]: Listening on port {PORT}...")
        
        while True:
            # Accept the incoming connection (client connection)
            client_conn, client_addr = sock.accept()
            print(f"[LB]: Connected by {client_addr}...")
            
            # Select the backend server where data will be sent
            be: Beserver = lb_algorithm.get_next_server()
            if be:
                lb_thread = Thread(target=be.handle_beservers, args=(client_conn,))
                lb_threads.append(lb_thread)
                lb_thread.start()
        
    except Exception as e:
        print(f"Error handling connection: {e}")
        
    except KeyboardInterrupt:
        print("Ctrl-C pressed")
        
    finally:
        sock.close()   
        map(lambda th: th.join(), lb_threads) 


if __name__ == "__main__":
    main()