# Jinja2 templating with Docker

## Build & Coverage
[![Build Status](https://travis-ci.org/dinuta/jinja2docker.svg?branch=master)](https://travis-ci.org/dinuta/jinja2docker)
[![Coverage Status](https://coveralls.io/repos/github/dinuta/jinja2docker/badge.svg?branch=master)](https://coveralls.io/github/dinuta/jinja2docker?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a9754bb39c4145c3818920509bc70a3e)](https://www.codacy.com/manual/dinuta/jinja2docker?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dinuta/jinja2docker&amp;utm_campaign=Badge_Grade)
## Docker Hub
[Docker Hub Image](https://hub.docker.com/r/dinutac/jinja2docker)

![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/dinutac/jinja2docker/2.1.6) ![MicroBadger Layers (tag)](https://img.shields.io/microbadger/layers/dinutac/jinja2docker/2.1.6) ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/dinutac/jinja2docker/2.1.6) ![](https://img.shields.io/docker/pulls/dinutac/jinja2docker.svg)

Steps:   
*   Mount the directory containing your template(s) to the container's **/templates** directory
*   Mount the directory containing your variables file(s) directory **/variables**
*   Pass needed env vars (any number)
*   In your jinja2 template get OS environment variables plus your inserted environment vars with ```environ('your_env_var')```

## Supported formats (default)
Check [jinja2-cli](https://github.com/mattrobenolt/jinja2-cli) commands for all supported formats.  

## Docker image in action on katacoda  
[Katacoda scenario](https://katacoda.com/dinuta/scenarios/jinja2docker)

## Syntax

```bash
docker run --rm \
-v **TEMPLATE_FOLDER**:/templates \ 
-v **VARIABLES_FOLDER**:/variables  \
-e CUSTOM_ENV_VAR=**VALUE** \
dinutac/jinja2docker:latest /templates/json.j2 /variables/json.json --format=json > **OUTPUT_FILE**
```

Example 1: 
```bash
docker run --rm 
-v $PWD/inputs/templates:/templates 
-v $PWD/inputs/variables:/variables \
-e DATABASE=mysql56 -e IMAGE=latest \
dinutac/jinja2docker:latest /templates/standalone.j2 /variables/variables.yml --format=yaml > docker-compose.yml
```

Example 2:
```bash
docker run --rm 
-v $PWD/inputs/templates:/templates 
-v $PWD/inputs/variables:/variables
dinutac/jinja2docker:latest /templates/json.j2 /variables/json.json --format=json
```

## Templating example
**template.json**
``` txt
Os: {{os}}
Flavour: {{flavour}}
   
Path: {{environ('PATH')}}
```

**variables.json**
```json
{
  "os" : "Linux",
  "flavour": "CentOS"
}
```

## Templating result  
**result.json**
```json
Os: Linux
Flavour: CentOS

Path: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

## Embedded custom render

If you want to use the custom embedded render you must override the entrypoint with ```/scripts/entities/render.py```. It supports:
*   yaml
*   json

Example:
```bash
docker run --rm --entrypoint /scripts/entities/render.py
-e DATABASE=mysql56 -e IMAGE=latest 
dinutac/jinja2docker:latest json.j2 /variables/json.json
```
*The call is similar to jinja2-cli default render, but the template is called by name, not by path. The template must exist in /templates dir.*

## Write your own custom render
If you want to write your own custom jinja2 render:

*   Override the ```render.py``` file (you must use this file name) in **/scripts/entities/render.py** in order to execute your own logic.
*   Verify the Dockerfile and add the needed python packages (requirements.txt).    
  
