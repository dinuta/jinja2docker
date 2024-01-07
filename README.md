# Jinja2 templating with Docker

## Docker Hub
[Docker Hub Image](https://hub.docker.com/r/dinutac/jinja2docker)  

![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/dinutac/jinja2docker/2.1.8) ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/dinutac/jinja2docker/2.1.8) ![](https://img.shields.io/docker/pulls/dinutac/jinja2docker.svg)

## Github docker image
Docker hub enforced [rate limits](https://www.docker.com/increase-rate-limits) starting with November 2020.  
[Github Docker Image as package](https://github.com/dinuta/jinja2docker/packages/546841)

## Steps to use   
*   Mount the directory containing your template(s) to the container's **/templates** directory
*   Mount the directory containing your variables file(s) directory **/variables**
*   Pass needed env vars (any number)
*   In your jinja2 template get OS environment variables plus your inserted environment vars with ```environ('your_env_var')```

## Supported formats (default)
*   YAML
*   JSON
*   XML
*   TOML
*   HJSON
*   JSON5

Check [jinja2-cli](https://github.com/mattrobenolt/jinja2-cli) commands for all supported formats.  

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
docker run --rm \
-v $PWD/inputs/templates:/templates \
-v $PWD/inputs/variables:/variables \
-e DATABASE=mysql56 -e IMAGE=latest \
dinutac/jinja2docker:latest /templates/standalone.j2 /variables/variables.yml --format=yaml > docker-compose.yml
```

Example 2:
```bash
docker run --rm \
-v $PWD/inputs/templates:/templates \
-v $PWD/inputs/variables:/variables \
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
  
