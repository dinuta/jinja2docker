#!/usr/bin/env python3

import os

from flask import Flask, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from entities.render import Render

unmodifiable_env_vars = {
    "TEMPLATES_DIR": os.environ.get('TEMPLATES_DIR'),
    "VARS_DIR": os.environ.get('VARS_DIR'),
    "PATH": os.environ.get('PATH')
}

app = Flask(__name__, instance_relative_config=False)
CORS(app)
app.register_blueprint(get_swaggerui_blueprint(
    base_url='/api/docs',
    api_url='/swagger/swagger.yml',
    config={
        'app_name': "jinja2docker"
    }), url_prefix='/api/docs')


@app.route('/swagger/swagger.yml')
def get_swagger():
    return swagger_file_content


@app.route('/env')
def get_vars():
    return dict(os.environ), 200


@app.route('/render/<template>/<variables>', methods=['POST'])
def get_content_with_env(template, variables):
    os.environ['TEMPLATE'] = template
    os.environ['VARIABLES'] = variables
    try:
        input_json = request.get_json(force=True)
        for key, value in input_json.items():
            if key not in unmodifiable_env_vars:
                os.environ[key] = value
    except:
        pass
    r = Render(os.environ['TEMPLATE'], os.environ['VARIABLES'])
    try:
        result = r.rend_template()
    except Exception as e:
        result = "Exception({})".format(e.__str__())

    return result, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

swagger_file_content = '''
"swagger": '2.0'
info:
  description: |
    This is Jinja2 with Docker.
  version: "1.0.1"
  title: Jinja2Docker
  termsOfService: http://swagger.io/terms/
  contact:
    email: apiteam@swagger.io
  license:
    name: Apache 2.0
    url: http://www.apache.org/licenses/LICENSE-2.0.html
# host: localhost:5000
basePath: /
tags:
  - name: Jinja2
    description: Rend templates with Jinja2 and Docker
    externalDocs:
      description: Find out more about our store
      url: http://swagger.io
schemes:
  - http
paths:
  /env:
    get:
      tags:
        - jinja2
      summary: Print env vars
      produces:
        - application/json
      responses:
        200:
          description: List of env vars in key value pairs
  /render/{template}/{variables}:
    post:
      tags:
        - jinja2
      summary: Jinja2 render with inserted env vars
      consumes:
        - application/json
        - application/x-www-form-urlencoded
      produces:
        - application/json
      parameters:
        - name: template
          in: path
          description: Template file mounted in docker
          required: true
          type: string
        - name: variables
          in: path
          description: Variables file mounted in docker
          required: true
          type: string
        - name: EnvVars
          in: body
          description: E.g. {"envvar1":"value1", "envvar2":"value2"}
          required: false
          schema:
            $ref: '#/components/schemas/EnvVar'
      responses:
        200:
          description: Jinja2 rendered template or the exception which occured.
components:
  schemas:
    EnvVar:
      type: object
      properties:
        your_env_var:
          type: string

externalDocs:
  description: Find out more about Swagger
  url: http://swagger.io
'''
