import os
from flask import Flask
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
app = Flask(__name__)


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")


    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)

    from .mainpage import mainpage
    from .reg import reg
    from .login import login
    from .projects import projects
    from .profile import profile_bp

    app.register_blueprint(mainpage, url_prefix='/')
    app.register_blueprint(reg, url_prefix='/')
    app.register_blueprint(login, url_prefix='/')
    app.register_blueprint(projects, url_prefix='/')
    app.register_blueprint(profile_bp, url_prefix='/')

    return app