from flask import Flask
from .views import blueprints
from .db import create_db_cli_commands

def create_app():
    app = Flask(__name__)

    create_db_cli_commands(app)

    for bp in blueprints:
        app.register_blueprint(bp)
        
    return app

