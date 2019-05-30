import os

from flask import Flask, jsonify

from render import Render

app = Flask(__name__)

env_vars = {
    "TEMPLATES_DIR": os.environ.get('TEMPLATES_DIR'),
    "VARS_DIR": os.environ.get('VARS_DIR'),
    "TEMPLATE": os.environ.get('TEMPLATE'),
    "VARIABLES": os.environ.get('VARIABLES'),
    "TEMPLATES_DIR_FILES": os.listdir(os.environ.get('TEMPLATES_DIR')),
    "VARS_DIR_FILES": os.listdir(os.environ.get('VARS_DIR'))
}


@app.route('/')
def get_vars():
    return jsonify(env_vars), 200


@app.route('/rend/<template>/<variables>', methods=['GET'])
def get_content(template, variables):
    os.environ['TEMPLATE'] = template
    os.environ['VARIABLES'] = variables
    r = Render(os.environ['TEMPLATE'], os.environ['VARIABLES'])
    result = r.rend_template("dummy")

    return result, 200


app.run(host='0.0.0.0')
