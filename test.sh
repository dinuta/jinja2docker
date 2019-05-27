#!/bin/bash

docker run -i   -v C:\Users\cdinuta\IdeaProjects\jinja2docker\templates:/data \
-v C:\Users\cdinuta\IdeaProjects\jinja2docker\variables:/variables   \
-e TEMPLATE=standalone.j2 -e VARIABLES=variables.yml -e DATABASE=mysql56 cdinuta/jinja2:latest > docker-compose.yml
