# Third-party imports.
from flask import Flask
from flask_socketio import SocketIO

# Local imports.
from src.modules.udp_socket import UDPSocketModule

class FlaskApp(Flask):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.socket = SocketIO(self)
        
        self._load_modules()
    
    def start(self, host: str, port: int):
        self.run(host, port, debug = True)
    
    def _load_modules(self):
        self.udp_socket = UDPSocketModule(self)