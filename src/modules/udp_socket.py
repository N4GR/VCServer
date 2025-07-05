# Third-party imports.
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect

class UDPSocketModule:
    def __init__(self, flask_app: Flask):
        print(self.__class__.__name__, "loaded.")
        
        self.flask_app = flask_app
        self.socket : SocketIO = self.flask_app.socket
    
        self.connected_users : dict[str, str] = {}
        
        self._set_events()
    
    def _set_events(self):
        self.socket.on_event("connect", self._on_connect)
        self.socket.on_event("disconnect", self._on_disconnect)
        self.socket.on_event("send_audio", self._on_send_audio)
    
    def _on_connect(self):
        user_id = request.args.get("user_id")
        session_id = request.sid
        
        self.connected_users[user_id] = session_id
        
        print(f"{user_id} connected to socket with session id {session_id}")
    
    def _on_disconnect(self):
        user_id = None
        
        for user, sid in self.connected_users.items():
            if sid == request.sid:
                user_id = user
                
                break
        
        if user_id:
            del self.connected_users[user_id]
        
        print(f"{user_id} disconnected from socket.")
    
    def _on_send_audio(self, data):
        audio_data = data.get("audio_data")
        
        print("Received audio.")
        
        for user_id, session_id in self.connected_users.items():
            emit("receive_audio", {"audio_data": audio_data}, room = session_id)
        