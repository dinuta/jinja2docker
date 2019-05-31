FROM alpine:latest

ENV PUID 1000
ENV PGID 1000


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
  requests


## Cleanup
RUN apk del \
  python-dev \
  make && \
  rm -rf /var/cache/apk/*

# create dev user
RUN addgroup -g $PGID dev && \
  adduser -h /config -u $PUID -H -D -G dev -s /bin/bash dev && \
  mkdir -p /home/dev/bin && \
  sed -ri 's/(wheel:x:10:root)/\1,dev/' /etc/group && \
  sed -ri 's/# %wheel ALL=\(ALL\) NOPASSWD: ALL/%wheel ALL=\(ALL\) NOPASSWD: ALL/' /etc/sudoers
  
# Create a shared data volume
# create an empty file, otherwise the volume will
# belong to root.
RUN mkdir /data/ && \
 touch /data/.extra && \
 chown -R dev:dev /data

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
RUN chown -R dev:dev /home/dev && chmod +x $SCRIPTS_DIR/*.py
 
WORKDIR /data

ENTRYPOINT ["python3 $SCRIPTS_DIR/main.py"]
