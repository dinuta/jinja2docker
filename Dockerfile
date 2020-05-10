FROM alpine:3.11

RUN apk add --no-cache python3
RUN pip3 install --upgrade pip==20.0.2 setuptools==46.1.3 --no-cache

RUN apk add --no-cache build-base sshpass

## Cleanup
RUN rm -rf /var/cache/apk/* 

# Create a shared data volume
RUN mkdir /data/

## Expose some volumes
VOLUME ["/data"]
VOLUME ["/variables"]

ENV TEMPLATES_DIR /data
ENV VARS_DIR /variables
ENV SCRIPTS_DIR /scripts
ENV OUT_DIR out
ENV TEMPLATE docker-compose.j2
ENV VARIABLES variables.yml

COPY . $SCRIPTS_DIR/
RUN chmod +x $SCRIPTS_DIR/*.py
 
WORKDIR /data

RUN pip3 install -r $SCRIPTS_DIR/requirements.txt

ENTRYPOINT ["python3", "/scripts/entities/render.py"]
