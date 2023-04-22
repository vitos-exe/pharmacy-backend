from flask import Flask, request
from .views import blueprints
from .db import init_db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app)

    init_db()

    for bp in blueprints:
        app.register_blueprint(bp)
        
    return app