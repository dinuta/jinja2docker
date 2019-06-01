FROM alpine:latest

RUN apk add --update python3 && \
    pip3 install --upgrade pip setuptools

RUN apk add \
  build-base \
  sshpass \
  sudo

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
  requests \
  parameterized


## Cleanup
RUN apk del \
  python-dev \
  make && \
  rm -rf /var/cache/apk/*

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
