# Third-party imports.
from srp import Verifier
from flask import Flask, request, jsonify

# Local imports.
from src.objects import User
from src.data_manager import DataManager

class SRPModule:
    def __init__(self, flask_app: Flask, data_manager: DataManager):
        print(self.__class__.__name__, "loaded.")
        self.flask_app = flask_app
        self.data_manager = data_manager
        
        self._processing_verifiers : dict[str, Verifier] = {}
    
        self._set_url_rules()
    
    def _set_url_rules(self):
        self.flask_app.add_url_rule("/srp/register", view_func = self._register, methods = ["POST"])
        self.flask_app.add_url_rule("/srp/start", view_func = self._start, methods = ["POST"])
        self.flask_app.add_url_rule("/srp/end", view_func = self._end, methods = ["POST"])
    
    def _register(self):
        data : dict = request.get_json()
        username : str = data.get("username")
        srp_salt : str = data.get("srp_salt")
        srp_verifier : str = data.get("srp_verifier")
        
        if not username:
            return jsonify({"Error": "(username) not specified."}), 404
        
        if not srp_salt:
            return jsonify({"Error": "(srp_salt) not specified."}), 404
        
        if not srp_verifier:
            return jsonify({"Error": "(srp_verifier) not specified."}), 404
        
        if self.data_manager.get_user(username):
            return jsonify({"Error": "(username) already exist."}), 404
        
        self.data_manager.add_user(username, bytes.fromhex(srp_verifier), bytes.fromhex(srp_salt))
                
        return jsonify({"Success": "Registered successfully."}), 200
    
    def _start(self):
        data : dict = request.get_json()
        a = data.get("A")
        username = data.get("username")
        
        if not a:
            return jsonify({"Error": "(A) not specified."}), 404
    
        if not username:
            return jsonify({"Error": "(username) not specified."}), 404
        
        A = bytes.fromhex(a)
        user = self.data_manager.get_user(username)
        
        if not user:
            return jsonify({"Error": "(username) doesn't exist."}), 404
        
        svr = Verifier(user.username, user.srp_salt, user.srp_verifier, A)
        self._processing_verifiers[user.username] = svr
        salt, B = svr.get_challenge()
        
        return jsonify({
            "salt": salt.hex(),
            "B": B.hex()
        })
    
    def _end(self):
        data : dict = request.json()
        m : str = data.get("M")
        username : str = data.get("username")
        
        if not m:
            return jsonify({"Error": "(M) not specified."}), 404
        
        if not username:
            return jsonify({"Error", "(username) not specified."}), 404
        
        M = bytes.fromhex(m)
        verifier = self._processing_verifiers.pop(username)
        HAMK = verifier.verify_session(M)
        
        if not HAMK:
            return jsonify({"Error": "Invalid password"}), 404
        
        user = self.data_manager.get_user(username)
        return jsonify({
            "HAMK": HAMK.hex(),
            "id": user.id.hex,
            "username": user.username
        })