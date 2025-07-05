# Local imports.
from src.flask_app import FlaskApp

if __name__ == "__main__":
    flask_app = FlaskApp()
    flask_app.start("localhost", 8080)