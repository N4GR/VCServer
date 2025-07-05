import json

# Third-party imports.
import psycopg
from psycopg.rows import namedtuple_row

# Local imports.
from src.objects import User

class DataManager:
    def __init__(self):
        credentials = self._get_credentials()
        
        self._connection = psycopg.connect(
            host = credentials["host"],
            port = credentials["port"],
            dbname = credentials["database"],
            user = credentials["username"],
            password = credentials["password"],
            autocommit = True
        )
        self._cursor = self._connection.cursor(row_factory = namedtuple_row)
    
    def _get_credentials(self) -> dict[str, str]:
        with open("private/db_credentials.json", "r") as file:
            json_data = json.load(file)
        
        return json_data

    def get_user(self, username: str) -> User:
        self._cursor.execute("SELECT * FROM users WHERE username ILIKE %s", (username,))
        fetch = self._cursor.fetchone()
        
        if not fetch:
            return None
        
        return User(
            id = fetch.id,
            created_at = fetch.created_at,
            username = fetch.username.decode("utf-8"),
            srp_salt = fetch.srp_salt,
            srp_verifier = fetch.srp_verifier
        )
    
    def add_user(self, username: str, srp_verifier: bytes, srp_salt: bytes) -> User:
        self._cursor.execute("""
            INSERT INTO users (
                username, srp_verifier, srp_salt
            ) VALUES (%s, %s, %s)
        """, (username, srp_verifier, srp_salt))
        
        return self.get_user(username)