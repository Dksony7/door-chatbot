# app/__init__.py
from flask import Flask
from .database import init_db

# Flask app initialization
app = Flask(__name__)

# Database initialization
init_db(app)
