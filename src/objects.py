# Python imports.
import uuid
from datetime import datetime

class User:
    def __init__(
            self,
            id: uuid.UUID,
            created_at: datetime,
            username: str, 
            srp_verifier: object, 
            srp_salt: object, 
    ):
        self.id = id
        self.created_at = created_at
        self.username = username
        self.srp_verifier = srp_verifier
        self.srp_salt = srp_salt