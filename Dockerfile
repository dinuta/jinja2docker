FROM alpine:3.9.4

RUN apk add --no-cache python3 && \
    pip3 install --upgrade pip setuptools --no-cache

RUN apk add --no-cache \
  build-base \
  sshpass 

RUN pip3 install \
  PyYAML \
  httplib2 \
  urllib3 \
  simplejson \
  Jinja2 \
  jinja2-cli \
  flask \
  flask_restplus\
  jsonify \
  parameterized \
  flask_swagger_ui \
  flask_cors


## Cleanup
RUN rm -rf /var/cache/apk/* 

# Create a shared data volume
# create an empty file, otherwise the volume will
# belong to root.
RUN mkdir /data/

## Expose some volumes
VOLUME ["/data"]
VOLUME ["/variables"]

ENV TEMPLATES_DIR /data
ENV VARS_DIR /variables
ENV SCRIPTS_DIR /home/dev/scripts
ENV OUT_DIR out
ENV TEMPLATE docker-compose.j2
ENV VARIABLES variables.yml

ADD . $SCRIPTS_DIR/
RUN chmod +x $SCRIPTS_DIR/*.py
 
WORKDIR /data

ENTRYPOINT ["python3", "/home/dev/scripts/main.py"]
