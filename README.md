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
*  In your jinja2 template get OS environment variables plus your inserted env vars from docker run cmd with ```environ('your_env_var')```

## Supported formats
- json
- yaml  

[Check Jinja2 cli commands inside Docker for other formats](#latest-updates)  

## Synthax
docker run -i   -v **your_jinja2_template_folder**:/data \ 
-v **your_jinja2_variables_file_folder**:/variables  \
-e TEMPLATE=**filename_of_your_j2_template** -e VARIABLES=**filename_of_your_variable_file** \
-e **list_of_your_env_vars** dinutac/jinja2docker:latest > **your_output_file**

Example: 
```
docker run -i   -v %cd%\inputs\templates:/data \ 
-v %cd%\inputs\variables:/variables   -e TEMPLATE=standalone.j2 \ 
-e VARIABLES=variables.yml -e DATABASE=mysql56 -e IMAGE=latest dinutac/jinja2docker:latest > docker-compose.yml
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
## Built-in filters
yaml


Example {{yourYamlVariableHere | yaml | safe }}

## Additional flexibility & base image inheritance
-  !Verify the Dockerfile in order to check the python packages installed inside.
-  Override the ```render.py``` file (you must use this file name) in /home/dev/bin/ in order to execute your own logic.
-  If no support exists in the current image use this as base image and add your python packages using pip commands.

## Limitations
-  big chunks of yaml data can't be pasted into the jinja2 template files. Currently no yaml filter exists in jinja2.
 Custom yaml filter was implemented and 2 variants were tested:  
```yaml.dump(value, sys.stdout, Dumper=yaml.RoundTripDumper, indent=4)``` tested, keeps indentations but does not glue yaml chunk where needed)  
```yaml.dump(value, Dumper=yaml.RoundTripDumper, indent=4)```  this is the current implementation, but does not keep indentations for large chunks of yaml)  

The recommendation is either paste selectively smaller chunks of yaml or use json whenever possible.

## Latest updates  

### 1. Integrated Jinja2 Cli 

https://github.com/mattrobenolt/jinja2-cli  

#### Generate template with container up
-  run the docker compose:  ``docker-compose up``
-  run the docker exec command with the jinja2-cli params as per documentation: https://github.com/mattrobenolt/jinja2-cli  by specifying template and variables folders.

Synthax:  
docker exec jinja2docker **jinja2_cli_command**  

Example:  
```
docker exec -e DATABASE=mysql56 -e IMAGE=latest jinja2docker \
jinja2 /data/standalone.j2 /variables/variables.yml --format=yml > docker-compose.yml
```

#### Hybrid call 
```
docker run --entrypoint jinja2   \
-v %cd%\inputs\templates:/data \
-v %cd%\inputs\variables:/variables \
dinutac/jinja2docker:latest \
/data/json.j2 /variables/json.json --format=json
```

!observe that jinja2 is called before image name and the arguments after


### 2. Added flask restful server
[Info in wiki](https://github.com/dinuta/jinja2docker/wiki)

## Postman collections
[Collection](https://documenter.getpostman.com/view/2360061/SVYjUN7j)  

## Api docs
/api/docs

## 3. Added kubernetes deployment for flask restful server
Added deployment and service files for kubernetes.
