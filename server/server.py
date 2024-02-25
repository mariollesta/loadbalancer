"""
File name: server.py
Author: Mario Llesta
Created: 2024-02-17
Last Edited: 2024-02-25

Summary:
This module will start up and listen for connections on on a specified port
(i.e 80 for HTTP)
"""

# --- Imports ---
import socket
import sys
from time import sleep


# --- Constants and variables ---
HOST = 'localhost'
if len(sys.argv) <= 1:
    PORT = 5001
else:
    PORT = int(sys.argv[1]) 


# --- Functions ---
def start_server():
    # Create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            # Timeout
            sock.settimeout(10)
        
            # Bind it to an specific address an port
            sock.bind((HOST, PORT))
            
            # Listen for incoming connections
            sock.listen(5) # number of clients waiting in queue for "accept"
            print(f"[S]: Server listening on port {PORT}...")
            
            while True:
                # Accept the connection
                client_conn, client_addr = sock.accept()

                # Handle the connection
                handle_connection(client_conn, client_addr)
        
        except Exception as e:
            print(f"[S]: Error handling connection: {e}")
        
        finally:
            sock.close()
    
    
def handle_connection(client_conn, client_addr):
    with client_conn:
        print(f"[S]: Connected by {client_addr}...")
        try:
            # Receive and handle data    
            data = client_conn.recv(1024).decode('utf-8')
            if not data:
                return
            print(f"[S]: Received data from {client_conn.getpeername()}...")
            
            response = f"[S]: Hello from Backend Server {HOST}:{PORT}"
            http_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response)}\r\n\r\n{response}"
            sleep(10)
                    
            client_conn.send(http_response.encode())               
        
        except Exception as e:
            print(f"Error handling connection: {e}")   
    
    
    
if __name__ == "__main__":
    start_server()