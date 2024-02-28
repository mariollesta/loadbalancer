"""
File name: roundrobin.py
Author: Mario Llesta
Created: 2024-02-27
Last Edited: 2024-02-28

Summary:

"""


# --- Round Robin Algorithm Class ---
class RoundRobin:
    def __init__(self, servers):
        self.servers = servers
        self.current_index = 0

    def get_next_server(self):
        if not self.servers:
            raise ValueError("[ERROR]: No available servers...")
        
        next_server = self.servers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.servers)
        
        return next_server
