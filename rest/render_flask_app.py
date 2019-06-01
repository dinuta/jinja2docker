import os

from flask import Flask, jsonify, request, Blueprint
from flask_restplus import Api

from entitities.render import Render

env_vars = {
    "TEMPLATES_DIR": os.environ.get('TEMPLATES_DIR'),
    "VARS_DIR": os.environ.get('VARS_DIR'),
    "TEMPLATE": os.environ.get('TEMPLATE'),
    "VARIABLES": os.environ.get('VARIABLES'),
    "TEMPLATES_DIR_FILES": os.listdir(os.environ.get('TEMPLATES_DIR')),
    "VARS_DIR_FILES": os.listdir(os.environ.get('VARS_DIR')),
    "PATH": os.environ.get('PATH')
}

app = Flask(__name__)
api = Api(app)


def init_app(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    flask_app.register_blueprint(blueprint)


# TODO define swagger specs

@app.route('/env')
def get_vars():
    return jsonify(env_vars), 200


@app.route('/rend/<template>/<variables>', methods=['GET'])
def get_content(template, variables):
    os.environ['TEMPLATE'] = template
    os.environ['VARIABLES'] = variables
    r = Render(os.environ['TEMPLATE'], os.environ['VARIABLES'])
    try:
        result = r.rend_template("dummy")
    except Exception as e:
        result = "Exception({0})".format(e.__str__())

    return result, 200


@app.route('/rendwithenv/<template>/<variables>', methods=['POST'])
def get_content_with_env(template, variables):
    input_json = request.get_json(force=True)
    os.environ['TEMPLATE'] = template
    os.environ['VARIABLES'] = variables
    for key, value in input_json.items():
        if key not in env_vars:
            os.environ[key] = value

    r = Render(os.environ['TEMPLATE'], os.environ['VARIABLES'])
    try:
        result = r.rend_template("dummy")
    except Exception as e:
        result = "Exception({0})".format(e.__str__())

    return result, 200
