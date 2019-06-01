from flask import Flask

print("Start init")


def create_app():
    print("Start init flask!")
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('rest.flask_config.Config')
    with app.app_context():
        return app


print("End init")
