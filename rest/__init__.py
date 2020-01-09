from flask import Flask

from rest.flask_config import Config


def create_app():
    print("Start init flask!")
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)
    with app.app_context():
        return app
