# Jinja2 templating with Docker

## Build & Coverage
[![Build Status](https://travis-ci.org/dinuta/jinja2docker.svg?branch=master)](https://travis-ci.org/dinuta/jinja2docker)
[![Coverage Status](https://coveralls.io/repos/github/dinuta/jinja2docker/badge.svg?branch=master)](https://coveralls.io/github/dinuta/jinja2docker?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a9754bb39c4145c3818920509bc70a3e)](https://www.codacy.com/manual/dinuta/jinja2docker?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dinuta/jinja2docker&amp;utm_campaign=Badge_Grade)
## Docker Hub
https://hub.docker.com/r/dinutac/jinja2docker

[![](https://images.microbadger.com/badges/image/dinutac/jinja2docker.svg)](https://microbadger.com/images/dinutac/jinja2docker "Get your own image badge on microbadger.com") [![](https://images.microbadger.com/badges/version/dinutac/jinja2docker.svg)](https://microbadger.com/images/dinutac/jinja2docker "Get your own version badge on microbadger.com") ![](https://img.shields.io/docker/pulls/dinutac/jinja2docker.svg)

Steps:   
*  Mount the directory containing your template(s) to the container's **/data** directory
*  Mount the directory containing your variables file(s) directory **/variables**
*  Pass needed env vars (any number)
*  In your jinja2 template get OS environment variables plus your inserted environment vars with ```environ('your_env_var')```

## Supported formats (default)

Check [jinja2-cli](https://github.com/mattrobenolt/jinja2-cli) commands for all supported formats.  

## Supported formats (embedded custom render)

If you want to use the custom embedded render you must override the entrypoint with ```/scripts/entities/render.py```

## Syntax

```bash
docker run --rm \
-v **TEMPLATE_FOLDER**:/data \ 
-v **VARIABLES_FOLDER**:/variables  \
-e CUSTOM_ENV_VAR=**VALUE** \
dinutac/jinja2docker:latest /data/json.j2 /variables/json.json --format=json > **OUTPUT_FILE**
```

Example 1: 
```bash
docker run --rm 
-v $PWD\inputs\templates:/data 
-v $PWD\inputs\variables:/variables \
-e DATABASE=mysql56 -e IMAGE=latest \
dinutac/jinja2docker:latest /data/standalone.j2 /variables/variables.yml --format=yaml > docker-compose.yml
```

Example 2:
```bash
docker run --rm 
-v $PWD\inputs\templates:/data 
-v $PWD\inputs\variables:/variables
dinutac/jinja2docker:latest /data/json.j2 /variables/json.json --format=json
```

## Example template ```json-template.j2```
``` txt
Os: {{os}}
Flavour: {{flavour}}
   
Path: {{environ('PATH')}}
```

## Example json variables file ```variables.json```
```json
{
  "os" : "Linux",
  "flavour": "CentOS"
}
```

## Example result  
```json
Os: Linux
Flavour: CentOS

Path: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

## Custom jinja2 render
-  Override the ```render.py``` file (you must use this file name) in **/scripts/entities/render.py** in order to execute your own logic.
-  Verify the Dockerfile and add the needed python packages.

# Latest updates  

### Added flask restful server

[Info in wiki](https://github.com/dinuta/jinja2docker/wiki)  
[Collection](https://documenter.getpostman.com/view/2360061/SVYjUN7j)    
  
