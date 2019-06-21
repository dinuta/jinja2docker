import os

from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

from entities.render import Render

env_vars = {
    "TEMPLATES_DIR": os.environ.get('TEMPLATES_DIR'),
    "VARS_DIR": os.environ.get('VARS_DIR'),
    "TEMPLATE": os.environ.get('TEMPLATE'),
    "VARIABLES": os.environ.get('VARIABLES'),
    "TEMPLATES_DIR_FILES": os.listdir(os.environ.get('TEMPLATES_DIR')),
    "VARS_DIR_FILES": os.listdir(os.environ.get('VARS_DIR')),
    "PATH": os.environ.get('PATH')
}

SWAGGER_URL = '/api/docs'
API_URL = '/swagger/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Jinja2Docker"
    },
)

app = Flask(__name__)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger/swagger.json')
def get_swagger():
    return app.send_static_file("swagger.json")


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
